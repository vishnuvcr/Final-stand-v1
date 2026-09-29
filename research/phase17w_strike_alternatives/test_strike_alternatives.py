from __future__ import annotations

from research.phase17w_strike_alternatives.strike_alternatives import (
    choose_k1,
    choose_k2,
    variant_ids,
)

STRIKES = [24000.0, 24050.0, 24100.0, 24150.0, 24200.0, 24250.0, 24300.0]


def test_registry_size():
    assert len(variant_ids()) == 32


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
    assert ids[0] == "OTM1_NEXT1"
    assert ids[-1] == "ITM3_MIRROR_GAP"
