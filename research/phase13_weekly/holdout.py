from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl

CANDIDATE_STOPS = [25.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0]
SELECTION_SLIPPAGE = 0.50


def split(df: pl.DataFrame):
    x = df.sort("target_expiry")
    n = x.height
    a = int(n * 0.60)
    b = a + int(n * 0.20)
    return x[:a], x[a:b], x[b:]


def metrics(df: pl.DataFrame) -> dict:
    x = df["net_rupees"].to_numpy()
    if len(x) == 0:
        return {"n": 0}
    equity = np.cumsum(x)
    drawdown = float(np.min(equity - np.maximum.accumulate(equity)))
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    sharpe = float(np.mean(x) / sd * np.sqrt(52.0)) if sd > 0 else None
    q = max(1, int(np.floor(0.05 * len(x))))
    es95 = float(np.mean(np.sort(x)[:q]))
    return {
        "n": int(len(x)),
        "total_net_rupees": float(np.sum(x)),
        "mean_net_rupees": float(np.mean(x)),
        "median_net_rupees": float(np.median(x)),
        "win_rate": float(np.mean(x > 0)),
        "max_drawdown_rupees": drawdown,
        "expected_shortfall_95_rupees": es95,
        "annualized_weekly_sharpe": sharpe,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="research/phase13_weekly/input")
    ap.add_argument("--output", default="research/phase13_weekly/holdout.json")
    args = ap.parse_args()

    base = Path(args.input_dir)
    candidates = {}
    for stop in CANDIDATE_STOPS:
        p = base / f"trades_slip_{SELECTION_SLIPPAGE:.2f}_stop_{int(stop)}.csv"
        if not p.exists():
            raise SystemExit(f"Missing candidate: {p}")
        try:
            candidates[stop] = pl.read_csv(p)
        except pl.exceptions.NoDataError:
            raise SystemExit(f"Candidate {p} is empty: upstream backtest produced zero executable trades; diagnose the upstream cycle/quote filter before holdout selection.")

    scored = []
    for stop, df in candidates.items():
        train, _, _ = split(df)
        m = metrics(train)
        scored.append((stop, m["mean_net_rupees"], m["max_drawdown_rupees"]))

    scored.sort(key=lambda z: (-z[1], z[2], z[0]))
    frozen_stop = scored[0][0]

    chosen = candidates[frozen_stop]
    train, validation, holdout = split(chosen)

    result = {
        "selection_slippage_points_per_leg": SELECTION_SLIPPAGE,
        "candidate_stops": CANDIDATE_STOPS,
        "frozen_stop_loss_points": frozen_stop,
        "selection_basis": "training mean net rupees; tie-break lower training max drawdown; then lower stop",
        "training": metrics(train),
        "validation": metrics(validation),
        "untouched_holdout": metrics(holdout),
        "all_periods": metrics(chosen),
        "holdout_used_for_selection": False,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
