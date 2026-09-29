"""Cross-check selected NIFTY weekly option bars against a second Hugging Face source."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import polars as pl
from huggingface_hub import hf_hub_download


SECONDARY_REPO = "rissin/nse-options-intraday"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, default=2025)
    p.add_argument(
        "--cycle-manifest",
        default="research/phase9_weekly/output/weekly_cycle_manifest.csv",
    )
    p.add_argument(
        "--output",
        default="research/phase9_weekly/output/source_crosscheck.csv",
    )
    p.add_argument("--hf-cache", default="")
    return p.parse_args()


def normalize_ts(df: pl.DataFrame) -> pl.DataFrame:
    if df.schema["timestamp"] == pl.String:
        df = df.with_columns(
            pl.col("timestamp").str.to_datetime(strict=False).alias("timestamp")
        )
    return df.with_columns(
        pl.col("timestamp").dt.strftime("%Y-%m-%d %H:%M:%S").alias("ts_key")
    )


def main() -> None:
    args = parse_args()
    token = __import__("os").environ.get("HF_TOKEN") or None
    cache_dir = args.hf_cache or None

    cycles = pl.read_csv(Path(args.cycle_manifest))
    cycles = cycles.filter(
        (pl.col("status") == "USABLE_OHLC")
        & pl.col("target_expiry").str.starts_with(str(args.year))
    )

    expected = []
    for row in cycles.iter_rows(named=True):
        expiry = row["target_expiry"]
        for leg in ("k1", "k2", "k3"):
            strike = row[leg]
            if strike is None:
                continue
            for event_name, ts_col in (("entry", "entry_timestamp"), ("lock", "lock_timestamp")):
                expected.append(
                    {
                        "target_expiry": expiry,
                        "ts_key": datetime.fromisoformat(row[ts_col]).strftime("%Y-%m-%d %H:%M:%S"),
                        "leg": leg,
                        "strike": float(strike),
                    }
                )

    exp = pl.DataFrame(expected)
    if exp.height == 0:
        raise SystemExit("No usable cross-check cycles were found for the requested year.")

    local = hf_hub_download(
        repo_id=SECONDARY_REPO,
        filename=f"upstox_intraday/NIFTY/NIFTY_{args.year}.parquet",
        repo_type="dataset",
        token=token,
        cache_dir=cache_dir,
    )
    src = pl.read_parquet(local)
    required = {"timestamp", "expiry", "strike", "option_type", "open"}
    missing = sorted(required.difference(src.columns))
    if missing:
        raise RuntimeError(f"Secondary source missing required columns: {missing}")

    src = normalize_ts(src)
    src = src.with_columns(
        pl.col("expiry").cast(pl.String).alias("target_expiry"),
        pl.col("strike").cast(pl.Float64),
        pl.col("option_type").str.to_uppercase().alias("option_type"),
        pl.col("open").cast(pl.Float64),
    )

    src = src.filter(
        (pl.col("option_type") == "CE")
        & (pl.col("target_expiry").str.starts_with(str(args.year)))
    ).select(
        ["target_expiry", "ts_key", "strike", "open"]
    )

    joined = exp.join(src, on=["target_expiry", "ts_key", "strike"], how="left")
    joined = joined.with_columns(
        pl.when(pl.col("open").is_not_null())
        .then(pl.col("open"))
        .otherwise(None)
        .alias("secondary_open")
    )

    primary = cycles.select(
        [
            "target_expiry",
            "entry_timestamp",
            "lock_timestamp",
            "k1", "p1",
            "k2", "p2",
            "k3", "p3",
        ]
    )

    values = []
    for row in primary.iter_rows(named=True):
        for leg in ("k1", "k2", "k3"):
            strike = row[leg]
            p_entry = row[leg.replace("k", "p")]
            p_lock = row["lock_" + leg.replace("k", "p")]
            if strike is None:
                continue
            for event_name, ts_col, primary_price in (
                ("entry", "entry_timestamp", p_entry),
                ("lock", "lock_timestamp", p_lock),
            ):
                ts_key = datetime.fromisoformat(row[ts_col]).strftime("%Y-%m-%d %H:%M:%S")
                match = joined.filter(
                    (pl.col("target_expiry") == row["target_expiry"])
                    & (pl.col("ts_key") == ts_key)
                    & (pl.col("strike") == float(strike))
                )
                sec = match["secondary_open"][0] if match.height else None
                values.append(
                    {
                        "target_expiry": row["target_expiry"],
                        "event": event_name,
                        "leg": leg,
                        "strike": float(strike),
                        "primary_open": float(primary_price) if primary_price is not None else None,
                        "secondary_open": float(sec) if sec is not None else None,
                        "abs_pct_diff": (
                            abs(float(sec) - float(primary_price)) / abs(float(primary_price))
                            if sec is not None and primary_price not in (None, 0)
                            else None
                        ),
                    }
                )

    result = pl.DataFrame(values)
    result.write_csv(Path(args.output))

    matched = result.filter(pl.col("secondary_open").is_not_null())
    diffs = matched.filter(pl.col("abs_pct_diff").is_not_null())["abs_pct_diff"]
    summary = {
        "year": args.year,
        "cycles": cycles.height,
        "expected_observations": result.height,
        "matched_observations": matched.height,
        "match_rate": matched.height / result.height if result.height else 0.0,
        "mean_abs_pct_diff": float(diffs.mean()) if len(diffs) else None,
        "p95_abs_pct_diff": float(diffs.quantile(0.95)) if len(diffs) else None,
    }
    print(summary)

    if summary["match_rate"] < 0.80:
        raise SystemExit("FAIL: fewer than 80% of cross-check observations matched the secondary source.")


if __name__ == "__main__":
    main()
