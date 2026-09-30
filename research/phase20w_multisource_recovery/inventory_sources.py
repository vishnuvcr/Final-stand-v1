import json, os, urllib.parse, requests
from pathlib import Path
TARGET=json.loads(Path("research/phase19w_recovered_rerun/output/baseline_calendar.json").read_text())
OUT=Path("research/phase20w_multisource_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
session=requests.Session()
headers={"Authorization":f"Bearer {os.getenv('HF_TOKEN','')}"} if os.getenv("HF_TOKEN") else {}

sources=[
 {"id":"RECOVERY-1","repo":"johnwick3690/stocks","revision":"main","base":"https://huggingface.co/datasets/johnwick3690/stocks/blob/main/nifty%20historical%20data/nifty%2050%201min%20options%20weekly%20expiries/"},
 {"id":"RECOVERY-2","repo":"artist-23/nifty-options-data","revision":"main","base":None},
 {"id":"RECOVERY-3","repo":"rissin/nse-options-intraday","revision":"main","base":None},
]
report={"targets":TARGET,"sources":[]}
for s in sources:
    item={**s,"probes":{}}
    if s["id"]=="RECOVERY-1":
        for d in TARGET:
            fn=f"{d.replace('-','')}_WEEK.parquet"
            url=s["base"]+urllib.parse.quote(fn)
            try:
                rr=session.get(url,stream=True,allow_redirects=True,timeout=30)
                item["probes"][d]={"status":rr.status_code,"content_length":rr.headers.get("content-length"),"final_url":rr.url}
                rr.close()
            except Exception as ex:
                item["probes"][d]={"error":type(ex).__name__+":"+str(ex)}
    else:
        item["probes"]={"status":"DEFERRED","reason":"No verified path template yet; retain registered source for next schema discovery step."}
    report["sources"].append(item)
Path(OUT/"source_inventory.json").write_text(json.dumps(report,indent=2))
print(json.dumps({s["id"]:({"matched":sum(1 for v in s["probes"].values() if isinstance(v,dict) and v.get("status")==200)} if isinstance(s.get("probes"),dict) else {}) for s in report["sources"]},indent=2))
