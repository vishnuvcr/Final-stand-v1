from weekly_backtest import CostConfig, cost_rates_for_date, cost_rupees, entry_cf, lot_size_for_expiry


def test_entry_cashflow():
    assert entry_cf(100.0, 60.0, 40.0, 0.25) == -0.75


def test_lot_size_transition():
    cfg = CostConfig()
    assert lot_size_for_expiry("2025-12-23", cfg) == 75
    assert lot_size_for_expiry("2026-01-06", cfg) == 65


def test_gst_not_applied_to_stt_or_stamp():
    cfg = CostConfig()
    x = cost_rupees(10000.0, 10000.0, 4, cfg, "2026-09-29")
    brokerage = 40.0
    stt = 10.0
    exchange = 10000.0 * 2 * 0.0003503
    sebi = 10000.0 * 2 * 0.000001
    ipft = 10000.0 * 2 * 0.000005
    stamp = 0.30
    gst = (brokerage + exchange + sebi + ipft) * 0.18
    expected = brokerage + stt + exchange + sebi + ipft + stamp + gst
    assert abs(x - expected) < 1e-9


if __name__ == "__main__":
    test_entry_cashflow()
    test_lot_size_transition()
    test_gst_not_applied_to_stt_or_stamp()
    test_historical_rate_schedule()
    print("Phase 11W unit tests passed.")


def test_historical_rate_schedule():
    cfg = CostConfig()
    assert cost_rates_for_date("2024-09-30", cfg)[:2] == (0.000625, 0.000495)
    assert cost_rates_for_date("2024-10-01", cfg)[:2] == (0.001, 0.0003503)
    assert cost_rates_for_date("2026-04-01", cfg)[:2] == (0.0015, 0.0003503)
