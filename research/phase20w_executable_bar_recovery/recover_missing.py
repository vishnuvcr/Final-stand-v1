from __future__ import annotations
import json, os, hashlib
import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path
from datetime import date, datetime
from zoneinfo import ZoneInfo
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

IST=ZoneInfo("Asia/Kolkata")
OUT=Path("research/phase20w_executable_bar_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
CACHE=Path(os.getenv("HF_CACHE","~/.cache/huggingface")).expanduser()
token=os.getenv("HF_TOKEN") or None
HF1_PIN="78b1c5468255d18cf492984bfe6fe4e3ac874d7c"
HF2_PIN="45e0a043f34f3f40f9694e52a944297803c2af8b"
K1=["OTM1","OTM2","OTM3","ATM_NEAREST","ATM_UP","ITM1","ITM2","ITM3"]
K2=["NEXT1","NEXT2","NEXT3","MIRROR_GAP"]
K3=[0.5,1.0,1.5,2.0,2.5,3.0,4.0]
variants=[f"{a}_{b}_K3M{m:g}" for a in K1 for b in K2 for m in K3]

base=pl.read_csv("research/phase9_weekly/output/weekly_cycle_manifest.csv")
trade=pl.read_csv("research/phase19w_recovered_rerun/output/trades_ITM3_NEXT1_K3M4.csv")
got=set(trade["target_expiry"].cast(pl.String).to_list())
missing=[x for x in base["target_expiry"].cast(pl.String).to_list() if x not in got]
base=base.with_columns(pl.col("target_expiry").cast(pl.String))
need=base.filter(pl.col("target_expiry").is_in(missing))

def choose_k1(strikes,spot,rule):
    s=sorted(set(float(x) for x in strikes))
    if rule=="OTM1": c=[k for k in s if k>spot]; return c[0] if c else None
    if rule=="OTM2": c=[k for k in s if k>spot]; return c[1] if len(c)>1 else None
    if rule=="OTM3": c=[k for k in s if k>spot]; return c[2] if len(c)>2 else None
    if rule=="ATM_NEAREST": return min(s,key=lambda k:(abs(k-spot),-k)) if s else None
    if rule=="ATM_UP": c=[k for k in s if k>=spot]; return c[0] if c else None
    if rule=="ITM1": c=[k for k in s if k<spot]; return c[-1] if c else None
    if rule=="ITM2": c=[k for k in s if k<spot]; return c[-2] if len(c)>1 else None
    if rule=="ITM3": c=[k for k in s if k<spot]; return c[-3] if len(c)>2 else None

def choose_k2(strikes,k1,rule):
    c=sorted(k for k in set(float(x) for x in strikes) if k>k1)
    if rule in {"NEXT1","NEXT2","NEXT3"}:
        i={"NEXT1":0,"NEXT2":1,"NEXT3":2}[rule]
        return c[i] if len(c)>i else None
    if rule=="MIRROR_GAP":
        return next((k for k in c if k>=2*k1), c[-1] if c else None)
    return None

def choose_k3(strikes,opens,k2,target):
    pairs=[(float(s),float(p)) for s,p in zip(strikes,opens) if float(s)>k2 and p is not None]
    if not pairs: return None,None
    return min(pairs,key=lambda x:(abs(x[1]-target),x[0]))

def norm_ts(x):
    return str(x).replace(" ","T").replace("+05:30","")[:19]

api=HfApi(token=token)
hf1_main_sha=getattr(api.repo_info("rissin/nse-options-intraday",repo_type="dataset",revision="main"),"sha",None) or "main"
frames=[]; cycles=[]; prov=[]
for exp in missing:
    b=need.filter(pl.col("target_expiry")==exp).row(0,named=True)
    entry=norm_ts(b["entry_timestamp"]); lock=norm_ts(b["lock_timestamp"]); spot=float(b["entry_spot"])
    source_df=None; source_name=None; source_rev=None; source_path=None
    year=int(exp[:4])
    if year>=2024:
        rev=HF1_PIN if year<2026 else hf1_main_sha
        path=f"upstox_intraday/NIFTY/NIFTY_{year}.parquet"
        try:
            local=hf_hub_download(repo_id="rissin/nse-options-intraday",filename=path,repo_type="dataset",revision=rev,token=token,cache_dir=str(CACHE))
            source_df=None
            source_name="HF1"; source_rev=str(rev); source_path=path
            source_local=local
        except Exception as e:
            prov.append({"expiry":exp,"source":"HF1","error":repr(e)})
    # For early missing dates, use the weekly ATM-relative HF-02 source.
    if source_df is None:
        parts=[]
        for off in range(-10,11):
            tag="ATM" if off==0 else f"ATM{off:+d}"
            path=f"NIFTY/WEEK/{tag}_CE.parquet"
            try:
                local=hf_hub_download(repo_id="artist-23/nifty-options-data",filename=path,repo_type="dataset",revision=HF2_PIN,token=token,cache_dir=str(CACHE))
                parts.append(pl.read_parquet(local))
            except Exception:
                pass
        if parts:
            source_df=pl.concat(parts,how="diagonal")
            source_name="HF2"; source_rev=HF2_PIN; source_path="NIFTY/WEEK/ATM±0..10_CE.parquet"
    if source_df is None:
        for vid in variants:
            cycles.append({"variant_id":vid,"target_expiry":exp,"entry_timestamp":b["entry_timestamp"],"lock_timestamp":b["lock_timestamp"],"status":"UNRECOVERED","source":None})
        continue
    if source_name=="HF1":
        table=pq.read_table(source_local,filters=[("expiry","=",exp),("option_type","=","CE"),("date",">=",entry[:10]),("date","<=",exp)],columns=["date","timestamp","expiry","strike","option_type","open","high","low","close","volume","oi"])
        pdf=table.to_pandas()
        pdf["timestamp"]=pdf["timestamp"].astype(str).str.replace(" ","T").str.slice(0,19)
        pdf["expiry"]=pdf["expiry"].astype(str).str.slice(0,10)
        source_df=pl.from_pandas(pdf)
        source_df=source_df.with_columns(pl.col("timestamp").alias("_ts"),pl.col("expiry").alias("_exp"))
        sdf=source_df
        entry_df=sdf.filter((pl.col("expiry")==exp)&(pl.col("timestamp")==entry)&(pl.col("volume").fill_null(0)>0))

    else:
        sdf=source_df.with_columns(pl.col("datetime").cast(pl.String).str.replace(r" ","T").str.slice(0,19).alias("_ts"))
        entry_df=sdf.filter((pl.col("_ts")==entry)&(pl.col("option_type").str.to_uppercase().is_in(["CE","CALL"])))
    strikes=entry_df["strike"].to_list() if source_name=="HF1" else entry_df["strike_price"].to_list()
    opens=entry_df["open"].to_list()
    bar_rows=[]
    for k1r in K1:
        k1=choose_k1(strikes,spot,k1r)
        for k2r in K2:
            k2=choose_k2(strikes,k1,k2r) if k1 is not None else None
            for m in K3:
                vid=f"{k1r}_{k2r}_K3M{m:g}"
                p1=None;p2=None;k3=None;p3=None
                if k1 is not None:
                    for s,p in zip(strikes,opens):
                        if float(s)==float(k1): p1=float(p)
                if k2 is not None:
                    for s,p in zip(strikes,opens):
                        if float(s)==float(k2): p2=float(p)
                target=(p1-p2)*m if p1 is not None and p2 is not None else None
                if target is not None and target>0:
                    k3,p3=choose_k3(strikes,opens,k2,target)
                status="INCOMPLETE"
                if k3 is not None and p3 is not None:
                    if source_name=="HF1":
                        lock_df=sdf.filter((pl.col("_exp")==exp)&(pl.col("_ts")==lock)&pl.col("strike").is_in([k1,k2,k3])&pl.col("option_type").str.to_uppercase().is_in(["CE","CALL"]))
                    else:
                        lock_df=sdf.filter((pl.col("_ts")==lock)&pl.col("strike_price").is_in([k1,k2,k3])&pl.col("option_type").str.to_uppercase().is_in(["CE","CALL"]))
                    lock_strikes=set((lock_df["strike"] if source_name=="HF1" else lock_df["strike_price"]).cast(pl.Float64).to_list())
                    if all(float(k) in lock_strikes for k in [k1,k2,k3]): status="USABLE_OHLC"
                cycles.append({"variant_id":vid,"target_expiry":exp,"prior_expiry":b["prior_expiry"],"historical_expiry_regime":b["historical_expiry_regime"],"entry_timestamp":b["entry_timestamp"],"lock_timestamp":b["lock_timestamp"],"source_file":source_path,"source_sha256":"","entry_spot":spot,"k1":k1,"k2":k2,"k3":k3,"p1":p1,"p2":p2,"target_premium":target,"k3_multiplier":m,"p3":p3,"target_error":(abs(p3-target)/target if p3 is not None and target else None),"status":status,"recovery_source":source_name,"recovery_revision":source_rev})
    # Store only the strikes required by usable recovered variants.
    usable=[x for x in cycles if x["target_expiry"]==exp and x["status"]=="USABLE_OHLC"]
    reqstr=sorted({float(k) for x in usable for k in [x["k1"],x["k2"],x["k3"]] if k is not None})
    if source_name=="HF1":
        bars=sdf.filter(pl.col("strike").is_in(reqstr)&(pl.col("timestamp")>=entry)&(pl.col("timestamp")<=f"{exp}T15:30:00"))
        bars=bars.select(["timestamp","strike","open","high","low","close","volume","oi"]).with_columns(pl.lit(exp).alias("target_expiry"))
    else:
        bars=sdf.filter(pl.col("strike_price").is_in(reqstr)&pl.col("_ts").is_between(entry,f"{exp}T15:30:00"))
        bars=bars.select([pl.col("datetime").alias("timestamp"),pl.col("strike_price").alias("strike"),"open","high","low","close","volume","oi"]).with_columns(pl.lit(exp).alias("target_expiry"))
    if bars.height: frames.append(bars)
    prov.append({"expiry":exp,"source":source_name,"revision":source_rev,"path":source_path,"usable_variants":len(usable)})

cycle_df=pl.DataFrame(cycles)
cycle_df.write_csv(OUT/"recovered_variant_cycle_manifest.csv")
if frames: pl.concat(frames,how="diagonal").write_parquet(OUT/"recovered_variant_option_bars.parquet",compression="zstd")
Path(OUT/"recovery_provenance.json").write_text(json.dumps({"hf1_main_resolved":hf1_main_sha,"hf1_pinned":HF1_PIN,"hf2_pinned":HF2_PIN,"cycles":prov},indent=2,default=str))
print(json.dumps({"missing_cycles":len(missing),"recovered_usable_variant_cycles":cycle_df.filter(pl.col("status")=="USABLE_OHLC").height,"total_variant_cycles":cycle_df.height,"source_counts":cycle_df.filter(pl.col("status")=="USABLE_OHLC").group_by("recovery_source").len().to_dicts()},indent=2))
