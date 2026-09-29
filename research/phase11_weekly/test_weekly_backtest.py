from weekly_backtest import CostConfig, cost_rupees, entry_cf, lot_size_for_expiry


def test_entry_cashflow():
    assert entry_cf(100.0, 60.0, 40.0, 0.25) == -0.75


def test_lot_size_transition():
    cfg = CostConfig()
    assert lot_size_for_expiry("2025-12-23", cfg) == 75
    assert lot_size_for_expiry("2026-01-06", cfg) == 65


def test_gst_not_applied_to_stt_or_stamp():
    cfg = CostConfig()
    x = cost_rupees(10000.0, 10000.0, 4, cfg)
    brokerage = 40.0
    stt = 10.0
    exchange = 0.69
    sebi = 0.01
    stamp = 0.30
    gst = (brokerage + exchange + sebi) * 0.18
    expected = brokerage + stt + exchange + sebi + stamp + gst
    assert abs(x - expected) < 1e-9


if __name__ == "__main__":
    test_entry_cashflow()
    test_lot_size_transition()
    test_gst_not_applied_to_stt_or_stamp()
    print("Phase 11W unit tests passed.")
