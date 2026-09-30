from __future__ import annotations
import json, os
from pathlib import Path
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

HF_CACHE=Path(os.getenv("HF_CACHE","~/.cache/huggingface")).expanduser()
OUT=Path("research/phase20w_executable_bar_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
HF3="0f4800e43e6f96cec0794369d78eb4d3c4211ef5"
HF1="78b1c5468255d18cf492984bfe6fe4e3ac874d7c"
HF2="45e0a043f34f3f40f9694e52a944297803c2af8b"
repo="vishnuvcr/Final-stand-v1"
# The 27 missing executable cycles are taken from the frozen Phase-19 representative trade file.
trade=pl.read_csv("research/phase19w_recovered_rerun/output/trades_ITM3_NEXT1_K3M4.csv")
cal=json.loads(Path("research/phase19w_recovered_rerun/output/baseline_calendar.json").read_text())
got=set(trade["target_expiry"].cast(pl.String).to_list())
missing=[d for d in cal if d not in got]
# Required variant strikes for the missing cycles.
vc=pl.read_csv("research/phase19w_recovered_rerun/output/variant_cycle_manifest.csv")
print({"variant_cycle_rows":vc.height,"variant_cycle_unique_expiries":vc["target_expiry"].n_unique()})
req=vc.with_columns(pl.col("target_expiry").cast(pl.String)).filter(pl.col("target_expiry").is_in(missing))
api=HfApi(token=os.getenv("HF_TOKEN") or None)
sources={}
# HF-01: Oct-2024 onward 1-minute NIFTY option data plus daily NIFTY spot.
for y in sorted({d[:4] for d in missing if d >= "2024-10-01"}):
    p=f"upstox_intraday/NIFTY/NIFTY_{y}.parquet"
    try:
        local=hf_hub_download(repo_id="rissin/nse-options-intraday",filename=p,repo_type="dataset",revision=HF1,token=os.getenv("HF_TOKEN") or None,cache_dir=str(HF_CACHE))
        df=pl.read_parquet(local)
        sources[f"HF1_{y}"]={"path":p,"rows":df.height,"min_date":str(df["date"].min()),"max_date":str(df["date"].max()),"columns":df.columns}
    except Exception as e:
        sources[f"HF1_{y}"]={"path":p,"error":repr(e)}
# HF-02: compact weekly ATM-relative files; CE only because the frozen strategy uses calls.
for off in range(-10,11):
    tag="ATM" if off==0 else f"ATM{off:+d}"
    p=f"NIFTY/WEEK/{tag}_CE.parquet"
    try:
        local=hf_hub_download(repo_id="artist-23/nifty-options-data",filename=p,repo_type="dataset",revision=HF2,token=os.getenv("HF_TOKEN") or None,cache_dir=str(HF_CACHE))
        df=pl.read_parquet(local)
        sources[f"HF2_{tag}_CE"]={"path":p,"rows":df.height,"columns":df.columns}
    except Exception as e:
        sources[f"HF2_{tag}_CE"]={"path":p,"error":repr(e)}
# Persist the exact missing-cycle inventory and source inventory; no bars are admitted in this step.
Path(OUT/"missing_cycles.json").write_text(json.dumps({"missing_cycles":missing,"count":len(missing)},indent=2))
Path(OUT/"source_inventory.json").write_text(json.dumps({"HF1_revision":HF1,"HF2_revision":HF2,"HF3_revision":HF3,"sources":sources},indent=2,default=str))
req.select(["variant_id","target_expiry","entry_timestamp","lock_timestamp","k1","k2","k3"]).write_csv(OUT/"required_missing_variant_bars.csv")
print(json.dumps({"missing_cycles":len(missing),"required_variant_cycle_rows":req.height,"sources":len(sources)},indent=2))
