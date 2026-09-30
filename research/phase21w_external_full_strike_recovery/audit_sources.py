from pathlib import Path
import json
out=Path('research/phase21w_external_full_strike_recovery/output'); out.mkdir(parents=True,exist_ok=True)
rows=[
 {'source':'Upstox','route':'expired option contracts / 1-minute candles','status':'requires credentials/entitlement','admission':'not yet tested'},
 {'source':'ICICI Breeze','route':'historical option data','status':'requires API credentials','admission':'not yet tested'},
 {'source':'Dhan','route':'expired options API','status':'requires API credentials','admission':'not yet tested'},
 {'source':'NSE/BSE','route':'historical derivatives datasets','status':'public/controlled access varies','admission':'not yet tested'},
 {'source':'Public mirrors','route':'GitHub/Kaggle/HF/open datasets','status':'audited in Phase 18/20','admission':'insufficient full-strike coverage'}]
(out/'source_access_audit.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
