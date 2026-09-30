from __future__ import annotations

import hashlib
import math
import os
from dataclasses import asdict
from datetime import datetime, date, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import polars as pl
import pyarrow.parquet as pq

from research.phase17w_strike_alternatives import strike_alternatives as base

IST = ZoneInfo("Asia/Kolkata")

K1_RULES = [
    *[f"OTM{i}" for i in range(1, 9)],
    "ATM_NEAREST",
    "ATM_UP",
    *[f"ITM{i}" for i in range(1, 9)],
]
K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
K3_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
VARIANT_IDS = [
    base.make_variant_id(k1, k2, mult)
    for k1 in K1_RULES
    for k2 in K2_RULES
    for mult in K3_MULTIPLIERS
]

THEMARKET_REPO = base.DATASET_REPO
THEMARKET_TYPE = base.DATASET_TYPE
THEMARKET_REVISION = os.getenv("THEMARKET_REVISION", "main")

RISSIN_REPO = "rissin/nse-options-intraday"
RISSIN_TYPE = "dataset"
RISSIN_REVISION = os.getenv(
    "RISSIN_REVISION",
    "8f7739cab3f38abdcbc6332a6d0a83e1341326e3",
)
RISSIN_FILE = "upstox_intraday/NIFTY/NIFTY_2026.parquet"
EXTERNAL_TARGETS = {
    "2026-01-13",
    "2026-02-10",
    "2026-03-10",
    "2026-04-13",
    "2026-05-12",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def choose_k1_extended(strikes, spot, rule):
    s = sorted(set(float(x) for x in strikes))
    if rule.startswith("OTM"):
        n = int(rule[3:])
        candidates = [k for k in s if k > spot]
        return candidates[n - 1] if len(candidates) >= n else None
    if rule.startswith("ITM"):
        n = int(rule[3:])
        candidates = [k for k in s if k < spot]
        return candidates[-n] if len(candidates) >= n else None
    if rule == "ATM_NEAREST":
        return min(s, key=lambda k: (abs(k - spot), -k)) if s else None
    if rule == "ATM_UP":
        candidates = [k for k in s if k >= spot]
        return candidates[0] if candidates else None
    raise ValueError(f"unknown K1 rule: {rule}")


base.choose_k1 = choose_k1_extended
base.K1_RULES = K1_RULES
base.K2_RULES = K2_RULES
base.K3_MULTIPLIERS = K3_MULTIPLIERS
base.VARIANT_IDS = VARIANT_IDS

if len(VARIANT_IDS) != 504:
    raise RuntimeError(f"Expected 504 variants, found {len(VARIANT_IDS)}")


def _normalize_timestamp(df: pl.DataFrame) -> pl.DataFrame:
    dtype = df.schema.get("timestamp")
    if dtype == pl.String:
        return df.with_columns(
            pl.col("timestamp")
            .str.to_datetime(strict=False, time_zone="Asia/Kolkata")
            .alias("timestamp")
        )
    return df.with_columns(
        pl.col("timestamp")
        .cast(pl.Datetime(time_zone="Asia/Kolkata"))
        .alias("timestamp")
    )


def _normalize_option_frame(df: pl.DataFrame, source_name: str, duplicate_key_extra=None) -> pl.DataFrame:
    required = {"timestamp", "open", "strike", "option_type"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise RuntimeError(f"{source_name}: missing required columns {missing}")
    df = _normalize_timestamp(df)
    if "volume" not in df.columns:
        df = df.with_columns(pl.lit(None, dtype=pl.Float64).alias("volume"))
    df = df.filter(
        pl.col("option_type")
        .cast(pl.String)
        .str.to_uppercase()
        .is_in(["CE", "CALL"])
    )
    if "volume" in df.columns:
        df = df.with_columns(pl.col("volume").cast(pl.Float64, strict=False))
    df = df.with_columns(
        pl.col("strike").cast(pl.Float64, strict=False),
        pl.col("open").cast(pl.Float64, strict=False),
    )
    df = df.filter(pl.col("strike").is_not_null() & pl.col("open").is_not_null())
    dup_keys = ["timestamp", "strike", *(duplicate_key_extra or [])]
    dup = (
        df.group_by(dup_keys)
        .len()
        .filter(pl.col("len") > 1)
    )
    if dup.height:
        raise RuntimeError(
            f"{source_name}: duplicate CE observation groups={dup.height}"
        )
    return df


def _load_rissin_targets(cache_dir: Path) -> tuple[pl.DataFrame, str, str]:
    token = os.getenv("HF_TOKEN") or None
    local = Path(
        base.hf_hub_download(
            repo_id=RISSIN_REPO,
            filename=RISSIN_FILE,
            repo_type=RISSIN_TYPE,
            revision=RISSIN_REVISION,
            token=token,
            cache_dir=str(cache_dir),
        )
    )
    sha = sha256_file(local)
    target_cache = cache_dir / "phase22a_rissin_2026_targets.parquet"
    if target_cache.exists():
        cached = pl.read_parquet(target_cache)
        return cached, str(local), sha

    lf = pl.scan_parquet(local)
    schema = lf.collect_schema()
    names = set(schema.names())
    required = {"timestamp", "expiry", "strike", "option_type", "open", "volume"}
    missing = sorted(required - names)
    if missing:
        raise RuntimeError(f"RISSIN source missing columns: {missing}")

    expr = (
        lf.filter(pl.col("underlying") == "NIFTY")
        .filter(pl.col("granularity") == "1min")
        .filter(pl.col("option_type").cast(pl.String).str.to_uppercase().is_in(["CE", "CALL"]))
        .with_columns(pl.col("expiry").cast(pl.String).str.slice(0, 10).alias("_expiry"))
        .filter(pl.col("_expiry").is_in(sorted(EXTERNAL_TARGETS)))
    )
    df = expr.collect(engine="streaming")
    df = _normalize_option_frame(
        df,
        f"{RISSIN_REPO}:{RISSIN_FILE}",
        duplicate_key_extra=["_expiry"],
    )
    df = df.with_columns(pl.col("_expiry").alias("target_expiry"))
    df.write_parquet(target_cache, compression="zstd")
    return df, str(local), sha


def _load_thetrademarkk_expiry(
    source_path: str,
    expected_sha: str,
    cache_dir: Path,
) -> tuple[pl.DataFrame, str]:
    token = os.getenv("HF_TOKEN") or None
    local = Path(
        base.hf_hub_download(
            repo_id=THEMARKET_REPO,
            filename=source_path,
            repo_type=THEMARKET_TYPE,
            revision=THEMARKET_REVISION,
            token=token,
            cache_dir=str(cache_dir),
        )
    )
    sha = sha256_file(local)
    if expected_sha and sha != expected_sha:
        raise RuntimeError(
            f"TheTrademArkk source hash drift for {source_path}: "
            f"expected={expected_sha}, actual={sha}"
        )
    df = pl.read_parquet(local)
    df = _normalize_option_frame(df, source_path)
    return df, sha


def build_variants_504(
    max_expiries,
    start_date,
    end_date,
    cache_dir,
    out_dir,
    revision,
    baseline_manifest_path=None,
    expiry_start=0,
    expiry_end=None,
):
    del max_expiries, start_date, end_date, revision
    cache_dir = Path(cache_dir).expanduser()
    out_dir = Path(out_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    if baseline_manifest_path is None:
        raise RuntimeError("Phase 22A requires the frozen 63-cycle Phase-9 manifest")

    manifest = (
        pl.read_csv(baseline_manifest_path)
        .filter(pl.col("status") == "USABLE_OHLC")
        .sort("target_expiry")
    )
    if manifest.height != 63:
        raise RuntimeError(
            f"Frozen baseline calendar mismatch: expected 63 usable cycles, got {manifest.height}"
        )

    ordered = manifest["target_expiry"].cast(pl.String).to_list()
    wanted = ordered[expiry_start:expiry_end]
    if len(wanted) != 63:
        raise RuntimeError(
            f"Phase 22A must evaluate all 63 frozen weekly expiries, got {len(wanted)}"
        )
    manifest = manifest.filter(pl.col("target_expiry").cast(pl.String).is_in(wanted))

    rissin_df, _, rissin_sha = _load_rissin_targets(cache_dir)

    cycles = []
    raw_parts = []

    for row in manifest.iter_rows(named=True):
        expiry = str(row["target_expiry"])[:10]
        entry_ts = datetime.fromisoformat(str(row["entry_timestamp"]))
        lock_ts = datetime.fromisoformat(str(row["lock_timestamp"]))
        spot = float(row["entry_spot"])
        prior_expiry = (
            str(row["prior_expiry"])[:10]
            if row.get("prior_expiry") is not None
            else None
        )
        regime = (
            str(row["historical_expiry_regime"])
            if row.get("historical_expiry_regime") is not None
            else base.historical_expiry_regime(date.fromisoformat(expiry))
        )

        if expiry in EXTERNAL_TARGETS:
            opt = rissin_df.filter(
                (pl.col("target_expiry") == expiry)
                & (pl.col("timestamp") >= pl.lit(entry_ts))
                & (
                    pl.col("timestamp")
                    <= pl.lit(
                        datetime.combine(
                            date.fromisoformat(expiry),
                            time(16, 0),
                            IST,
                        )
                    )
                )
            )
            source_file = RISSIN_FILE
            source_sha = rissin_sha
        else:
            source_file = str(row["source_file"])
            expected_sha = str(row["source_sha256"])
            opt, source_sha = _load_thetrademarkk_expiry(
                source_file,
                expected_sha,
                cache_dir,
            )
            expiry_end_ts = datetime.combine(
                date.fromisoformat(expiry),
                time(16, 0),
                IST,
            )
            entry_lit = pl.lit(entry_ts).cast(
                pl.Datetime(time_unit="us", time_zone="Asia/Kolkata")
            )
            expiry_end_lit = pl.lit(expiry_end_ts).cast(
                pl.Datetime(time_unit="us", time_zone="Asia/Kolkata")
            )
            opt = opt.filter(
                (pl.col("timestamp") >= entry_lit)
                & (pl.col("timestamp") <= expiry_end_lit)
            )

        entry_lit = pl.lit(entry_ts).cast(
            pl.Datetime(time_unit="us", time_zone="Asia/Kolkata")
        )
        entry_calls = opt.filter(
            (pl.col("timestamp") == entry_lit)
            & (pl.col("volume") > 0)
        )
        strikes = (
            sorted(float(x) for x in entry_calls["strike"].unique().to_list())
            if entry_calls.height
            else []
        )

        usable_specs = []
        for k1_rule in K1_RULES:
            k1 = choose_k1_extended(strikes, spot, k1_rule)
            for k2_rule in K2_RULES:
                k2 = (
                    base.choose_k2(strikes, spot, k1, k2_rule)
                    if k1 is not None
                    else None
                )
                for mult in K3_MULTIPLIERS:
                    variant_id = base.make_variant_id(k1_rule, k2_rule, mult)
                    p1 = p2 = p3 = target = target_error = None
                    k3 = None
                    status = "USABLE_OHLC"

                    if k1 is None or k2 is None:
                        status = "INCOMPLETE"
                    else:
                        r1 = entry_calls.filter(pl.col("strike") == k1)
                        r2 = entry_calls.filter(pl.col("strike") == k2)
                        p1 = float(r1["open"][0]) if r1.height else None
                        p2 = float(r2["open"][0]) if r2.height else None
                        if p1 is None or p2 is None:
                            status = "INCOMPLETE"
                        else:
                            d = p1 - p2
                            if d <= 0:
                                status = "INCOMPLETE_D_NONPOSITIVE"
                            else:
                                target = mult * d
                                k3, p3 = base.select_k3(entry_calls, k2, target)
                                if k3 is None or p3 is None:
                                    status = "INCOMPLETE"
                                else:
                                    target_error = (
                                        abs(p3 - target) / target
                                        if target > 0
                                        else None
                                    )
                                    required_strikes = [k1, k2, k3]
                                    chk = (
                                        opt.filter(
                                            pl.col("strike").is_in(required_strikes)
                                            & pl.col("timestamp").is_in([entry_ts, lock_ts])
                                        )
                                        .select(pl.col("strike").n_unique().alias("n"))
                                    )
                                    n = int(chk["n"][0]) if chk.height else 0
                                    if n != 3:
                                        status = "INCOMPLETE"

                    cycles.append(
                        asdict(
                            base.VariantCycle(
                                variant_id,
                                expiry,
                                prior_expiry,
                                regime,
                                entry_ts.isoformat(),
                                lock_ts.isoformat(),
                                source_file,
                                source_sha,
                                spot,
                                float(k1) if k1 is not None else None,
                                float(k2) if k2 is not None else None,
                                float(k3) if k3 is not None else None,
                                p1,
                                p2,
                                target,
                                mult,
                                p3,
                                target_error,
                                status,
                            )
                        )
                    )

                    if status == "USABLE_OHLC":
                        for strike in (k1, k2, k3):
                            usable_specs.append(
                                {
                                    "variant_id": variant_id,
                                    "strike": float(strike),
                                }
                            )

        if usable_specs:
            strikes_needed = sorted(
                {float(spec["strike"]) for spec in usable_specs}
            )
            # Store each source observation once per expiry/strike. Variant membership
            # remains in the cycle manifest, eliminating a large Cartesian replication
            # of identical OHLC bars across the 504 configurations.
            part = opt.filter(pl.col("strike").is_in(strikes_needed)).with_columns(
                pl.lit(expiry).alias("target_expiry"),
                pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
                pl.lit(lock_ts.isoformat()).alias("lock_timestamp"),
                pl.lit(source_file).alias("source_file"),
                pl.lit(source_sha).alias("source_sha256"),
            )
            raw_parts.append(
                part.select(
                    [
                        "timestamp",
                        "open",
                        "strike",
                        "volume",
                        "target_expiry",
                        "entry_timestamp",
                        "lock_timestamp",
                        "source_file",
                        "source_sha256",
                    ]
                )
            )

    cycle_df = pl.DataFrame(cycles)
    option_df = (
        pl.concat(raw_parts, how="diagonal_relaxed")
        if raw_parts
        else pl.DataFrame(
            schema={
                "timestamp": pl.Datetime(time_zone="Asia/Kolkata"),
                "open": pl.Float64,
                "strike": pl.Float64,
                "volume": pl.Float64,
                "variant_id": pl.String,
                "target_expiry": pl.String,
                "entry_timestamp": pl.String,
                "lock_timestamp": pl.String,
                "source_file": pl.String,
                "source_sha256": pl.String,
            }
        )
    )

    # The custom Phase-22A runner consumes one expiry at a time from this compact
    # shared strike-bar table. Identical source bars are not duplicated per variant;
    # the cycle manifest supplies the variant-to-strike mapping.
    option_path = out_dir / "variant_option_bars.parquet"
    option_df.write_parquet(option_path, compression="zstd")

    cycle_df.write_csv(out_dir / "variant_cycle_manifest.csv")
    (out_dir / "variant_registry.json").write_text(
        __import__("json").dumps(
            {
                "k1_rules": K1_RULES,
                "k2_rules": K2_RULES,
                "k3_multipliers": K3_MULTIPLIERS,
                "variant_ids": VARIANT_IDS,
            },
            indent=2,
        )
    )
    return cycle_df, option_df, ordered


def run_variants_504(
    cycle_df: pl.DataFrame,
    option_source: Path,
    spot_df: pl.DataFrame,
    out_dir: Path,
    variant_subset=None,
):
    cfg = base.CostConfig()
    variants = variant_subset or VARIANT_IDS
    usable = cycle_df.filter(pl.col("status") == "USABLE_OHLC")

    spot_keyed = (
        spot_df
        .sort("timestamp")
        .with_columns(
            pl.col("timestamp").cast(pl.String).str.slice(0, 10).alias("_expiry")
        )
        .group_by("_expiry", maintain_order=True)
        .agg(pl.col("close").last())
    )
    spot_close = {
        str(r["_expiry"]): float(r["close"])
        for r in spot_keyed.iter_rows(named=True)
        if r["close"] is not None
    }

    scan = pl.scan_parquet(str(option_source))
    all_rows = []
    rows_by_variant = {v: [] for v in variants}

    for expiry in sorted(usable["target_expiry"].cast(pl.String).unique().to_list()):
        raw = (
            scan
            .filter(pl.col("target_expiry").cast(pl.String) == expiry)
            .select(["timestamp", "strike", "open"])
            .collect(engine="streaming")
        )
        if raw.height == 0:
            continue

        wide = (
            raw
            .select(["timestamp", "strike", "open"])
            .unique(["timestamp", "strike"], keep="first")
            .with_columns(
                pl.col("timestamp")
                .cast(pl.String)
                .str.replace(r" ", "T")
                .str.slice(0, 19)
            )
            .pivot(
                on="strike",
                index="timestamp",
                values="open",
                aggregate_function="first",
            )
            .sort("timestamp")
        )

        for row in (
            usable.filter(pl.col("target_expiry").cast(pl.String) == expiry)
            .filter(pl.col("variant_id").is_in(variants))
            .iter_rows(named=True)
        ):
            part = raw
            if part.height == 0:
                continue
            result = base._fast_backtest_cycle(
                row,
                part,
                spot_close.get(expiry),
                cfg,
                stop_loss=50.0,
                precomputed_wide=wide,
            )
            if result is None:
                continue
            record = asdict(result)
            record["variant_id"] = row["variant_id"]
            all_rows.append(record)
            rows_by_variant[row["variant_id"]].append(record)

    result_df = pl.DataFrame(all_rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    for variant in variants:
        pl.DataFrame(rows_by_variant.get(variant, [])).write_csv(
            out_dir / f"trades_{variant}.csv"
        )
    result_df.write_csv(out_dir / "all_variant_trades.csv")
    return result_df


base.build_variants = build_variants_504
base.run_variants = run_variants_504

def main() -> None:
    base.main()


if __name__ == "__main__":
    main()
