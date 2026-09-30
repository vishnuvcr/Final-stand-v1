from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import polars as pl
from huggingface_hub import hf_hub_download

IST = ZoneInfo("Asia/Kolkata")
SPOT_REPO = "thetrademarkk/india-index-options-1m"
SPOT_REVISION = "0f4800e43e6f96cec0794369d78eb4d3c4211ef5"
SPOT_FILE = "index/NIFTY.parquet"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-calendar", required=True)
    ap.add_argument("--hf-cache", default="~/.cache/huggingface")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    import os
    cache = Path(args.hf_cache).expanduser()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    calendar = json.loads(Path(args.baseline_calendar).read_text())
    if len(calendar) != 63:
        raise RuntimeError(f"Expected 63 frozen expiries, got {len(calendar)}")

    token = os.getenv("HF_TOKEN") or None
    local = Path(hf_hub_download(
        repo_id=SPOT_REPO,
        filename=SPOT_FILE,
        repo_type="dataset",
        revision=SPOT_REVISION,
        token=token,
        cache_dir=str(cache),
    ))
    spot = pl.read_parquet(local)
    if spot.schema["timestamp"] == pl.String:
        spot = spot.with_columns(
            pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata").alias("timestamp")
        )
    else:
        spot = spot.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))

    trading_days = sorted(set(ts.date() for ts in spot["timestamp"].to_list()))
    frames = []
    manifest = []

    for i, expiry in enumerate(calendar):
        expiry_date = date.fromisoformat(expiry)
        prior_expiry = calendar[i - 1] if i else None
        prior_date = date.fromisoformat(prior_expiry) if prior_expiry else date.min
        entry_day = next(d for d in trading_days if d > prior_date)
        lock_day = [d for d in trading_days if d < expiry_date][-1]
        entry_ts = datetime.combine(entry_day, time(10, 0), IST)
        lock_ts = datetime.combine(lock_day, time(14, 0), IST)
        part = (
            spot
            .filter((pl.col("timestamp") >= entry_ts) & (pl.col("timestamp") <= lock_ts))
            .with_columns(
                pl.lit(expiry).alias("target_expiry"),
                pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
                pl.lit(lock_ts.isoformat()).alias("lock_timestamp"),
            )
        )
        if part.height == 0:
            raise RuntimeError(f"No spot rows for frozen cycle {expiry}")
        frames.append(part)
        manifest.append({
            "target_expiry": expiry,
            "status": "USABLE_OHLC",
            "prior_expiry": prior_expiry,
            "entry_timestamp": entry_ts.isoformat(),
            "lock_timestamp": lock_ts.isoformat(),
        })

    selected = pl.concat(frames, how="diagonal_relaxed")
    selected.write_parquet(out / "selected_weekly_spot_bars.parquet", compression="zstd")
    pl.DataFrame(manifest).write_csv(out / "weekly_cycle_manifest.csv")
    (out / "spot_source_manifest.json").write_text(json.dumps({
        "repo": SPOT_REPO,
        "revision": SPOT_REVISION,
        "file": SPOT_FILE,
        "sha256": sha256_file(local),
        "cycles": 63,
        "spot_rows": selected.height,
    }, indent=2))
    print(json.dumps({
        "repo": SPOT_REPO,
        "revision": SPOT_REVISION,
        "spot_rows": selected.height,
        "cycles": 63,
    }, indent=2))


if __name__ == "__main__":
    main()
