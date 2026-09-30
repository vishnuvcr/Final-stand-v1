from huggingface_hub import hf_hub_download
import polars as pl, os, json
from pathlib import Path
OUT=Path("research/phase20w_executable_bar_recovery/output"); OUT.mkdir(parents=True,exist_ok=True)
token=os.getenv("HF_TOKEN")
rev="45e0a043f34f3f40f9694e52a944297803c2af8b"
# Missing frozen cycles from the last admitted 63-cycle sample.
missing=["2024-01-04","2024-02-01","2024-02-08","2024-03-07","2024-03-14","2024-04-04","2024-04-10","2024-05-02","2024-05-09","2024-06-06","2024-06-13","2024-07-04","2024-07-11","2024-08-01","2024-08-08","2024-09-05","2024-09-12","2024-10-03","2024-10-10","2024-11-07","2024-11-14","2024-12-05","2024-12-12","2025-01-02","2025-01-09","2025-01-16","2025-01-23","2025-02-06","2025-02-13","2025-02-20","2025-03-06","2025-03-13","2025-04-03","2025-04-09","2025-05-08","2025-05-15","2025-06-05","2025-06-12","2025-07-03","2025-07-10"]
rows=[]
for off in range(-10,11):
    tag="ATM" if off==0 else f"ATM{off:+d}"
    p=f"NIFTY/WEEK/{tag}_CE.parquet"
    local=hf_hub_download(repo_id="artist-23/nifty-options-data",filename=p,repo_type="dataset",revision=rev,token=token,cache_dir=os.getenv("HF_CACHE","~/.cache/huggingface"))
    df=pl.read_parquet(local)
    # epoch is UTC; add 5:30 for IST matching.
    d=df.with_columns((pl.from_epoch(pl.col("timestamp"),time_unit="s")+pl.duration(hours=5,minutes=30)).dt.strftime("%Y-%m-%dT%H:%M:%S").alias("ist"))
    for exp in missing:
        q=d.filter((pl.col("date").cast(pl.String).str.slice(0,10)==exp)&pl.col("ist").is_in([f"{exp}T10:00:00",f"{exp}T14:00:00"]))
        if q.height:
            rows.append({"file":tag,"expiry":exp,"entry_lock_rows":q.height,"strikes":q["strike_price"].n_unique(),"entry_lock_timestamps":"|".join(sorted(map(str,q["ist"].unique().to_list())))})
pl.DataFrame(rows).write_csv(OUT/"hf2_exact_entry_lock_probe.csv")
summary=pl.DataFrame(rows).group_by("expiry").agg(pl.col("entry_lock_rows").sum(),pl.col("strikes").max()).sort("expiry")
summary.write_csv(OUT/"hf2_exact_entry_lock_summary.csv")
print(summary)
