from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import polars as pl
from huggingface_hub import HfApi, hf_hub_download

from research.phase9_weekly.hf_weekly_ingest import (
    DATASET_REPO,
    DATASET_TYPE,
    exact_row,
    first_trading_day_after,
    historical_expiry_regime,
    list_nifty_expiry_files,
    monthly_expiry_dates,
    open_value,
    prior_trading_day,
    require_columns,
    trading_dates,
)
from research.phase11_weekly.weekly_backtest import CostConfig, backtest_cycle

IST = ZoneInfo("Asia/Kolkata")
K1_RULES = ["OTM1", "OTM2", "OTM3", "ATM_NEAREST", "ATM_UP", "ITM1", "ITM2", "ITM3"]
K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
VARIANT_IDS = [f"{k1}_{k2}" for k1 in K1_RULES for k2 in K2_RULES]


@dataclass
class VariantCycle:
    variant_id: str
    target_expiry: str
    prior_expiry: str | None
    historical_expiry_regime: str
    entry_timestamp: str
    lock_timestamp: str
    source_file: str
    source_sha256: str
    entry_spot: float | None
    k1: float | None
    k2: float | None
    k3: float | None
    p1: float | None
    p2: float | None
    target_premium: float | None
    p3: float | None
    target_error: float | None
    status: str


def variant_ids() -> list[str]:
    return list(VARIANT_IDS)


def choose_k1(strikes: list[float], spot: float, rule: str) -> float | None:
    s = sorted(set(float(x) for x in strikes))
    if rule == "OTM1":
        candidates = [k for k in s if k > spot]
        return candidates[0] if candidates else None
    if rule == "OTM2":
        candidates = [k for k in s if k > spot]
        return candidates[1] if len(candidates) >= 2 else None
    if rule == "OTM3":
        candidates = [k for k in s if k > spot]
        return candidates[2] if len(candidates) >= 3 else None
    if rule == "ATM_NEAREST":
        return min(s, key=lambda k: (abs(k - spot), -k)) if s else None
    if rule == "ATM_UP":
        candidates = [k for k in s if k >= spot]
        return candidates[0] if candidates else None
    if rule == "ITM1":
        candidates = [k for k in s if k < spot]
        return candidates[-1] if candidates else None
    if rule == "ITM2":
        candidates = [k for k in s if k < spot]
        return candidates[-2] if len(candidates) >= 2 else None
    if rule == "ITM3":
        candidates = [k for k in s if k < spot]
        return candidates[-3] if len(candidates) >= 3 else None
    raise ValueError(f"unknown K1 rule: {rule}")


def choose_k2(strikes: list[float], spot: float, k1: float, rule: str) -> float | None:
    higher = sorted(k for k in set(float(x) for x in strikes) if k > k1)
    if rule in {"NEXT1", "NEXT2", "NEXT3"}:
        idx = {"NEXT1": 0, "NEXT2": 1, "NEXT3": 2}[rule]
        return higher[idx] if len(higher) > idx else None
    if rule == "MIRROR_GAP":
        desired_gap = abs(spot - k1)
        return min(higher, key=lambda k: (abs((k - k1) - desired_gap), k)) if higher else None
    raise ValueError(f"unknown K2 rule: {rule}")


def select_k3(entry_calls: pl.DataFrame, k2: float, target: float) -> tuple[float | None, float | None]:
    candidates = (
        entry_calls
        .filter(pl.col("strike") > k2)
        .with_columns((pl.col("open") - target).abs().alias("distance"))
        .sort(["distance", "strike"])
    )
    if candidates.height == 0:
        return None, None
    return float(candidates["strike"][0]), float(candidates["open"][0])


def centered_block_bootstrap_pvalue(
    values: np.ndarray,
    block_len: int = 3,
    reps: int = 3000,
    seed: int = 1727,
) -> float | None:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < max(8, block_len + 2):
        return None
    centered = x - x.mean()
    blocks = [centered[i : i + block_len] for i in range(n - block_len + 1)]
    if not blocks:
        return None
    rng = np.random.default_rng(seed)
    means = np.empty(reps, dtype=float)
    for r in range(reps):
        pieces = []
        total = 0
        while total < n:
            b = blocks[int(rng.integers(0, len(blocks)))]
            pieces.append(b)
            total += len(b)
        means[r] = np.concatenate(pieces)[:n].mean()
    # Observed mean is the null-boundary; centered bootstrap is used for a one-sided
    # descriptive test of whether the observed mean is unusually large.
    return float((np.count_nonzero(means >= x.mean()) + 1) / (reps + 1))


def holm_adjust(pairs: list[tuple[str, float | None]]) -> dict[str, float | None]:
    valid = [(k, p) for k, p in pairs if p is not None and math.isfinite(p)]
    valid.sort(key=lambda t: t[1])
    out = {k: None for k, _ in pairs}
    previous = 0.0
    m = len(valid)
    for i, (k, p) in enumerate(valid):
        adjusted = min(1.0, (m - i) * p)
        adjusted = max(previous, adjusted)
        previous = adjusted
        out[k] = adjusted
    return out


def metrics(df: pl.DataFrame) -> dict:
    if df.height == 0:
        return {"n": 0}
    x = df["net_rupees"].to_numpy()
    equity = np.cumsum(x)
    drawdown = float(np.min(equity - np.maximum.accumulate(equity)))
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    q = max(1, int(math.floor(0.05 * len(x))))
    return {
        "n": int(len(x)),
        "total_net_rupees": float(np.sum(x)),
        "mean_net_rupees": float(np.mean(x)),
        "median_net_rupees": float(np.median(x)),
        "win_rate": float(np.mean(x > 0)),
        "max_drawdown_rupees": drawdown,
        "expected_shortfall_95_rupees": float(np.mean(np.sort(x)[:q])),
        "annualized_weekly_sharpe": float(np.mean(x) / sd * np.sqrt(52.0)) if sd > 0 else None,
        "mean_cost_rupees": float(df["costs_rupees"].mean()),
    }


def build_variants(
    max_expiries: int,
    start_date: str,
    end_date: str,
    cache_dir: Path,
    out_dir: Path,
    revision: str,
) -> tuple[pl.DataFrame, pl.DataFrame, list[str]]:
    token = os.getenv("HF_TOKEN") or None
    api = HfApi(token=token)
    repo_info = api.repo_info(DATASET_REPO, repo_type=DATASET_TYPE, revision=revision)
    resolved_revision = getattr(repo_info, "sha", None) or revision

    all_files = list_nifty_expiry_files(api, resolved_revision)
    monthly_dates = monthly_expiry_dates(all_files)
    weekly_catalog = [(d, p) for d, p in all_files if d not in monthly_dates]
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    window = [(d, p) for d, p in weekly_catalog if start <= d <= end]
    expiry_files = window[-max_expiries:]
    if not expiry_files:
        raise RuntimeError("No weekly expiry files in requested window.")

    first_expiry = expiry_files[0][0]
    previous = [d for d, _ in weekly_catalog if d < first_expiry]
    prior_expiry = previous[-1] if previous else None

    index_local = hf_hub_download(
        repo_id=DATASET_REPO,
        filename="index/NIFTY.parquet",
        repo_type=DATASET_TYPE,
        revision=resolved_revision,
        token=token,
        cache_dir=str(cache_dir),
    )
    index_df = pl.read_parquet(index_local)
    require_columns(index_df, {"timestamp", "open"}, "NIFTY index file")
    index_df = index_df.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))
    dates = trading_dates(index_df)

    cycles: list[VariantCycle] = []
    selected_rows: list[pl.DataFrame] = []
    baseline_expiries: list[str] = []

    for expiry, source_path in expiry_files:
        local = hf_hub_download(
            repo_id=DATASET_REPO,
            filename=source_path,
            repo_type=DATASET_TYPE,
            revision=resolved_revision,
            token=token,
            cache_dir=str(cache_dir),
        )
        h = hashlib.sha256()
        with open(local, "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
        source_sha = h.hexdigest()

        opt = pl.read_parquet(local)
        require_columns(
            opt,
            {"timestamp", "open", "volume", "strike", "option_type", "expiry"},
            source_path,
        )
        opt = opt.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))

        entry_day = first_trading_day_after(dates, prior_expiry)
        lock_day = prior_trading_day(dates, expiry)
        if entry_day is None or lock_day is None:
            prior_expiry = expiry
            continue

        entry_ts = datetime.combine(entry_day, datetime.min.time(), IST).replace(hour=10, minute=0)
        lock_ts = datetime.combine(lock_day, datetime.min.time(), IST).replace(hour=14, minute=0)
        spot = open_value(exact_row(index_df, entry_ts))

        entry_calls = opt.filter(
            (pl.col("timestamp") == entry_ts)
            & (pl.col("volume") > 0)
            & (pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"]))
        )
        if spot is None or entry_calls.height == 0:
            prior_expiry = expiry
            continue

        spot_float = float(spot)
        strikes = sorted(float(x) for x in entry_calls["strike"].unique().to_list())
        if choose_k1(strikes, spot_float, "OTM1") is not None:
            baseline_expiries.append(expiry.isoformat())

        for k1_rule in K1_RULES:
            k1 = choose_k1(strikes, spot_float, k1_rule)
            for k2_rule in K2_RULES:
                variant_id = f"{k1_rule}_{k2_rule}"
                if k1 is None:
                    cycles.append(
                        VariantCycle(
                            variant_id, expiry.isoformat(),
                            prior_expiry.isoformat() if prior_expiry else None,
                            historical_expiry_regime(expiry),
                            entry_ts.isoformat(), lock_ts.isoformat(), source_path, source_sha,
                            spot_float, None, None, None, None, None, None, None, None,
                            "INCOMPLETE",
                        )
                    )
                    continue

                p1 = open_value(entry_calls.filter(pl.col("strike") == k1))
                k2 = choose_k2(strikes, spot_float, k1, k2_rule)
                if k2 is None:
                    cycles.append(
                        VariantCycle(
                            variant_id, expiry.isoformat(),
                            prior_expiry.isoformat() if prior_expiry else None,
                            historical_expiry_regime(expiry),
                            entry_ts.isoformat(), lock_ts.isoformat(), source_path, source_sha,
                            spot_float, k1, None, None, p1, None, None, None, None,
                            "INCOMPLETE",
                        )
                    )
                    continue

                p2 = open_value(entry_calls.filter(pl.col("strike") == k2))
                if p1 is None or p2 is None:
                    cycles.append(
                        VariantCycle(
                            variant_id, expiry.isoformat(),
                            prior_expiry.isoformat() if prior_expiry else None,
                            historical_expiry_regime(expiry),
                            entry_ts.isoformat(), lock_ts.isoformat(), source_path, source_sha,
                            spot_float, k1, k2, None, p1, p2, None, None, None,
                            "INCOMPLETE",
                        )
                    )
                    continue

                d = float(p1 - p2)
                if d <= 0:
                    cycles.append(
                        VariantCycle(
                            variant_id, expiry.isoformat(),
                            prior_expiry.isoformat() if prior_expiry else None,
                            historical_expiry_regime(expiry),
                            entry_ts.isoformat(), lock_ts.isoformat(), source_path, source_sha,
                            spot_float, k1, k2, None, p1, p2, 2.0 * d, None, None,
                            "INCOMPLETE_D_NONPOSITIVE",
                        )
                    )
                    continue

                target = 2.0 * d
                k3, p3 = select_k3(entry_calls, k2, target)
                status = "USABLE_OHLC" if k3 is not None and p3 is not None else "INCOMPLETE"
                target_error = abs(p3 - target) / target if p3 is not None and target > 0 else None

                cycles.append(
                    VariantCycle(
                        variant_id, expiry.isoformat(),
                        prior_expiry.isoformat() if prior_expiry else None,
                        historical_expiry_regime(expiry),
                        entry_ts.isoformat(), lock_ts.isoformat(), source_path, source_sha,
                        spot_float, k1, k2, k3, p1, p2, target, p3, target_error, status,
                    )
                )

                if status == "USABLE_OHLC":
                    selected_rows.append(
                        opt.filter(
                            pl.col("strike").is_in([k1, k2, k3])
                            & pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"])
                        ).with_columns(
                            pl.lit(variant_id).alias("variant_id"),
                            pl.lit(expiry.isoformat()).alias("target_expiry"),
                            pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
                            pl.lit(lock_ts.isoformat()).alias("lock_timestamp"),
                        )
                    )

        prior_expiry = expiry

    cycle_df = pl.DataFrame([asdict(x) for x in cycles])
    option_df = pl.concat(selected_rows, how="diagonal") if selected_rows else pl.DataFrame()
    out_dir.mkdir(parents=True, exist_ok=True)
    cycle_df.write_csv(out_dir / "variant_cycle_manifest.csv")
    option_df.write_parquet(out_dir / "variant_option_bars.parquet", compression="zstd")
    (out_dir / "baseline_calendar.json").write_text(
        json.dumps(sorted(set(baseline_expiries)), indent=2),
        encoding="utf-8",
    )
    (out_dir / "variant_registry.json").write_text(
        json.dumps({"k1_rules": K1_RULES, "k2_rules": K2_RULES, "variant_ids": VARIANT_IDS}, indent=2),
        encoding="utf-8",
    )
    return cycle_df, option_df, sorted(set(baseline_expiries))


def run_variants(
    cycle_df: pl.DataFrame,
    option_df: pl.DataFrame,
    spot_df: pl.DataFrame,
    out_dir: Path,
) -> pl.DataFrame:
    cfg = CostConfig()
    rows: list[dict] = []
    usable = cycle_df.filter(pl.col("status") == "USABLE_OHLC")

    for variant in VARIANT_IDS:
        cycles = usable.filter(pl.col("variant_id") == variant).sort("target_expiry")
        local_results: list[dict] = []
        for row in cycles.iter_rows(named=True):
            option_slice = option_df.filter(
                (pl.col("variant_id") == variant)
                & (pl.col("target_expiry") == row["target_expiry"])
            )
            if option_slice.height == 0:
                continue
            result = backtest_cycle(row, option_slice, spot_df, stop_loss=50.0, cfg=cfg)
            if result is None:
                continue
            record = asdict(result)
            record["variant_id"] = variant
            local_results.append(record)
            rows.append(record)
        pl.DataFrame(local_results).write_csv(out_dir / f"trades_{variant}.csv")

    result_df = pl.DataFrame(rows)
    result_df.write_csv(out_dir / "all_variant_trades.csv")
    return result_df


def split_cutoffs(baseline_expiries: list[str]) -> tuple[set[str], set[str], set[str]]:
    ordered = sorted(baseline_expiries)
    n = len(ordered)
    train_end = int(n * 0.60)
    val_end = train_end + int(n * 0.20)
    return (
        set(ordered[:train_end]),
        set(ordered[train_end:val_end]),
        set(ordered[val_end:]),
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-expiries", type=int, default=104)
    ap.add_argument("--start-date", default="2024-01-01")
    ap.add_argument("--end-date", default="2026-12-31")
    ap.add_argument("--hf-cache", default=os.path.expanduser("~/.cache/huggingface"))
    ap.add_argument("--output-dir", default="research/phase17w_strike_alternatives/output")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    cache_dir = Path(args.hf_cache)
    out_dir.mkdir(parents=True, exist_ok=True)

    cycle_df, option_df, _ = build_variants(
        args.max_expiries,
        args.start_date,
        args.end_date,
        cache_dir,
        out_dir,
        os.getenv("HF_REVISION", "main"),
    )

    baseline_manifest_path = Path("research/phase9_weekly/output/weekly_cycle_manifest.csv")
    spot_path = Path("research/phase9_weekly/output/selected_weekly_spot_bars.parquet")
    if not spot_path.exists():
        raise RuntimeError("Missing Phase 9 selected spot bars. Build the frozen Phase 9 data interface first.")
    spot_df = pl.read_parquet(spot_path)

    baseline_manifest = pl.read_csv(baseline_manifest_path)
    baseline_expiries = (
        baseline_manifest
        .filter(pl.col("status") == "USABLE_OHLC")
        .sort("target_expiry")["target_expiry"]
        .cast(pl.String)
        .to_list()
    )
    if len(baseline_expiries) != 63:
        raise RuntimeError(
            f"Phase 9 baseline calendar mismatch: expected 63 usable cycles, got {len(baseline_expiries)}"
        )
    (out_dir / "baseline_calendar.json").write_text(
        json.dumps(baseline_expiries, indent=2),
        encoding="utf-8",
    )

    train_set, validation_set, holdout_set = split_cutoffs(baseline_expiries)
    results = run_variants(cycle_df, option_df, spot_df, out_dir)

    rows: list[dict] = []
    pvals: list[tuple[str, float | None]] = []
    split_map = {
        "training": train_set,
        "validation": validation_set,
        "holdout": holdout_set,
    }

    for variant in VARIANT_IDS:
        variant_results = results.filter(pl.col("variant_id") == variant).sort("target_expiry")
        rec: dict = {"variant_id": variant}
        for split_name, expiry_set in split_map.items():
            part = variant_results.filter(pl.col("target_expiry").is_in(sorted(expiry_set)))
            rec[split_name] = metrics(part)

        train_part = variant_results.filter(pl.col("target_expiry").is_in(sorted(train_set)))
        p_value = (
            centered_block_bootstrap_pvalue(train_part["net_rupees"].to_numpy())
            if train_part.height
            else None
        )
        rec["training_bootstrap_p_value"] = p_value
        pvals.append((variant, p_value))

        rec["valid_rate_all_63"] = float(variant_results.height / len(baseline_expiries)) if baseline_expiries else None
        rec["target_error_mean_all"] = (
            float(variant_results["k3_target_error"].mean())
            if variant_results.height and "k3_target_error" in variant_results.columns
            else None
        )
        rec["k1_spot_distance_mean_all"] = (
            float((variant_results["entry_spot"] - variant_results["k1"]).abs().mean())
            if variant_results.height
            else None
        )
        rec["k2_k1_distance_mean_all"] = (
            float((variant_results["k2"] - variant_results["k1"]).mean())
            if variant_results.height
            else None
        )
        rows.append(rec)

    adjusted = holm_adjust(pvals)
    for rec in rows:
        rec["training_holm_adjusted_p"] = adjusted.get(rec["variant_id"])
        tr = rec["training"]
        va = rec["validation"]
        rec["promotable_to_capital_phase"] = bool(
            rec["valid_rate_all_63"] is not None
            and rec["valid_rate_all_63"] >= (50.0 / 63.0)
            and tr.get("n", 0) >= 30
            and tr.get("mean_net_rupees", -math.inf) > 0
            and va.get("n", 0) >= 8
            and va.get("mean_net_rupees", -math.inf) > 0
            and rec["training_holm_adjusted_p"] is not None
            and rec["training_holm_adjusted_p"] < 0.05
        )

    (out_dir / "variant_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "variants": len(rows),
                "baseline_calendar_n": len(baseline_expiries),
                "promotable": [
                    x["variant_id"] for x in rows if x["promotable_to_capital_phase"]
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
