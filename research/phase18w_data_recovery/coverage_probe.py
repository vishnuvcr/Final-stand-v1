from pathlib import Path
from datetime import datetime, timezone
import json, os
from huggingface_hub import HfApi
OUT=Path('research/phase18w_data_recovery/output'); OUT.mkdir(parents=True,exist_ok=True)
api=HfApi(token=os.getenv('HF_TOKEN'))
targets=[x.strip() for x in Path('research/phase18w_data_recovery/FROZEN_63_EXPIRIES.csv').read_text().splitlines()[1:] if x.strip()]
report={'generated_utc':datetime.now(timezone.utc).isoformat(),'target_cycles':len(targets),'sources':[]}
for sid,repo_id in [('HF-01','rissin/nse-options-intraday'),('HF-02','artist-23/nifty-options-data'),('HF-03','thetrademarkk/india-index-options-1m')]:
 row={'id':sid,'repo':repo_id}
 try:
  info=api.dataset_info(repo_id); files={x.rfilename for x in (info.siblings or [])}
  row['metadata_status']='ok'; row['file_count']=len(files); row['sha']=getattr(info,'sha',None)
  if sid=='HF-03':
   expected=[f'options/NIFTY/{d}.parquet' for d in targets]; present=[f for f in expected if f in files]
   row['target_expiry_files_present']=len(present); row['target_expiry_files_missing']=[f for f in expected if f not in files]
  if sid=='HF-02': row['weekly_schema_files_present']=len([f for f in files if f.startswith('NIFTY/WEEK/') and f.endswith('.parquet')])
  if sid=='HF-01': row['nifty_intraday_year_files']=sorted([f for f in files if f.startswith('upstox_intraday/NIFTY/') and f.endswith('.parquet')])
 except Exception as exc: row['metadata_status']='error'; row['error']=repr(exc)
 report['sources'].append(row)
Path(OUT/'target_coverage_inventory.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))