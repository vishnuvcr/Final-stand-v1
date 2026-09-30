from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import polars as pl
from huggingface_hub import hf_hub_download

IST = ZoneInfo("Asia/Kolkata")

RISSIN_REPO = "rissin/nse-options-intraday"
RISSIN_REVISION = "78b1c5468255d18cf492984bfe6fe4e3ac874d7c"
RISSIN_FILE = "upstox_intraday/NIFTY/NIFTY_2026.parquet"

SPOT_REPO = "thetrademarkk/india-index-options-1m"
SPOT_REVISION = "0f4800e43e6f96cec0794369d78eb4d3c4211ef5"
SPOT_FILE = "index/NIFTY.parquet"

TARGETS = [
    "2026-01-13",
    "2026-02-10",
    "2026-03-10",
    "2026-04-13",
    "2026-05-12",
]

K1_RULES = ["OTM1", "OTM2", "OTM3", "ATM_NEAREST", "ATM_UP", "ITM1", "ITM2", "ITM3"]
K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
K3_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
VARIANT_IDS = [
    f"{k1}_{k2}_K3M{m:g}"
    for k1 in K1_RULES
    for k2 in K2_RULES
    for m in K3_MULTIPLIERS
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def choose_k1(strikes: list[float], spot: float, rule: str) -> float | None:
    s = sorted(set(float(x) for x in strikes))
    if rule == "OTM1":
        x = [k for k in s if k > spot]
        return x[0] if x else None
    if rule == "OTM2":
        x = [k for k in s if k > spot]
        return x[1] if len(x) > 1 else None
    if rule == "OTM3":
        x = [k for k in s if k > spot]
        return x[2] if len(x) > 2 else None
    if rule == "ATM_NEAREST":
        return min(s, key=lambda k: (abs(k - spot), -k)) if s else None
    if rule == "ATM_UP":
        x = [k for k in s if k >= spot]
        return x[0] if x else None
    if rule == "ITM1":
        x = [k for k in s if k < spot]
        return x[-1] if x else None
    if rule == "ITM2":
        x = [k for k in s if k < spot]
        return x[-2] if len(x) > 1 else None
    if rule == "ITM3":
        x = [k for k in s if k < spot]
        return x[-3] if len(x) > 2 else None
    raise ValueError(rule)


def choose_k2(strikes: list[float], spot: float, k1: float, rule: str) -> float | None:
    higher = sorted(k for k in set(float(x) for x in strikes) if k > k1)
    if rule in {"NEXT1", "NEXT2", "NEXT3"}:
        idx = {"NEXT1": 0, "NEXT2": 1, "NEXT3": 2}[rule]
        return higher[idx] if len(higher) > idx else None
    if rule == "MIRROR_GAP":
        gap = abs(spot - k1)
        return min(higher, key=lambda k: (abs((k - k1) - gap), k)) if higher else None
    raise ValueError(rule)


def select_k3(entry_calls: pl.DataFrame, k2: float, target: float) -> tuple[float | None, float | None]:
    c = (
        entry_calls
        .filter(pl.col("strike") > k2)
        .with_columns((pl.col("open") - target).abs().alias("_distance"))
        .sort(["_distance", "strike"])
    )
    if c.height == 0:
        return None, None
    return float(c["strike"][0]), float(c["open"][0])


def parse_timestamp(df: pl.DataFrame) -> pl.DataFrame:
    if df.schema["timestamp"] == pl.String:
        return df.with_columns(
            pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata").alias("timestamp")
        )
    return df.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf-cache", default="~/.cache/huggingface")
    ap.add_argument("--baseline-calendar", required=True)
    ap.add_argument("--spot-output", required=True)
    ap.add_argument("--cycle-output", required=True)
    ap.add_argument("--bars-output", required=True)
    ap.add_argument("--source-summary", required=True)
    args = ap.parse_args()

    cache = Path(args.hf_cache).expanduser()
    cache.mkdir(parents=True, exist_ok=True)
    out = Path(args.cycle_output).parent
    out.mkdir(parents=True, exist_ok=True)

    calendar = json.loads(Path(args.baseline_calendar).read_text())
    if len(calendar) != 63:
        raise RuntimeError(f"Expected frozen 63-expiry calendar, got {len(calendar)}")
    if not set(TARGETS).issubset(set(calendar)):
        raise RuntimeError("Recovery targets are not present in the frozen baseline calendar")

    token = None
    import os
    token = os.getenv("HF_TOKEN") or None

    rissin_local = Path(hf_hub_download(
        repo_id=RISSIN_REPO,
        filename=RISSIN_FILE,
        repo_type="dataset",
        revision=RISSIN_REVISION,
        token=token,
        cache_dir=str(cache),
    ))
    rissin_sha = sha256_file(rissin_local)

    spot_local = Path(hf_hub_download(
        repo_id=SPOT_REPO,
        filename=SPOT_FILE,
        repo_type="dataset",
        revision=SPOT_REVISION,
        token=token,
        cache_dir=str(cache),
    ))
    spot_sha = sha256_file(spot_local)

    spot = pl.read_parquet(spot_local)
    spot = parse_timestamp(spot)
    required_spot_cols = {"timestamp", "open", "close"}
    if not required_spot_cols.issubset(set(spot.columns)):
        raise RuntimeError(f"Spot interface missing columns: {sorted(required_spot_cols - set(spot.columns))}")

    trading_days = sorted(set(ts.date() for ts in spot["timestamp"].to_list()))
    source = pl.scan_parquet(rissin_local)
    source_schema = source.collect_schema().names()
    required_source = {"timestamp", "expiry", "strike", "option_type", "open", "volume"}
    missing = sorted(required_source - set(source_schema))
    if missing:
        raise RuntimeError(f"RISSIN source missing columns: {missing}")

    # Keep only the five missing expiries and CE rows. The source is pinned and the
    # filter is executed lazily to avoid materializing the full 2026 archive.
    source = (
        source
        .filter(pl.col("underlying") == "NIFTY")
        .filter(pl.col("granularity") == "1min")
        .filter(pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"]))
        .with_columns(pl.col("expiry").cast(pl.String).str.slice(0, 10).alias("_expiry"))
        .filter(pl.col("_expiry").is_in(TARGETS))
    )
    source = source.with_columns(
        pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata").alias("timestamp")
    )
    source_df = source.collect(streaming=True)

    if source_df.height == 0:
        raise RuntimeError("No RISSIN NIFTY 1-minute CE rows were found for the five targets")

    # Normalize to the frozen bar interface.
    if "oi" in source_df.columns and "open_interest" not in source_df.columns:
        source_df = source_df.rename({"oi": "open_interest"})
    if "open_interest" not in source_df.columns:
        source_df = source_df.with_columns(pl.lit(None, dtype=pl.Float64).alias("open_interest"))
    if "trading_day" not in source_df.columns:
        source_df = source_df.with_columns(pl.col("timestamp").dt.date().cast(pl.String).alias("trading_day"))
    if "symbol" not in source_df.columns:
        source_df = source_df.with_columns(pl.lit("NIFTY").alias("symbol"))

    dup = (
        source_df
        .group_by(["_expiry", "timestamp", "strike", "option_type"])
        .len()
        .filter(pl.col("len") > 1)
    )
    if dup.height:
        raise RuntimeError(f"RISSIN duplicate groups: {dup.height}")

    cycles: list[dict] = []
    selected: list[pl.DataFrame] = []
    target_reports: list[dict] = []

    for expiry in TARGETS:
        idx = calendar.index(expiry)
        prior_expiry = calendar[idx - 1] if idx > 0 else None
        expiry_date = date.fromisoformat(expiry)
        prior_date = date.fromisoformat(prior_expiry) if prior_expiry else date.min
        entry_day = next((d for d in trading_days if d > prior_date), None)
        lock_candidates = [d for d in trading_days if d < expiry_date]
        lock_day = lock_candidates[-1] if lock_candidates else None
        if entry_day is None or lock_day is None:
            raise RuntimeError(f"Could not resolve entry/lock trading days for {expiry}")

        entry_ts = datetime.combine(entry_day, time(10, 0), IST)
        lock_ts = datetime.combine(lock_day, time(14, 0), IST)
        expiry_end = datetime.combine(expiry_date, time(16, 0), IST)

        spot_row = spot.filter(pl.col("timestamp") == entry_ts)
        if spot_row.height != 1:
            raise RuntimeError(f"Expected exactly one NIFTY spot row at {entry_ts}, got {spot_row.height}")
        spot_value = float(spot_row["open"][0])

        opt = source_df.filter(
            (pl.col("_expiry") == expiry)
            & (pl.col("timestamp") >= entry_ts)
            & (pl.col("timestamp") <= expiry_end)
        )
        entry_calls = opt.filter(
            (pl.col("timestamp") == entry_ts) & (pl.col("volume") > 0)
        )
        if entry_calls.height == 0:
            raise RuntimeError(f"No positive-volume CE entry rows for {expiry} at {entry_ts}")

        strikes = sorted(float(x) for x in entry_calls["strike"].unique().to_list())
        usable_count = 0
        expiry_selected: list[pl.DataFrame] = []

        for k1_rule in K1_RULES:
            k1 = choose_k1(strikes, spot_value, k1_rule)
            for k2_rule in K2_RULES:
                for mult in K3_MULTIPLIERS:
                    variant_id = f"{k1_rule}_{k2_rule}_K3M{mult:g}"
                    status = "USABLE_OHLC"
                    p1 = p2 = p3 = target = target_error = None
                    k2 = k3 = None

                    if k1 is None:
                        status = "INCOMPLETE"
                    else:
                        row1 = entry_calls.filter(pl.col("strike") == k1)
                        p1 = float(row1["open"][0]) if row1.height else None
                        k2 = choose_k2(strikes, spot_value, k1, k2_rule)
                        if p1 is None or k2 is None:
                            status = "INCOMPLETE"
                        else:
                            row2 = entry_calls.filter(pl.col("strike") == k2)
                            p2 = float(row2["open"][0]) if row2.height else None
                            if p1 is None or p2 is None or p1 - p2 <= 0:
                                status = "INCOMPLETE_D_NONPOSITIVE"
                            else:
                                target = mult * (p1 - p2)
                                k3, p3 = select_k3(entry_calls, k2, target)
                                if k3 is None or p3 is None:
                                    status = "INCOMPLETE"
                                else:
                                    target_error = abs(p3 - target) / target if target > 0 else None

                    if status == "USABLE_OHLC":
                        required_strikes = [float(k1), float(k2), float(k3)]
                        bars = opt.filter(pl.col("strike").is_in(required_strikes))
                        # All three legs must have exact entry and lock observations.
                        for ts in (entry_ts, lock_ts):
                            check = bars.filter(pl.col("timestamp") == ts).select(
                                pl.col("strike").n_unique().alias("n")
                            )
                            n = int(check["n"][0]) if check.height else 0
                            if n != 3:
                                status = "INCOMPLETE"
                                break
                        if status == "USABLE_OHLC":
                            usable_count += 1
                            expiry_selected.append(
                                bars.with_columns(
                                    pl.lit(variant_id).alias("variant_id"),
                                    pl.lit(expiry).alias("target_expiry"),
                                    pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
                                    pl.lit(lock_ts.isoformat()).alias("lock_timestamp"),
                                    pl.lit(float(mult)).alias("k3_multiplier"),
                                    pl.lit(RISSIN_FILE).alias("source_file"),
                                    pl.lit(rissin_sha).alias("source_sha256"),
                                )
                            )

                    cycles.append({
                        "variant_id": variant_id,
                        "target_expiry": expiry,
                        "prior_expiry": prior_expiry,
                        "entry_timestamp": entry_ts.isoformat(),
                        "lock_timestamp": lock_ts.isoformat(),
                        "entry_spot": spot_value,
                        "k1": k1,
                        "k2": k2,
                        "k3": k3,
                        "p1": p1,
                        "p2": p2,
                        "p3": p3,
                        "target_premium": target,
                        "k3_multiplier": mult,
                        "target_error": target_error,
                        "status": status,
                        "source_file": RISSIN_FILE,
                        "source_sha256": rissin_sha,
                    })

        if usable_count != 224:
            raise RuntimeError(f"{expiry}: only {usable_count}/224 variants passed exact entry/lock coverage")

        target_reports.append({
            "target_expiry": expiry,
            "prior_expiry": prior_expiry,
            "entry_timestamp": entry_ts.isoformat(),
            "lock_timestamp": lock_ts.isoformat(),
            "entry_spot": spot_value,
            "entry_strike_count": len(strikes),
            "source_rows": opt.height,
            "usable_variants": usable_count,
        })
        selected.extend(expiry_selected)

    cycle_df = pl.DataFrame(cycles)
    if cycle_df.height != 224 * len(TARGETS):
        raise RuntimeError(f"Unexpected external cycle count: {cycle_df.height}")

    bars = pl.concat(selected, how="diagonal_relaxed")
    if bars.height == 0:
        raise RuntimeError("No external option bars selected")

    # Keep only the fields needed by the frozen engine plus the frozen metadata.
    keep = [
        "timestamp", "open", "high", "low", "close", "volume",
        "open_interest", "strike", "option_type", "expiry", "trading_day",
        "symbol", "variant_id", "target_expiry", "entry_timestamp",
        "lock_timestamp", "k3_multiplier", "source_file", "source_sha256",
    ]
    for col in keep:
        if col not in bars.columns:
            bars = bars.with_columns(pl.lit(None).alias(col))
    bars = bars.select(keep).sort(["variant_id", "target_expiry", "timestamp", "strike"])

    cycle_df.write_csv(args.cycle_output)
    bars.write_parquet(args.bars_output, compression="zstd")
    spot.write_parquet(args.spot_output, compression="zstd")

    summary = {
        "source": RISSIN_REPO,
        "source_revision": RISSIN_REVISION,
        "source_file": RISSIN_FILE,
        "source_sha256": rissin_sha,
        "spot_source": SPOT_REPO,
        "spot_revision": SPOT_REVISION,
        "spot_file": SPOT_FILE,
        "spot_sha256": spot_sha,
        "targets": target_reports,
        "variant_count": 224,
        "all_targets_224_usable": True,
    }
    Path(args.source_summary).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
