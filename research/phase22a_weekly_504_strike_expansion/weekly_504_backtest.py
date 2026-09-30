from __future__ import annotations

import sys

from research.phase17w_strike_alternatives import strike_alternatives as base

# Extend only K1. All execution mechanics, cost model, stop logic, split logic,
# K2/K3 definitions and statistical functions remain from the frozen engine.
base.K1_RULES = [
    *[f"OTM{i}" for i in range(1, 9)],
    "ATM_NEAREST",
    "ATM_UP",
    *[f"ITM{i}" for i in range(1, 9)],
]
base.K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
base.K3_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
base.VARIANT_IDS = [
    base.make_variant_id(k1, k2, m)
    for k1 in base.K1_RULES
    for k2 in base.K2_RULES
    for m in base.K3_MULTIPLIERS
]

if len(base.VARIANT_IDS) != 504:
    raise RuntimeError(f"Expected 504 variants, found {len(base.VARIANT_IDS)}")

# Delegate all remaining CLI/data/backtest/statistical behavior to the frozen engine.
sys.argv[0] = "weekly_504_backtest.py"
base.main()