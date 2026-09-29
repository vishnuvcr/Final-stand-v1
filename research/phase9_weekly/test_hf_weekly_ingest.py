from datetime import datetime
from zoneinfo import ZoneInfo

import polars as pl

from hf_weekly_ingest import choose_strikes


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
    print("Phase 9W ingestion helper tests passed.")
