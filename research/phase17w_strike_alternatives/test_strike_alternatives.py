from __future__ import annotations

import polars as pl

from research.phase17w_strike_alternatives.strike_alternatives import (
    K3_MULTIPLIERS,
    choose_k1,
    choose_k2,
    make_variant_id,
    variant_ids,
    _fast_backtest_cycle,
)

STRIKES = [24000.0, 24050.0, 24100.0, 24150.0, 24200.0, 24250.0, 24300.0]


def test_registry_size():
    assert len(variant_ids()) == 224
    assert K3_MULTIPLIERS == [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]


def test_baseline():
    assert choose_k1(STRIKES, 24180.0, "OTM1") == 24200.0
    assert choose_k2(STRIKES, 24180.0, 24200.0, "NEXT1") == 24250.0


def test_otm2():
    assert choose_k1(STRIKES, 24180.0, "OTM2") == 24250.0


def test_atm_nearest_tie_prefers_higher():
    assert choose_k1(STRIKES, 24125.0, "ATM_NEAREST") == 24150.0


def test_atm_up_exact_spot():
    assert choose_k1(STRIKES, 24100.0, "ATM_UP") == 24100.0


def test_itm_rules():
    assert choose_k1(STRIKES, 24180.0, "ITM1") == 24150.0
    assert choose_k1(STRIKES, 24180.0, "ITM2") == 24100.0


def test_k2_variants():
    assert choose_k2(STRIKES, 24180.0, 24200.0, "NEXT1") == 24250.0
    assert choose_k2(STRIKES, 24180.0, 24200.0, "NEXT2") == 24300.0


def test_mirror_gap():
    assert choose_k2(STRIKES, 24180.0, 24200.0, "MIRROR_GAP") == 24250.0


def test_ids_are_deterministic():
    ids = variant_ids()
    assert ids[0] == "OTM1_NEXT1_K3M0.5"
    assert ids[-1] == "ITM3_MIRROR_GAP_K3M4"


def test_variant_id_and_baseline_multiplier():
    assert make_variant_id("OTM1", "NEXT1", 2.0) == "OTM1_NEXT1_K3M2"
    assert make_variant_id("ATM_NEAREST", "NEXT2", 1.5) == "ATM_NEAREST_NEXT2_K3M1.5"


def test_fast_backtest_matches_phase11_expiry_semantics():
    from research.phase11_weekly.weekly_backtest import CostConfig, backtest_cycle

    cycle = {
        "status": "USABLE_OHLC",
        "target_expiry": "2026-01-06",
        "entry_timestamp": "2026-01-05T10:00:00+05:30",
        "lock_timestamp": "2026-01-05T14:00:00+05:30",
        "k1": 24200.0,
        "k2": 24250.0,
        "k3": 24300.0,
        "entry_spot": 24180.0,
        "p1": 110.0,
        "p2": 85.0,
        "target_premium": 50.0,
        "target_error": 0.10,
    }
    rows = []
    for ts, vals in [
        ("2026-01-05T10:00:00+05:30", [110.0, 85.0, 50.0]),
        ("2026-01-05T11:00:00+05:30", [108.0, 83.0, 49.0]),
        ("2026-01-05T14:00:00+05:30", [120.0, 70.0, 40.0]),
        ("2026-01-05T15:00:00+05:30", [125.0, 65.0, 35.0]),
    ]:
        for strike, op in zip([24200.0, 24250.0, 24300.0], vals):
            rows.append({"timestamp": ts, "strike": strike, "open": op})
    options = pl.DataFrame(rows)
    spot = pl.DataFrame({"timestamp": ["2026-01-06T15:30:00+05:30"], "close": [24150.0]})
    cfg = CostConfig()
    ref = backtest_cycle(cycle, options, spot, stop_loss=50.0, cfg=cfg)
    fast = _fast_backtest_cycle(cycle, options, 24150.0, cfg, stop_loss=50.0)
    assert ref is not None and fast is not None
    assert ref.exit_reason == fast.exit_reason
    assert ref.orders == fast.orders
    assert abs(ref.gross_points - fast.gross_points) < 1e-9
    assert abs(ref.costs_rupees - fast.costs_rupees) < 1e-9
    assert abs(ref.net_rupees - fast.net_rupees) < 1e-9
