from datetime import datetime
from zoneinfo import ZoneInfo

import polars as pl

from hf_weekly_ingest import choose_strikes, historical_expiry_regime, monthly_expiry_dates


IST = ZoneInfo("Asia/Kolkata")


def test_weekly_strike_selection_uses_open_not_close():
    ts = datetime(2025, 1, 7, 10, 0, tzinfo=IST)
    df = pl.DataFrame(
        {
            "timestamp": [ts, ts, ts, ts],
            "strike": [25000.0, 25050.0, 25100.0, 25150.0],
            "option_type": ["CE", "CE", "CE", "CE"],
            "open": [120.0, 80.0, 40.0, 20.0],
            "high": [121.0, 81.0, 41.0, 21.0],
            "low": [119.0, 79.0, 39.0, 19.0],
            "close": [1.0, 2.0, 3.0, 4.0],
            "volume": [100, 100, 100, 100],
        }
    )
    k1, k2, k3, p1, p2, target, p3 = choose_strikes(df, 24990.0)
    assert (k1, k2, k3) == (25000.0, 25050.0, 25100.0)
    assert (p1, p2) == (120.0, 80.0)
    assert target == 80.0
    assert p3 == 40.0


def test_zero_volume_is_not_admitted_to_entry_quotes():
    ts = datetime(2025, 1, 7, 10, 0, tzinfo=IST)
    df = pl.DataFrame(
        {
            "timestamp": [ts, ts, ts],
            "strike": [25000.0, 25050.0, 25100.0],
            "option_type": ["CE", "CE", "CE"],
            "open": [120.0, 80.0, 40.0],
            "high": [121.0, 81.0, 41.0],
            "low": [119.0, 79.0, 39.0],
            "close": [120.0, 80.0, 40.0],
            "volume": [100, 0, 100],
        }
    )
    active = df.filter(pl.col("volume") > 0)
    assert active.height == 2


if __name__ == "__main__":
    test_weekly_strike_selection_uses_open_not_close()
    test_zero_volume_is_not_admitted_to_entry_quotes()
    test_monthly_expiry_is_excluded_from_weekly_catalog()
    test_historical_expiry_regime_boundary()
    print("Phase 9W ingestion helper tests passed.")


def test_monthly_expiry_is_excluded_from_weekly_catalog():
    expiries = [
        (datetime(2025, 1, 2, tzinfo=IST).date(), "a"),
        (datetime(2025, 1, 9, tzinfo=IST).date(), "b"),
        (datetime(2025, 1, 16, tzinfo=IST).date(), "c"),
        (datetime(2025, 1, 23, tzinfo=IST).date(), "d"),
        (datetime(2025, 1, 30, tzinfo=IST).date(), "e"),
    ]
    assert monthly_expiry_dates(expiries) == {datetime(2025, 1, 30, tzinfo=IST).date()}


def test_historical_expiry_regime_boundary():
    assert historical_expiry_regime(datetime(2025, 8, 28, tzinfo=IST).date()) == "THURSDAY_ERA"
    assert historical_expiry_regime(datetime(2025, 9, 2, tzinfo=IST).date()) == "TUESDAY_ERA"


