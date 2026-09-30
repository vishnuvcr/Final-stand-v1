from __future__ import annotations

import json
import os
from pathlib import Path

import polars as pl

from research.phase17w_strike_alternatives import strike_alternatives as base

K1_RULES = [
    *[f"OTM{i}" for i in range(1, 9)],
    "ATM_NEAREST",
    "ATM_UP",
    *[f"ITM{i}" for i in range(1, 9)],
]
K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
K3_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

VARIANT_IDS = [
    base.make_variant_id(k1, k2, m)
    for k1 in K1_RULES
    for k2 in K2_RULES
    for m in K3_MULTIPLIERS
]

if len(VARIANT_IDS) != 504:
    raise RuntimeError(f"Expected 504 variants, found {len(VARIANT_IDS)}")


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
    raise ValueError(rule)


base.choose_k1 = choose_k1_extended
base.K1_RULES = K1_RULES
base.K2_RULES = K2_RULES
base.K3_MULTIPLIERS = K3_MULTIPLIERS
base.VARIANT_IDS = VARIANT_IDS


def main():
    out = Path("research/phase22b_weekly_504_prospective_freeze/output")
    cache = Path(os.getenv("HF_HOME", ".hf_cache"))
    out.mkdir(parents=True, exist_ok=True)

    start_date = os.getenv("PROSPECTIVE_START", "2026-05-19")
    end_date = os.getenv("PROSPECTIVE_END", "2026-08-04")
    revision = os.getenv("THEMARKET_REVISION", "main")
    max_expiries = int(os.getenv("MAX_EXPIRIES", "32"))

    cycles, option_df, ordered = base.build_variants(
        max_expiries=max_expiries,
        start_date=start_date,
        end_date=end_date,
        cache_dir=cache,
        out_dir=out,
        revision=revision,
        baseline_manifest_path=None,
    )

    if len(ordered) < 8:
        raise RuntimeError(f"Prospective period has only {len(ordered)} weekly expiries; minimum 8 required.")

    if len(VARIANT_IDS) != 504:
        raise RuntimeError("504 registry mutated.")

    registry = {
        "family_size": 504,
        "k1_rules": K1_RULES,
        "k2_rules": K2_RULES,
        "k3_multipliers": K3_MULTIPLIERS,
        "start_date": start_date,
        "end_date": end_date,
        "selected_weekly_expiries": ordered,
        "dataset_repo": base.DATASET_REPO,
        "dataset_type": base.DATASET_TYPE,
        "dataset_revision": revision,
        "weekly_horizon": True,
        "new_holdout": True,
        "opened_after_freeze": True,
    }
    (out / "prospective_registry.json").write_text(json.dumps(registry, indent=2))

    # The prospective period is an untouched holdout. No training/validation
    # selection is performed here; every frozen configuration is evaluated.
    result_df = base.run_variants(
        cycles,
        option_df,
        pl.read_parquet("research/phase9_weekly/output/selected_weekly_spot_bars.parquet"),
        out,
    )

    usable = cycles.filter(pl.col("status") == "USABLE_OHLC")
    coverage = {
        "weekly_expiries": len(ordered),
        "usable_cycle_rows": usable.height,
        "expected_cycle_rows": len(ordered) * 504,
        "all_504_present": usable["variant_id"].n_unique() == 504,
    }
    (out / "coverage.json").write_text(json.dumps(coverage, indent=2))
    print(json.dumps({"registry": registry, "coverage": coverage, "trade_rows": result_df.height}, indent=2))


if __name__ == "__main__":
    main()
