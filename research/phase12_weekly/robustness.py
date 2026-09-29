from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl


def max_drawdown(values):
    x = np.asarray(values, dtype=float)
    if x.size == 0:
        return 0.0
    equity = np.cumsum(x)
    peak = np.maximum.accumulate(equity)
    return float(np.min(equity - peak))


def sharpe_weekly(values):
    x = np.asarray(values, dtype=float)
    if x.size < 2 or np.std(x, ddof=1) == 0:
        return None
    return float(np.mean(x) / np.std(x, ddof=1) * np.sqrt(52.0))


def expected_shortfall(values, alpha=0.95):
    x = np.sort(np.asarray(values, dtype=float))
    if x.size == 0:
        return None
    cutoff = int(np.floor((1.0 - alpha) * x.size))
    cutoff = max(cutoff, 1)
    return float(np.mean(x[:cutoff]))


def block_bootstrap_mean(values, block=4, reps=5000, seed=42):
    x = np.asarray(values, dtype=float)
    if x.size < block:
        return None
    rng = np.random.default_rng(seed)
    means = np.empty(reps)
    n_blocks = int(np.ceil(x.size / block))
    starts = rng.integers(0, x.size - block + 1, size=(reps, n_blocks))
    for i in range(reps):
        sample = np.concatenate([x[s:s + block] for s in starts[i]])[:x.size]
        means[i] = np.mean(sample)
    return {
        "mean": float(np.mean(x)),
        "bootstrap_p05": float(np.quantile(means, 0.05)),
        "bootstrap_p50": float(np.quantile(means, 0.50)),
        "bootstrap_p95": float(np.quantile(means, 0.95)),
        "prob_mean_positive": float(np.mean(means > 0)),
    }


def chronological_split(x, train=0.60, validation=0.20):
    n=len(x)
    a=int(n*train)
    b=a+int(n*validation)
    return x[:a], x[a:b], x[b:]


def analyse(path):
    df=pl.read_csv(path)
    if "net_rupees" not in df.columns:
        raise ValueError(f"Missing net_rupees in {path}")
    x=df.sort("target_expiry")["net_rupees"].to_numpy()
    train, val, test=chronological_split(x)
    return {
        "file": str(path),
        "n": int(len(x)),
        "total_net_rupees": float(np.sum(x)),
        "mean_net_rupees": float(np.mean(x)) if len(x) else None,
        "median_net_rupees": float(np.median(x)) if len(x) else None,
        "mean_net_points": float(np.mean(df.sort("target_expiry")["net_points"].to_numpy())) if "net_points" in df.columns and len(x) else None,
        "median_net_points": float(np.median(df.sort("target_expiry")["net_points"].to_numpy())) if "net_points" in df.columns and len(x) else None,
        "capital_normalization": "NOT_AVAILABLE: historical SPAN/peak-margin series has not yet been integrated; rupee P&L is not a return-on-capital measure.",
        "win_rate": float(np.mean(x>0)) if len(x) else None,
        "max_drawdown_rupees": max_drawdown(x),
        "sharpe_annualized_weekly": sharpe_weekly(x),
        "expected_shortfall_95_rupees": expected_shortfall(x),
        "block_bootstrap_mean": block_bootstrap_mean(x),
        "train": {"n":len(train),"mean":float(np.mean(train)) if len(train) else None},
        "validation": {"n":len(val),"mean":float(np.mean(val)) if len(val) else None},
        "test": {"n":len(test),"mean":float(np.mean(test)) if len(test) else None},
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",default="research/phase12_weekly/input")
    ap.add_argument("--output",default="research/phase12_weekly/robustness.json")
    args=ap.parse_args()

    paths=sorted(Path(args.input_dir).glob("*.csv"))
    if not paths:
        raise SystemExit("No Phase 11 result files found.")

    results=[analyse(p) for p in paths]
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(json.dumps({"files":len(results),"output":str(out)},indent=2))


if __name__=="__main__":
    main()
