from __future__ import annotations
import json, os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

IST=ZoneInfo("Asia/Kolkata")
OUT=Path("research/phase20w_executable_bar_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
HF_CACHE=Path(os.getenv("HF_CACHE","~/.cache/huggingface")).expanduser()
HF1_PIN="78b1c5468255d18cf492984bfe6fe4e3ac874d7c"
HF2_PIN="45e0a043f34f3f40f9694e52a944297803c2af8b"
token=os.getenv("HF_TOKEN") or None

req=pl.read_csv(OUT/"required_missing_variant_bars.csv")
# The Phase-19 branch already contains the exact 27-cycle inventory; recovery never alters it.
if req.height==0:
    raise RuntimeError("required_missing_variant_bars.csv is empty")

api=HfApi(token=token)
hf1_main_sha=getattr(api.repo_info("rissin/nse-options-intraday",repo_type="dataset",revision="main"),"sha",None) or "main"

# Cache only source files actually needed for the missing cycles.
source_frames=[]
source_prov=[]

def add_hf1(year, revision):
    p=f"upstox_intraday/NIFTY/NIFTY_{year}.parquet"
    try:
        local=hf_hub_download(repo_id="rissin/nse-options-intraday",filename=p,repo_type="dataset",revision=revision,token=token,cache_dir=str(HF_CACHE))
        df=pl.read_parquet(local)
        df=df.filter(pl.col("underlying")=="NIFTY").with_columns(
            pl.col("timestamp").cast(pl.String).str.replace(r" ", "T").str.slice(0,19).alias("_ts")
        )
        source_frames.append(("HF1",str(revision),p,df))
        source_prov.append({"source":"HF1","revision":str(revision),"path":p,"rows":df.height})
    except Exception as e:
        source_prov.append({"source":"HF1","revision":str(revision),"path":p,"error":repr(e)})

years=sorted({int(x[:4]) for x in req["target_expiry"].cast(pl.String).unique().to_list()})
for y in years:
    if y>=2024:
        add_hf1(y, HF1_PIN if y<2026 else hf1_main_sha)

# HF2 weekly ATM-relative CE files, used only when a complete variant-cycle cannot be obtained from HF1.
hf2_frames=[]
for off in range(-10,11):
    tag="ATM" if off==0 else f"ATM{off:+d}"
    p=f"NIFTY/WEEK/{tag}_CE.parquet"
    try:
        local=hf_hub_download(repo_id="artist-23/nifty-options-data",filename=p,repo_type="dataset",revision=HF2_PIN,token=token,cache_dir=str(HF_CACHE))
        df=pl.read_parquet(local).with_columns(pl.col("datetime").cast(pl.String).str.replace(r" ", "T").str.slice(0,19).alias("_ts"))
        hf2_frames.append((tag,p,df))
    except Exception as e:
        source_prov.append({"source":"HF2","revision":HF2_PIN,"path":p,"error":repr(e)})

recovered=[]
decisions=[]
for row in req.iter_rows(named=True):
    exp=str(row["target_expiry"]); entry=str(row["entry_timestamp"]).replace("+05:30","")[:19]; lock=str(row["lock_timestamp"]).replace("+05:30","")[:19]
    strikes=[float(row["k1"]),float(row["k2"]),float(row["k3"])]
    chosen=None; bars=[]
    # A source is admitted only if all three strikes have exact entry and lock observations.
    for source,rev,path,df in source_frames:
        q=df.filter((pl.col("expiry").cast(pl.String).str.slice(0,10)==exp)&pl.col("strike").is_in(strikes)&pl.col("_ts").is_in([entry,lock])& (pl.col("option_type").str.to_uppercase().is_in(["CE","CALL"])))
        keys=set((str(x["strike"]),str(x["_ts"])) for x in q.select(["strike","_ts"]).iter_rows(named=True))
        if all((str(s),entry) in keys and (str(s),lock) in keys for s in strikes):
            chosen=(source,rev,path,q)
            break
    if chosen is None:
        # HF2 is keyed by ATM-relative files; combine only within the single HF2 dataset source.
        qparts=[]
        for tag,path,df in hf2_frames:
            q=df.filter((pl.col("date").cast(pl.String).str.slice(0,10).is_in([exp,entry,lock])) & pl.col("strike_price").is_in(strikes))
            if q.height: qparts.append(q)
        if qparts:
            q=pl.concat(qparts,how="diagonal")
            keys=set((str(x["strike_price"]),str(x["_ts"])) for x in q.select(["strike_price","_ts"]).iter_rows(named=True))
            if all((str(s),entry) in keys and (str(s),lock) in keys for s in strikes):
                chosen=("HF2",HF2_PIN,"NIFTY/WEEK/ATM±0..10_CE",q)
    if chosen is None:
        decisions.append({"variant_id":row["variant_id"],"target_expiry":exp,"status":"UNRECOVERED","source":None})
        continue
    source,rev,path,q=chosen
    q=q.select([c for c in q.columns if c in ["timestamp","datetime","_ts","strike","strike_price","option_type","open","high","low","close","volume","oi","expiry","date","spot","source","granularity"]])
    q=q.with_columns(pl.lit(row["variant_id"]).alias("variant_id"),pl.lit(exp).alias("target_expiry"),pl.lit(source).alias("recovery_source"),pl.lit(rev).alias("recovery_revision"))
    recovered.append(q)
    decisions.append({"variant_id":row["variant_id"],"target_expiry":exp,"status":"RECOVERED","source":source,"revision":rev,"path":path})

if recovered:
    pl.concat(recovered,how="diagonal").write_parquet(OUT/"recovered_executable_bars.parquet",compression="zstd")
pl.DataFrame(decisions).write_csv(OUT/"recovery_decisions.csv")
Path(OUT/"recovery_provenance.json").write_text(json.dumps({"hf1_pinned":HF1_PIN,"hf1_main_resolved":hf1_main_sha,"hf2_pinned":HF2_PIN,"sources":source_prov},indent=2,default=str))
d=pl.DataFrame(decisions)
print(json.dumps({"required_variant_cycles":req.height,"recovered":d.filter(pl.col("status")=="RECOVERED").height,"unrecovered":d.filter(pl.col("status")=="UNRECOVERED").height,"sources":d.group_by("source").len().to_dicts()},indent=2))
