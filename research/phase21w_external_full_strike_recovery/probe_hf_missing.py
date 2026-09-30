from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('POLARS_IGNORE_TIMEZONE_PARSE_ERROR', '1')
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

REPO_ID = 'rissin/nse-options-intraday'
REVISION = '78b1c5468255d18cf492984bfe6fe4e3ac874d7c'
FILENAME = 'upstox_intraday/NIFTY/NIFTY_2026.parquet'
MISSING = ['2026-01-13','2026-02-10','2026-03-10','2026-04-13','2026-05-12']
OUT = Path('research/phase21w_external_full_strike_recovery/output')
OUT.mkdir(parents=True, exist_ok=True)

token = os.getenv('HF_TOKEN') or None
api = HfApi(token=token)
info = api.dataset_info(REPO_ID, revision=REVISION)
resolved_revision = getattr(info, 'sha', None) or REVISION
local = Path(hf_hub_download(repo_id=REPO_ID, filename=FILENAME, repo_type='dataset', revision=REVISION, token=token, cache_dir=str(Path.home()/'.cache/huggingface')))
sha256 = hashlib.sha256(local.read_bytes()).hexdigest()

lf = pl.scan_parquet(local)
required = {'date','timestamp','underlying','expiry','strike','option_type','open','high','low','close','volume','oi','source','granularity'}
schema = pl.read_parquet_schema(local)
missing_columns = sorted(required - set(schema.keys()))
if missing_columns:
    raise RuntimeError(f'Missing Rissin schema columns: {missing_columns}')

df = (
    lf.filter(
        (pl.col('underlying').cast(pl.String).str.to_uppercase() == 'NIFTY')
        & (pl.col('expiry').cast(pl.String).is_in(MISSING))
        & (pl.col('option_type').cast(pl.String).str.to_uppercase() == 'CE')
        & (pl.col('source').cast(pl.String) == 'upstox_expired')
        & (pl.col('granularity').cast(pl.String) == '1min')
    )
    .select(['date','timestamp','underlying','expiry','strike','option_type','open','high','low','close','volume','oi','source','granularity'])
    .collect(streaming=True)
)

rows = []
for expiry in MISSING:
    cur = df.filter(pl.col('expiry').cast(pl.String) == expiry)
    rec = {
        'source':'rissin/nse-options-intraday',
        'repo_id':REPO_ID,
        'dataset_revision':resolved_revision,
        'requested_revision':REVISION,
        'filename':FILENAME,
        'file_sha256':sha256,
        'expiry':expiry,
        'ce_rows':cur.height,
        'unique_strikes_full_day':cur.select(pl.col('strike').n_unique()).item() if cur.height else 0,
    }
    if not cur.height:
        rec['status'] = 'NO_ROWS'
        rows.append(rec)
        continue
    dup = cur.group_by(['timestamp','strike','option_type','expiry']).len().filter(pl.col('len')>1).height
    bad = cur.select([pl.col(c).is_null().sum().alias(c) for c in ['open','high','low','close','volume','strike']]).row(0)
    rec['duplicate_groups'] = int(dup)
    rec['null_price_or_strike_fields'] = int(sum(bad))
    keyed = cur.with_columns([
        pl.col('timestamp').dt.date().cast(pl.String).alias('_date'),
        pl.col('timestamp').dt.hour().alias('_hour'),
        pl.col('timestamp').dt.minute().alias('_minute'),
    ])
    at10 = keyed.filter((pl.col('_date')==expiry) & (pl.col('_hour')==10) & (pl.col('_minute')==0))
    at14 = keyed.filter((pl.col('_date')==expiry) & (pl.col('_hour')==14) & (pl.col('_minute')==0))
    s10 = sorted(set(at10['strike'].to_list()))
    s14 = sorted(set(at14['strike'].to_list()))
    path = keyed.filter((pl.col('_date')==expiry) & (((pl.col('_hour')>10) | ((pl.col('_hour')==10)&(pl.col('_minute')>=0))) & ((pl.col('_hour')<14) | ((pl.col('_hour')==14)&(pl.col('_minute')<=0)))))
    path_counts = path.group_by('strike').len()
    rec['entry_10_strike_count'] = len(s10)
    rec['lock_14_strike_count'] = len(s14)
    rec['entry_lock_common_strike_count'] = len(set(s10) & set(s14))
    rec['path_unique_strikes'] = path.select(pl.col('strike').n_unique()).item() if path.height else 0
    rec['path_min_1min_rows_per_strike'] = path_counts['len'].min() if path_counts.height else 0
    rec['path_median_1min_rows_per_strike'] = path_counts['len'].median() if path_counts.height else 0
    rec['path_max_1min_rows_per_strike'] = path_counts['len'].max() if path_counts.height else 0
    rec['entry_strikes_sample'] = s10[:40]
    rec['lock_strikes_sample'] = s14[:40]
    rec['status'] = 'SOURCE_LEVEL_PASS' if dup == 0 and sum(bad) == 0 and len(s10) > 0 and len(s14) > 0 else 'SOURCE_LEVEL_FAIL'
    rows.append(rec)

(OUT/'hf_missing_expiry_probe.json').write_text(json.dumps(rows, indent=2, default=str))
keys = sorted({k for row in rows for k in row.keys()})
with (OUT/'hf_missing_expiry_probe.csv').open('w', newline='') as fh:
    writer = csv.DictWriter(fh, fieldnames=keys)
    writer.writeheader()
    for row in rows:
        writer.writerow({k:(json.dumps(row.get(k)) if isinstance(row.get(k),(list,dict)) else row.get(k)) for k in keys})
print(json.dumps(rows, indent=2, default=str))
