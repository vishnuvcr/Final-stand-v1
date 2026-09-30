from __future__ import annotations

import hashlib
import json
from pathlib import Path

import polars as pl
from huggingface_hub import HfApi, hf_hub_download

REPO_ID = 'thetrademarkk/india-index-options-1m'
MISSING = ['2026-01-13','2026-02-10','2026-03-10','2026-04-13','2026-05-12']
OUT = Path('research/phase21w_external_full_strike_recovery/output')
OUT.mkdir(parents=True, exist_ok=True)

token = None
api = HfApi(token=token)
info = api.dataset_info(REPO_ID, revision='main')
resolved_revision = getattr(info, 'sha', None) or 'main'

rows = []
for expiry in MISSING:
    filename = f'options/NIFTY/{expiry}.parquet'
    rec = {'source':'thetrademarkk/india-index-options-1m','repo_id':REPO_ID,'dataset_revision':resolved_revision,'expiry':expiry,'filename':filename}
    try:
        local = Path(hf_hub_download(repo_id=REPO_ID, filename=filename, repo_type='dataset', revision=resolved_revision, token=token, cache_dir=str(Path.home()/'.cache/huggingface')))
        rec['sha256'] = hashlib.sha256(local.read_bytes()).hexdigest()
        schema = pl.read_parquet_schema(local)
        rec['columns'] = list(schema.keys())
        lf = pl.scan_parquet(local)
        required = {'timestamp','open','high','low','close','volume','open_interest','strike','option_type','expiry'}
        rec['missing_columns'] = sorted(required-set(schema.keys()))
        if rec['missing_columns']:
            rec['status']='REJECT_SCHEMA'
            rows.append(rec)
            continue
        df = lf.filter((pl.col('expiry').cast(pl.String)==expiry) & (pl.col('option_type').cast(pl.String).str.to_uppercase()=='CE')).select(['timestamp','strike','open','high','low','close','volume','open_interest','expiry','option_type']).collect()
        rec['ce_rows'] = df.height
        rec['unique_strikes'] = df.select(pl.col('strike').n_unique()).item()
        dup = df.group_by(['timestamp','strike','option_type','expiry']).len().filter(pl.col('len')>1).height
        rec['duplicate_groups'] = dup
        bad = df.select([pl.col(c).is_null().sum().alias(c) for c in ['open','high','low','close','volume','strike']]).row(0)
        rec['null_price_or_strike_fields'] = int(sum(bad))
        # Dataset timestamps are documented as IST; filter exact local minute keys.
        keyed = df.with_columns([
            pl.col('timestamp').dt.date().cast(pl.String).alias('_date'),
            pl.col('timestamp').dt.hour().alias('_hour'),
            pl.col('timestamp').dt.minute().alias('_minute'),
        ])
        at10 = keyed.filter((pl.col('_date')==expiry) & (pl.col('_hour')==10) & (pl.col('_minute')==0))
        at14 = keyed.filter((pl.col('_date')==expiry) & (pl.col('_hour')==14) & (pl.col('_minute')==0))
        s10 = sorted(set(at10['strike'].to_list()))
        s14 = sorted(set(at14['strike'].to_list()))
        rec['entry_10_strike_count'] = len(s10)
        rec['lock_14_strike_count'] = len(s14)
        rec['entry_lock_common_strike_count'] = len(set(s10)&set(s14))
        rec['entry_strikes_sample'] = s10[:20]
        rec['lock_strikes_sample'] = s14[:20]
        rec['status'] = 'SOURCE_LEVEL_PASS' if rec['duplicate_groups']==0 and rec['null_price_or_strike_fields']==0 and rec['ce_rows']>0 else 'SOURCE_LEVEL_FAIL'
    except Exception as exc:
        rec['status']='ERROR'
        rec['error']=repr(exc)
    rows.append(rec)

(OUT/'hf_missing_expiry_probe.json').write_text(json.dumps(rows,indent=2,default=str))
pl.DataFrame(rows).write_csv(OUT/'hf_missing_expiry_probe.csv')
print(json.dumps(rows,indent=2,default=str))