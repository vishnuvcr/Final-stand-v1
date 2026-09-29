from __future__ import annotations

from research.phase17w_strike_alternatives.strike_alternatives import (
    K3_MULTIPLIERS,
    choose_k1,
    choose_k2,
    make_variant_id,
    variant_ids,
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
