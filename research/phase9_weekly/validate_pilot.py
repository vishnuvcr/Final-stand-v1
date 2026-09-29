"""Phase 9W pilot validation."""

import argparse
from pathlib import Path
from datetime import date

import polars as pl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="research/phase9_weekly/output/weekly_cycle_manifest.csv")
    args = parser.parse_args()

    df = pl.read_csv(Path(args.input))
    total = df.height
    entry_ok = int(df.filter(pl.col("entry_quote_complete") == True).height)
    lock_ok = int(df.filter(pl.col("lock_quote_complete") == True).height)

    if df["target_expiry"].n_unique() != total:
        raise SystemExit("FAIL: duplicate weekly expiry rows.")

    if df["prior_expiry"].is_not_null().any():
        bad_prior = df.filter(
            pl.col("prior_expiry").is_not_null()
            & (pl.col("prior_expiry") >= pl.col("target_expiry"))
        )
        if bad_prior.height:
            raise SystemExit("FAIL: prior weekly expiry is not strictly before target expiry.")

    if df.filter(pl.col("historical_expiry_regime").is_null()).height:
        raise SystemExit("FAIL: missing historical expiry regime.")

    print(f"cycles={total}")
    print(f"entry_complete={entry_ok}")
    print(f"lock_complete={lock_ok}")
    print(f"entry_coverage={entry_ok / total if total else 0.0:.4f}")
    print(f"lock_coverage={lock_ok / total if total else 0.0:.4f}")

    if total < 52:
        raise SystemExit("FAIL: fewer than 52 weekly expiry cycles.")
    if entry_ok / total < 0.95:
        raise SystemExit("FAIL: entry K1/K2/K3 coverage below 95%.")
    if lock_ok / total < 0.95:
        raise SystemExit("FAIL: lock K1/K2/K3 coverage below 95%.")

    print("PASS: Phase 9W weekly OHLC-reconstruction coverage gate met.")


if __name__ == "__main__":
    main()
