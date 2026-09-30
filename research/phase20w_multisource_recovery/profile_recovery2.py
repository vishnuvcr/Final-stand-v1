import json, os
from pathlib import Path
import polars as pl
from huggingface_hub import hf_hub_download

REV="45e0a043f34f3f40f9694e52a944297803c2af8b"
ROOT=Path(os.getenv("HF_CACHE","~/.cache/huggingface")).expanduser()
targets=json.loads(Path("research/phase19w_recovered_rerun/output/baseline_calendar.json").read_text())
cov=json.loads(Path("research/phase18w_data_recovery/output/hf03_variant_coverage.json").read_text())
windows={x["target_expiry"]:(x["entry_timestamp"],x["lock_timestamp"]) for x in cov["cycle_results"]}
files=[f"NIFTY/WEEK/{sign}{n}_CE.parquet" for sign in ("ATM+", "ATM-") for n in range(1,11)]
files += ["NIFTY/WEEK/ATM_CE.parquet"]
files += [x.replace("_CE.parquet","_PE.parquet") for x in files]
rows=[]
for fn in files:
    p=hf_hub_download("artist-23/nifty-options-data",filename=fn,revision=REV,repo_type="dataset",token=os.getenv("HF_TOKEN"),cache_dir=str(ROOT))
    df=pl.read_parquet(p)
    cols=set(df.columns)
    ts="datetime" if "datetime" in cols else "timestamp"
    if ts in cols and df.schema[ts] == pl.String:
        df=df.with_columns(pl.col(ts).str.to_datetime(strict=False).alias(ts))
    elif ts in cols:
        df=df.with_columns(pl.col(ts).cast(pl.Datetime(time_zone="Asia/Kolkata"),strict=False).alias(ts))
    expcol="date" if "date" in cols and df.schema["date"] == pl.Date else ("expiry" if "expiry" in cols else None)
    for ex in targets:
        entry,lock=windows[ex]
        if "expiry" in cols:
            part=df.filter(pl.col("expiry").cast(pl.String)==ex)
        else:
            part=df
        if ts in part.columns:
            n=part.filter((pl.col(ts)>=pl.lit(entry).str.to_datetime())&(pl.col(ts)<=pl.lit(lock).str.to_datetime())).height
        else: n=0
        if n: rows.append({"file":fn,"expiry":ex,"rows":n,"columns":sorted(cols)})
out=Path("research/phase20w_multisource_recovery/output"); out.mkdir(parents=True,exist_ok=True)
Path(out/"recovery2_profile.json").write_text(json.dumps({"revision":REV,"files":files,"matches":rows},indent=2))
print(json.dumps({"files":len(files),"matched_file_expiry_pairs":len(rows),"target_expiries_with_any_match":len(set(r["expiry"] for r in rows))},indent=2))
