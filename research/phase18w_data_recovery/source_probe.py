from pathlib import Path
from datetime import datetime, timezone
import json, os, hashlib
from huggingface_hub import HfApi

OUT = Path('research/phase18w_data_recovery/output')
OUT.mkdir(parents=True, exist_ok=True)
api = HfApi(token=os.getenv('HF_TOKEN'))
sources = [
    ('HF-01','rissin/nse-options-intraday'),
    ('HF-02','artist-23/nifty-options-data'),
    ('HF-03','thetrademarkk/india-index-options-1m'),
]
report = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'sources': []}
for sid, repo in sources:
    row = {'id': sid, 'repo': repo}
    try:
        info = api.dataset_info(repo)
        row['status'] = 'metadata_ok'
        row['sha'] = getattr(info, 'sha', None)
        row['siblings'] = [x.rfilename for x in (info.siblings or [])]
    except Exception as exc:
        row['status'] = 'metadata_error'
        row['error'] = repr(exc)
    report['sources'].append(row)
Path(OUT/'hf_source_inventory.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
Path(OUT/'SOURCE_AUDIT.md').write_text('# Phase 18W Public Source Inventory\n\n```json\n'+json.dumps(report, indent=2)+'\n```\n', encoding='utf-8')
print(json.dumps(report, indent=2))