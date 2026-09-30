import json, os, re
from pathlib import Path
from huggingface_hub import HfApi

SOURCES=[
 {"id":"RECOVERY-1","repo":"johnwick3690/stocks","revision":"main","kind":"dataset"},
 {"id":"RECOVERY-2","repo":"artist-23/nifty-options-data","revision":"45e0a043f34f3f40f9694e52a944297803c2af8b","kind":"dataset"},
 {"id":"RECOVERY-3","repo":"rissin/nse-options-intraday","revision":"8f7739cab3f38abdcbc6332a6d0a83e1341326e3","kind":"dataset"},
]
TARGET=json.loads(Path("research/phase19w_recovered_rerun/output/baseline_calendar.json").read_text())
OUT=Path("research/phase20w_multisource_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
api=HfApi(token=os.getenv("HF_TOKEN") or None)
report={"targets":TARGET,"sources":[]}
for s in SOURCES:
    info=api.repo_info(s["repo"],repo_type=s["kind"],revision=s["revision"])
    files=api.list_repo_files(s["repo"],repo_type=s["kind"])
    parquet=[f for f in files if f.lower().endswith(".parquet")]
    matches={}
    for d in TARGET:
        hits=[f for f in parquet if d in f or d.replace("-","") in f or d.replace("-","_") in f]
        if hits: matches[d]=hits[:25]
    report["sources"].append({**s,"parquet_file_count":len(parquet),"resolved_sha":getattr(info,"sha",None),"target_file_matches":matches,"sample_parquet_files":parquet[:100]})
Path(OUT/"source_inventory.json").write_text(json.dumps(report,indent=2))
print(json.dumps({s["id"]:{"parquet_file_count":s["parquet_file_count"],"target_dates_matched":len(s["target_file_matches"])} for s in report["sources"]},indent=2))
