from __future__ import annotations

import argparse
import itertools
import json
import math
import statistics
from pathlib import Path

import numpy as np
import polars as pl

BOOT_REPS = 5000
BOOT_BLOCK = 4
N_BLOCKS = 6
PURGE_WEEKS = 1
GAP_STRESS_POINTS = [0.0, 5.0, 10.0, 20.0]


def weekly_sharpe(x: np.ndarray) -> float | None:
    if len(x) < 2:
        return None
    sd = float(np.std(x, ddof=1))
    if sd == 0:
        return None
    return float(np.mean(x) / sd * math.sqrt(52.0))


def block_bootstrap(x: np.ndarray, block: int = BOOT_BLOCK, reps: int = BOOT_REPS, seed: int = 42) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if len(x) < block:
        return np.array([], dtype=float)
    rng = np.random.default_rng(seed)
    n_blocks = int(math.ceil(len(x) / block))
    out = np.empty(reps, dtype=float)
    starts = rng.integers(0, len(x) - block + 1, size=(reps, n_blocks))
    for i in range(reps):
        sample = np.concatenate([x[s:s + block] for s in starts[i]])[:len(x)]
        out[i] = float(np.mean(sample))
    return out


def bootstrap_two_sided_p(x: np.ndarray, seed: int) -> float:
    boot = block_bootstrap(x, seed=seed)
    if boot.size == 0:
        return 1.0
    p = 2.0 * min(float(np.mean(boot <= 0.0)), float(np.mean(boot >= 0.0)))
    return float(min(1.0, max(1.0 / BOOT_REPS, p)))


def holm_adjust(pairs: list[tuple[str, float]]) -> dict[str, float]:
    ordered = sorted(pairs, key=lambda z: z[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for rank, (name, p) in enumerate(ordered, start=1):
        value = min(1.0, p * (m - rank + 1))
        running = max(running, value)
        adjusted[name] = running
    return adjusted


def cscv_splits(n: int, n_blocks: int = N_BLOCKS, purge: int = PURGE_WEEKS):
    if n < n_blocks:
        raise ValueError("not enough observations for CSCV blocks")
    edges = np.linspace(0, n, n_blocks + 1, dtype=int)
    blocks = [np.arange(edges[i], edges[i + 1], dtype=int) for i in range(n_blocks)]
    half = n_blocks // 2
    for test_blocks in itertools.combinations(range(n_blocks), half):
        test = np.concatenate([blocks[i] for i in test_blocks])
        mask = np.ones(n, dtype=bool)
        mask[test] = False
        for idx in test:
            lo = max(0, int(idx) - purge)
            hi = min(n, int(idx) + purge + 1)
            mask[lo:hi] = False
        train = np.where(mask)[0]
        yield train, np.sort(test), test_blocks


def cscv_pbo(candidate_arrays: dict[str, np.ndarray]) -> dict:
    names = list(candidate_arrays)
    n = len(next(iter(candidate_arrays.values())))
    rows = []
    for path_id, (train, test, test_blocks) in enumerate(cscv_splits(n), start=1):
        train_means = {name: float(np.mean(arr[train])) for name, arr in candidate_arrays.items()}
        selected = max(names, key=lambda name: (train_means[name], -names.index(name)))
        test_means = {name: float(np.mean(arr[test])) for name, arr in candidate_arrays.items()}
        selected_test = test_means[selected]
        less = sum(v < selected_test for v in test_means.values())
        ties = sum(v == selected_test for v in test_means.values())
        rank_pct = (less + 0.5 * max(0, ties - 1)) / max(1, len(names) - 1)
        bounded = min(1.0 - 1e-12, max(1e-12, rank_pct))
        rows.append({
            "path": path_id,
            "test_blocks": list(test_blocks),
            "selected_training_config": selected,
            "selected_training_mean": train_means[selected],
            "selected_test_mean": selected_test,
            "selected_test_percentile": rank_pct,
            "logit_test_percentile": float(math.log(bounded / (1.0 - bounded))),
        })
    logits = np.array([r["logit_test_percentile"] for r in rows], dtype=float)
    pbo = float(np.mean(logits < 0.0)) if len(logits) else None
    return {
        "n_paths": len(rows),
        "n_candidates": len(names),
        "purge_weeks": PURGE_WEEKS,
        "pbo_proxy": pbo,
        "median_logit_test_percentile": float(np.median(logits)) if len(logits) else None,
        "paths": rows,
        "interpretation": "CSCV-style PBO proxy: fraction of combinatorial paths where the configuration selected by training has below-median test percentile. This is a diagnostic proxy, not a claim of exact reproduction of the published PBO estimator.",
    }


def dsr_style_probability(x: np.ndarray, n_trials: int) -> dict:
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 3:
        return {"probability": None, "weekly_sharpe": None, "annualized_sharpe": None}
    mean = float(np.mean(x))
    sd = float(np.std(x, ddof=1))
    if sd == 0:
        return {"probability": None, "weekly_sharpe": None, "annualized_sharpe": None}
    sr = mean / sd
    z = (x - mean) / sd
    skew = float(np.mean(z ** 3))
    kurtosis = float(np.mean(z ** 4))
    null_max_quantile = statistics.NormalDist().inv_cdf(0.5 ** (1.0 / max(1, n_trials)))
    sr_threshold = null_max_quantile / math.sqrt(n - 1)
    denom_sq = 1.0 - skew * sr + ((kurtosis - 1.0) / 4.0) * (sr ** 2)
    denom = math.sqrt(max(1e-12, denom_sq))
    psr_z = (sr - sr_threshold) * math.sqrt(n - 1) / denom
    probability = statistics.NormalDist().cdf(psr_z)
    return {
        "probability": float(probability),
        "weekly_sharpe": float(sr),
        "annualized_sharpe": float(sr * math.sqrt(52.0)),
        "skewness": skew,
        "kurtosis_raw": kurtosis,
        "trial_count": int(n_trials),
        "null_max_quantile": float(null_max_quantile),
        "weekly_sharpe_threshold": float(sr_threshold),
        "method": "DSR-style approximation using a multiple-testing null Sharpe threshold plus the non-normality-adjusted probabilistic Sharpe ratio; not a byte-for-byte reproduction of the published DSR implementation.",
    }


def group_metrics(df: pl.DataFrame, group_col: str) -> list[dict]:
    out = []
    for key, group in df.group_by(group_col, maintain_order=True):
        name = key[0] if isinstance(key, tuple) else key
        x = group["net_rupees"].to_numpy()
        out.append({
            "group": str(name),
            "n": int(len(x)),
            "mean_net_rupees": float(np.mean(x)) if len(x) else None,
            "median_net_rupees": float(np.median(x)) if len(x) else None,
            "win_rate": float(np.mean(x > 0)) if len(x) else None,
            "annualized_weekly_sharpe": weekly_sharpe(x),
        })
    return out


def add_regime_columns(df: pl.DataFrame) -> pl.DataFrame:
    if "target_expiry" not in df.columns:
        return df
    dates = pl.col("target_expiry").cast(pl.String).str.slice(0, 10).str.to_date()
    df = df.with_columns(dates.alias("expiry_date"))
    df = df.with_columns(
        pl.when(pl.col("expiry_date") < pl.date(2025, 8, 28))
        .then(pl.lit("pre_2025-08-28"))
        .otherwise(pl.lit("post_2025-08-28"))
        .alias("contract_rule_era"),
        pl.when(pl.col("lot_size") >= 75)
        .then(pl.lit("lot_75"))
        .otherwise(pl.lit("lot_65"))
        .alias("lot_regime"),
    )
    if "k3_target_error" in df.columns:
        vals = df["k3_target_error"].to_numpy()
        finite = vals[np.isfinite(vals)]
        if len(finite) >= 3:
            q1, q2 = np.quantile(finite, [1/3, 2/3])
            df = df.with_columns(
                pl.when(pl.col("k3_target_error") <= float(q1)).then(pl.lit("low_target_error"))
                .when(pl.col("k3_target_error") <= float(q2)).then(pl.lit("mid_target_error"))
                .otherwise(pl.lit("high_target_error"))
                .alias("target_error_regime")
            )
    return df


def tail_gap_stress(df: pl.DataFrame) -> list[dict]:
    x = df["net_rupees"].to_numpy().astype(float)
    if "exit_reason" in df.columns:
        stopped = df["exit_reason"].cast(pl.String).str.starts_with("stop").to_numpy()
    else:
        stopped = np.zeros(len(x), dtype=bool)
    lot = df["lot_size"].to_numpy().astype(float) if "lot_size" in df.columns else np.ones(len(x))
    rows = []
    for gap in GAP_STRESS_POINTS:
        adj = x.copy()
        adj[stopped] -= gap * lot[stopped]
        rows.append({
            "additional_gap_points": gap,
            "stopped_trades": int(np.sum(stopped)),
            "mean_net_rupees": float(np.mean(adj)) if len(adj) else None,
            "total_net_rupees": float(np.sum(adj)) if len(adj) else None,
            "win_rate": float(np.mean(adj > 0)) if len(adj) else None,
            "annualized_weekly_sharpe": weekly_sharpe(adj),
        })
    return rows


def parse_candidate_name(path: Path) -> tuple[float | None, float | None]:
    stem = path.stem
    try:
        left, right = stem.split("trades_slip_")[1].split("_stop_")
        slip = float(left)
        stop = None if right == "none" else float(right)
        return slip, stop
    except Exception:
        return None, None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="research/phase12_weekly/input")
    ap.add_argument("--output", default="research/phase12_weekly/robustness_supplement.json")
    args = ap.parse_args()

    paths = sorted(Path(args.input_dir).glob("*.csv"))
    if not paths:
        raise SystemExit("No Phase 12 candidate files found.")

    dataframes: dict[str, pl.DataFrame] = {}
    arrays: dict[str, np.ndarray] = {}
    expiry_keys: tuple[str, ...] | None = None
    for path in paths:
        df = pl.read_csv(path).sort("target_expiry")
        if "net_rupees" not in df.columns:
            raise SystemExit(f"Missing net_rupees in {path}")
        keys = tuple(df["target_expiry"].cast(pl.String).to_list())
        if expiry_keys is None:
            expiry_keys = keys
        elif keys != expiry_keys:
            raise SystemExit("Candidate files do not share identical target_expiry ordering.")
        dataframes[path.name] = df
        arrays[path.name] = df["net_rupees"].to_numpy().astype(float)

    p_pairs = []
    cell_meta = []
    adjusted = {}
    for i, (name, x) in enumerate(arrays.items()):
        p = bootstrap_two_sided_p(x, seed=42 + i)
        p_pairs.append((name, p))
        slip, stop = parse_candidate_name(Path(name))
        cell_meta.append({
            "file": name,
            "slippage_points_per_leg": slip,
            "stop_loss_points": stop,
            "n": int(len(x)),
            "mean_net_rupees": float(np.mean(x)),
            "annualized_weekly_sharpe": weekly_sharpe(x),
            "bootstrap_two_sided_p": p,
        })
    adjusted = holm_adjust(p_pairs)
    for row in cell_meta:
        row["holm_adjusted_p"] = adjusted[row["file"]]

    selected_name = "trades_slip_0.50_stop_50.csv"
    if selected_name not in dataframes:
        raise SystemExit("Frozen Phase 13 cell is missing from Phase 12 candidate grid.")
    selected_df = add_regime_columns(dataframes[selected_name])
    selected_x = selected_df["net_rupees"].to_numpy().astype(float)

    regime = {}
    for col in ["contract_rule_era", "lot_regime", "target_error_regime"]:
        if col in selected_df.columns:
            regime[col] = group_metrics(selected_df, col)

    supplement = {
        "scope": "Supplemental Phase 12 robustness audit after the 30-cell slippage x stop-loss grid.",
        "candidate_cells": len(paths),
        "observations_per_cell": int(len(next(iter(arrays.values())))),
        "multiple_testing": {
            "procedure": "Holm step-down adjustment across all 30 candidate cells.",
            "cells": cell_meta,
        },
        "cscv_pbo": cscv_pbo(arrays),
        "dsr_style": {
            "frozen_phase13_cell": selected_name,
            "result": dsr_style_probability(selected_x, len(paths)),
        },
        "regime_conditioning": regime,
        "tail_gap_stress": tail_gap_stress(selected_df),
        "margin_status": "BLOCKED: historical NSE SPAN/peak-margin series is not yet integrated, so no capital-normalized return is reported.",
        "execution_quality": "OHLC_RECONSTRUCTION: the primary HF dataset does not provide historical bid/ask; these outputs do not establish realized historical fills.",
        "holdout_governance": "The Phase 13 stop was frozen from training only at 0.50-point slippage. This supplemental audit does not change that frozen rule and does not perform any post-holdout parameter search.",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(supplement, indent=2), encoding="utf-8")
    print(json.dumps({"candidate_cells": len(paths), "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()