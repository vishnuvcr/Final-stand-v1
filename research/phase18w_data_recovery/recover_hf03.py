from pathlib import Path
from datetime import datetime, timezone
import json, os, zipfile, io, requests
import pandas as pd
from huggingface_hub import snapshot_download

ROOT=Path('research/phase18w_data_recovery/output/hf03'); ROOT.mkdir(parents=True,exist_ok=True)
targets=[x.strip() for x in Path('research/phase18w_data_recovery/FROZEN_63_EXPIRIES.csv').read_text().splitlines()[1:] if x.strip()]
patterns=[f'options/NIFTY/{d}.parquet' for d in targets]+['index/NIFTY.parquet']
local=snapshot_download('thetrademarkk/india-index-options-1m',repo_type='dataset',allow_patterns=patterns,local_dir=ROOT,token=os.getenv('HF_TOKEN'),max_workers=8)

api_url='https://api.github.com/repos/vishnuvcr/Final-stand-v1/actions/artifacts/11060261904/zip'
headers={'Authorization':f'Bearer {os.environ.get("GITHUB_TOKEN","")}'}
z=requests.get(api_url,headers=headers,timeout=120); z.raise_for_status()
with zipfile.ZipFile(io.BytesIO(z.content)) as zz:
    name=[n for n in zz.namelist() if n.endswith('weekly_cycle_manifest.csv')][0]
    manifest=pd.read_csv(io.BytesIO(zz.read(name)))
manifest=manifest[manifest.status.eq('USABLE_OHLC')].copy()

K1_RULES=['OTM1','OTM2','OTM3','ATM_NEAREST','ATM_UP','ITM1','ITM2','ITM3']
K2_RULES=['NEXT1','NEXT2','NEXT3','MIRROR_GAP']
MULTS=[0.5,1.0,1.5,2.0,2.5,3.0,4.0]

def choose_k1(strikes,spot,rule):
    s=sorted(float(x) for x in strikes)
    up=[x for x in s if x>spot]; down=[x for x in s if x<spot]
    if rule=='OTM1': return up[0] if len(up)>=1 else None
    if rule=='OTM2': return up[1] if len(up)>=2 else None
    if rule=='OTM3': return up[2] if len(up)>=3 else None
    if rule=='ATM_NEAREST': return min(s,key=lambda x:(abs(x-spot),-x)) if s else None
    if rule=='ATM_UP': return next((x for x in s if x>=spot),None)
    if rule=='ITM1': return down[-1] if len(down)>=1 else None
    if rule=='ITM2': return down[-2] if len(down)>=2 else None
    if rule=='ITM3': return down[-3] if len(down)>=3 else None

def choose_k2(strikes,spot,k1,rule):
    up=sorted(float(x) for x in strikes if float(x)>k1)
    if rule=='NEXT1': return up[0] if len(up)>=1 else None
    if rule=='NEXT2': return up[1] if len(up)>=2 else None
    if rule=='NEXT3': return up[2] if len(up)>=3 else None
    gap=abs(spot-k1)
    return min(up,key=lambda x:(abs((x-k1)-gap),x)) if up else None

def build_open_map(df, ts):
    q=df[(df.timestamp==ts)&(df.option_type.astype(str).str.upper().isin(['CE','C']))].copy()
    q=q[q.volume.fillna(0)>0].dropna(subset=['open'])
    return dict(zip(q.strike.astype(float), q.open.astype(float)))

def nearest_k3(strikes, opens, k2, target):
    above=[x for x in strikes if x>k2 and x in opens]
    return min(above,key=lambda x:(abs(opens[x]-target),x)) if above else None

spot_path=Path(local)/'index/NIFTY.parquet'
spot=pd.read_parquet(spot_path); spot['timestamp']=pd.to_datetime(spot['timestamp'])
rows=[]; control=[]
for _,cy in manifest.iterrows():
    expiry=str(cy.target_expiry); p=Path(local)/f'options/NIFTY/{expiry}.parquet'
    df=pd.read_parquet(p); df['timestamp']=pd.to_datetime(df['timestamp'])
    entry_ts=pd.Timestamp(cy.entry_timestamp); lock_ts=pd.Timestamp(cy.lock_timestamp)
    es=spot[spot.timestamp==entry_ts]
    entry_spot=float(es.open.iloc[0]) if len(es) else float(cy.entry_spot)
    ent=df[(df.timestamp==entry_ts)&(df.option_type.astype(str).str.upper().isin(['CE','C']))].copy()
    ent=ent[ent.volume.fillna(0)>0].dropna(subset=['open'])
    strikes=sorted(ent.strike.astype(float).unique())
    entry_opens=build_open_map(df, entry_ts)
    lock_opens=build_open_map(df, lock_ts)
    valid=0
    for k1r in K1_RULES:
        k1=choose_k1(strikes,entry_spot,k1r)
        for k2r in K2_RULES:
            k2=choose_k2(strikes,entry_spot,k1,k2r) if k1 is not None else None
            for m in MULTS:
                k3=None; p1=p2=None
                if k2 is not None:
                    p1=entry_opens.get(float(k1)); p2=entry_opens.get(float(k2))
                    if p1 is not None and p2 is not None and p1-p2>0:
                        target=m*(p1-p2); k3=nearest_k3(strikes, entry_opens, k2, target)
                ok=all(x is not None for x in [k1,k2,k3]) and all(float(x) in entry_opens for x in [k1,k2,k3]) and all(float(x) in lock_opens for x in [k1,k2,k3])
                if ok: valid+=1
                if k1r=='OTM1' and k2r=='NEXT1' and abs(m-2.0)<1e-9: control.append({'target_expiry':expiry,'entry_spot':entry_spot,'k1':k1,'k2':k2,'k3':k3,'valid':ok})
    rows.append({'target_expiry':expiry,'entry_timestamp':str(entry_ts),'lock_timestamp':str(lock_ts),'entry_strikes':len(strikes),'valid_variants':valid,'coverage_rate':valid/224.0})

out={'generated_utc':datetime.now(timezone.utc).isoformat(),'cycles':len(rows),'variant_family':224,'cycle_results':rows,'total_variant_cycle_cells':sum(x['valid_variants'] for x in rows)}
Path('research/phase18w_data_recovery/output/hf03_variant_coverage.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
pd.DataFrame(rows).to_csv('research/phase18w_data_recovery/output/hf03_variant_coverage.csv',index=False)
pd.DataFrame(control).to_csv('research/phase18w_data_recovery/output/hf03_control_crosscheck.csv',index=False)
print(json.dumps({'cycles':len(rows),'total_cells':out['total_variant_cycle_cells'],'mean_cycle_coverage':sum(x['coverage_rate'] for x in rows)/len(rows)},indent=2))