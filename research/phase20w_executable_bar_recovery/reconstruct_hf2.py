from __future__ import annotations
import os,json
from pathlib import Path
import polars as pl
from huggingface_hub import hf_hub_download
OUT=Path("research/phase20w_executable_bar_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
CACHE=os.getenv("HF_CACHE","~/.cache/huggingface"); token=os.getenv("HF_TOKEN")
REV="45e0a043f34f3f40f9694e52a944297803c2af8b"
K1=["OTM1","OTM2","OTM3","ATM_NEAREST","ATM_UP","ITM1","ITM2","ITM3"]; K2=["NEXT1","NEXT2","NEXT3","MIRROR_GAP"]; K3=[0.5,1,1.5,2,2.5,3,4]
base=pl.read_csv("research/phase9_weekly/output/weekly_cycle_manifest.csv").head(63).with_columns(pl.col("target_expiry").cast(pl.String))
trade=pl.read_csv("research/phase19w_recovered_rerun/output/trades_ITM3_NEXT1_K3M4.csv").filter(pl.col("target_expiry").is_in(base["target_expiry"]))
missing=[x for x in base["target_expiry"].to_list() if x not in set(trade["target_expiry"].to_list())]
def k1(s,spot,r):
 s=sorted(set(float(x) for x in s)); gt=[x for x in s if x>spot]; lt=[x for x in s if x<spot]
 return {"OTM1":gt[0] if len(gt)>0 else None,"OTM2":gt[1] if len(gt)>1 else None,"OTM3":gt[2] if len(gt)>2 else None,"ATM_NEAREST":min(s,key=lambda x:(abs(x-spot),-x)) if s else None,"ATM_UP":next((x for x in s if x>=spot),None),"ITM1":lt[-1] if lt else None,"ITM2":lt[-2] if len(lt)>1 else None,"ITM3":lt[-3] if len(lt)>2 else None}[r]
def k2(s,k,r):
 gt=sorted(x for x in set(float(x) for x in s) if k is not None and x>k)
 if r.startswith("NEXT"): return gt[int(r[-1])-1] if len(gt)>=int(r[-1]) else None
 return next((x for x in gt if x>=2*k),gt[-1] if gt else None)
frames=[]; rows=[]
idx_local=hf_hub_download(repo_id="thetrademarkk/india-index-options-1m",filename="index/NIFTY.parquet",repo_type="dataset",revision="0f4800e43e6f96cec0794369d78eb4d3c4211ef5",token=token,cache_dir=CACHE)
idx=pl.read_parquet(idx_local).with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))
idx=idx.with_columns(pl.col("timestamp").dt.strftime("%Y-%m-%dT%H:%M:%S").alias("_its"))
for off in range(-10,11):
 tag="ATM" if off==0 else f"ATM{off:+d}"
 p=f"NIFTY/WEEK/{tag}_CE.parquet"; local=hf_hub_download(repo_id="artist-23/nifty-options-data",filename=p,repo_type="dataset",revision=REV,token=token,cache_dir=CACHE)
 df=pl.read_parquet(local)
 df=df.with_columns((pl.col("datetime")+pl.duration(hours=5,minutes=30)).dt.strftime("%Y-%m-%dT%H:%M:%S").alias("_ts"))
 frames.append(df)
all_df=pl.concat(frames,how="diagonal")
for b in base.iter_rows(named=True):
 exp=str(b["target_expiry"])
 if exp not in missing: continue
 entry=f"{exp}T10:00:00"; lock=f"{exp}T14:00:00"; spot_row=idx.filter(pl.col("_its")==entry); spot=float(spot_row["open"][0]) if spot_row.height else None
 e=all_df.filter((pl.col("_ts")==entry)&(pl.col("option_type")=="CALL"))
 # Build one source-local strike universe at entry; no synthetic strike interpolation.
 strikes=e["strike_price"].cast(pl.Float64).unique().to_list()
 prices={float(x["strike_price"]):float(x["open"]) for x in e.select(["strike_price","open"]).iter_rows(named=True)}
 l=all_df.filter((pl.col("_ts")==lock)&(pl.col("option_type")=="CALL"))
 lockstr=set(l["strike_price"].cast(pl.Float64).to_list())
 for a in K1:
  kk1=k1(strikes,spot,a)
  for bb in K2:
   kk2=k2(strikes,kk1,bb)
   for m in K3:
    vid=f"{a}_{bb}_K3M{m:g}"; target=(prices.get(kk1)-prices.get(kk2))*m if kk1 in prices and kk2 in prices else None
    kk3=None; p3=None
    if target is not None and target>0 and kk2 is not None:
      cand=[s for s in strikes if s>kk2 and s in prices]; kk3=min(cand,key=lambda s:abs(prices[s]-target)) if cand else None; p3=prices.get(kk3)
    status="USABLE_OHLC" if kk3 is not None and all(x in lockstr for x in [kk1,kk2,kk3]) else "INCOMPLETE"
    rows.append({"variant_id":vid,"target_expiry":exp,"entry_timestamp":entry,"lock_timestamp":lock,"entry_spot":spot,"k1":kk1,"k2":kk2,"k3":kk3,"p1":prices.get(kk1),"p2":prices.get(kk2),"target_premium":target,"k3_multiplier":m,"p3":p3,"status":status,"recovery_source":"HF2","recovery_revision":REV})
# Save cycle manifest and exact option bars for required recovered strikes.
r=pl.DataFrame(rows); r.write_csv(OUT/"hf2_recovered_variant_cycles.csv")
req=sorted(set(x for row in rows if row["status"]=="USABLE_OHLC" for x in [row["k1"],row["k2"],row["k3"]] if x is not None))
bars=all_df.filter(pl.col("strike_price").cast(pl.Float64).is_in(req)&pl.col("_ts").is_in([str(x) for x in all_df["_ts"].unique().to_list()])) 
bars.write_parquet(OUT/"hf2_recovered_option_bars.parquet",compression="zstd")
summary=r.group_by("target_expiry").agg(pl.len().alias("variants"),(pl.col("status")=="USABLE_OHLC").sum().alias("usable_variants"))
summary.write_csv(OUT/"hf2_recovered_cycle_summary.csv")
print(json.dumps({"missing_cycles":len(missing),"variant_rows":r.height,"usable_variant_cycles":r.filter(pl.col("status")=="USABLE_OHLC").height,"fully_usable_expiries":summary.filter(pl.col("usable_variants")==224).height},indent=2))
