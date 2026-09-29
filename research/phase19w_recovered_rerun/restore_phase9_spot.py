from datetime import date
from pathlib import Path
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

REV=os.getenv("HF_REVISION","0f4800e43e6f96cec0794369d78eb4d3c4211ef5")
CACHE=Path(os.getenv("HF_CACHE","~/.cache/huggingface")).expanduser()
OUT=Path("research/phase9_weekly/output")
EXP=OUT/"weekly_cycle_manifest.csv"
api=HfApi(token=os.getenv("HF_TOKEN") or None)
info=api.repo_info("thetrademarkk/india-index-options-1m",repo_type="dataset",revision=REV)
resolved=getattr(info,"sha",None) or REV
local=hf_hub_download(repo_id="thetrademarkk/india-index-options-1m",filename="index/NIFTY.parquet",repo_type="dataset",revision=resolved,token=os.getenv("HF_TOKEN") or None,cache_dir=str(CACHE))
idx=pl.read_parquet(local).with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))
idx_dates=sorted(set(idx.select(pl.col("timestamp").dt.date()).to_series().to_list()))
exp=pl.read_csv(EXP).filter(pl.col("status")=="USABLE_OHLC").sort("target_expiry")["target_expiry"].to_list()
frames=[]
prev=None
for es in exp:
    ed=date.fromisoformat(es)
    prior=date.fromisoformat(exp[exp.index(es)-1]) if exp.index(es)>0 else None
    if prior is None:
        continue
    entry_days=[d for d in idx_dates if d>prior]
    lock_days=[d for d in idx_dates if d<ed]
    if not entry_days or not lock_days:
        continue
    entry=entry_days[0]; lock=lock_days[-1]
    ist=ZoneInfo("Asia/Kolkata")
    entry_ts=datetime.combine(entry,time(10,0),ist)
    lock_ts=datetime.combine(lock,time(14,0),ist)
    part=idx.filter((pl.col("timestamp")>=entry_ts)&(pl.col("timestamp")<=lock_ts)).with_columns(
        pl.lit(es).alias("target_expiry"),
        pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
        pl.lit(lock_ts.isoformat()).alias("lock_timestamp"))
    if part.height: frames.append(part)
if not frames: raise RuntimeError("No frozen spot slices could be reconstructed.")
pl.concat(frames,how="diagonal").write_parquet(OUT/"selected_weekly_spot_bars.parquet",compression="zstd")
print({"resolved_revision":resolved,"cycles":len(exp),"rows":sum(x.height for x in frames)})
