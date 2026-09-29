"""Phase 9W pilot validation."""

import argparse
from pathlib import Path

import polars as pl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="research/phase9_weekly/output/weekly_cycle_manifest.csv")
    args = parser.parse_args()

    df = pl.read_csv(Path(args.input))
    total = df.height
    entry_ok = int(df.filter(pl.col("entry_quote_complete") == True).height)
    lock_ok = int(df.filter(pl.col("lock_quote_complete") == True).height)

    print(f"cycles={total}")
    print(f"entry_complete={entry_ok}")
    print(f"lock_complete={lock_ok}")

    if total < 52:
        raise SystemExit("FAIL: fewer than 52 expiry cycles.")
    if entry_ok / total < 0.95:
        raise SystemExit("FAIL: entry K1/K2/K3 coverage below 95%.")
    if lock_ok / total < 0.95:
        raise SystemExit("FAIL: lock K1/K2/K3 coverage below 95%.")

    print("PASS: Phase 9W OHLC-reconstruction coverage gate met.")


if __name__ == "__main__":
    main()
