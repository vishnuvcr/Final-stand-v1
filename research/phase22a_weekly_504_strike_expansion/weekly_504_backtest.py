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


def choose_k1_extended(strikes, spot, rule):
    s = sorted(set(float(x) for x in strikes))
    if rule.startswith('OTM'):
        n = int(rule[3:])
        candidates = [k for k in s if k > spot]
        return candidates[n - 1] if len(candidates) >= n else None
    if rule.startswith('ITM'):
        n = int(rule[3:])
        candidates = [k for k in s if k < spot]
        return candidates[-n] if len(candidates) >= n else None
    if rule == 'ATM_NEAREST':
        return min(s, key=lambda k: (abs(k - spot), -k)) if s else None
    if rule == 'ATM_UP':
        candidates = [k for k in s if k >= spot]
        return candidates[0] if candidates else None
    raise ValueError(f'unknown K1 rule: {rule}')

base.choose_k1 = choose_k1_extended

if len(base.VARIANT_IDS) != 504:
    raise RuntimeError(f"Expected 504 variants, found {len(base.VARIANT_IDS)}")

# Delegate all remaining CLI/data/backtest/statistical behavior to the frozen engine.
sys.argv[0] = "weekly_504_backtest.py"
base.main()