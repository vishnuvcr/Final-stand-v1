"""Phase 9W — Hugging Face weekly NIFTY data ingestion and pilot extraction."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from huggingface_hub import HfApi, hf_hub_download
import polars as pl


DATASET_REPO = "thetrademarkk/india-index-options-1m"
DATASET_TYPE = "dataset"
EXPIRY_RE = re.compile(r"^options/NIFTY/(\d{4}-\d{2}-\d{2})\.parquet$")
IST = ZoneInfo("Asia/Kolkata")


@dataclass
class CycleRecord:
    target_expiry: str
    prior_expiry: str | None
    entry_day: str | None
    entry_timestamp: str
    lock_day: str | None
    lock_timestamp: str
    source_file: str
    source_sha256: str
    entry_spot: float | None
    k1: float | None
    k2: float | None
    k3: float | None
    p1: float | None
    p2: float | None
    target_premium: float | None
    p3: float | None
    target_error: float | None
    entry_quote_complete: bool
    lock_quote_complete: bool
    selected_bar_rows: int
    status: str
    note: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--max-expiries", type=int, default=104)
    p.add_argument("--start-date", default="2024-01-01")
    p.add_argument("--end-date", default="2026-12-31")
    p.add_argument("--output-dir", default="research/phase9_weekly/output")
    p.add_argument("--hf-cache", default="")
    return p.parse_args()


def parse_expiry(path: str) -> date | None:
    m = EXPIRY_RE.match(path)
    return date.fromisoformat(m.group(1)) if m else None


def list_nifty_expiry_files(api: HfApi, revision: str) -> list[tuple[date, str]]:
    out: list[tuple[date, str]] = []
    for item in api.list_repo_tree(
        repo_id=DATASET_REPO,
        repo_type=DATASET_TYPE,
        revision=revision,
        path="options/NIFTY",
        recursive=False,
    ):
        path = getattr(item, "path", None)
        if path:
            d = parse_expiry(path)
            if d is not None:
                out.append((d, path))
    return sorted(out)


def trading_dates(index_df: pl.DataFrame) -> list[date]:
    return (
        index_df
        .select(pl.col("timestamp").dt.date().alias("d"))
        .unique()
        .sort("d")["d"]
        .to_list()
    )


def first_trading_day_after(dates: list[date], prior_expiry: date | None) -> date | None:
    if prior_expiry is None:
        return None
    for d in dates:
        if d > prior_expiry:
            return d
    return None


def prior_trading_day(dates: list[date], expiry: date) -> date | None:
    candidates = [d for d in dates if d < expiry]
    return candidates[-1] if candidates else None


def exact_row(df: pl.DataFrame, ts: datetime) -> pl.DataFrame:
    return df.filter(pl.col("timestamp") == ts)


def close_value(row: pl.DataFrame) -> float | None:
    if row.height != 1:
        return None
    x = row["close"][0]
    return float(x) if x is not None else None


def choose_strikes(entry_calls: pl.DataFrame, spot: float):
    strikes = sorted(float(x) for x in entry_calls["strike"].unique().to_list())
    upper = [k for k in strikes if k > spot]
    if len(upper) < 2:
        return None, None, None, None, None, None, None

    k1, k2 = upper[0], upper[1]
    p1 = close_value(entry_calls.filter(pl.col("strike") == k1))
    p2 = close_value(entry_calls.filter(pl.col("strike") == k2))
    if p1 is None or p2 is None:
        return k1, k2, None, p1, p2, None, None

    d = p1 - p2
    if d <= 0:
        return k1, k2, None, p1, p2, 2.0 * d, None

    target = 2.0 * d
    c = (
        entry_calls
        .filter(pl.col("strike") > k2)
        .with_columns((pl.col("close") - target).abs().alias("distance"))
        .sort(["distance", "strike"])
    )
    if c.height == 0:
        return k1, k2, None, p1, p2, target, None

    k3 = float(c["strike"][0])
    p3 = float(c["close"][0])
    return k1, k2, k3, p1, p2, target, p3


def main() -> None:
    args = parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    token = os.getenv("HF_TOKEN") or None
    revision = os.getenv("HF_REVISION", "main")
    cache_dir = Path(args.hf_cache) if args.hf_cache else None
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)

    api = HfApi(token=token)
    repo_info = api.repo_info(DATASET_REPO, repo_type=DATASET_TYPE, revision=revision)
    resolved_revision = getattr(repo_info, "sha", None) or revision

    all_expiry_files = list_nifty_expiry_files(api, resolved_revision)
    start = date.fromisoformat(args.start_date)
    end = date.fromisoformat(args.end_date)
    window_files = [(d, p) for d, p in all_expiry_files if start <= d <= end]

    if not window_files:
        raise RuntimeError("No NIFTY expiry files matched the requested window.")

    expiry_files = window_files[-args.max_expiries :]
    first_selected_expiry = expiry_files[0][0]
    prior_candidates = [d for d, _ in all_expiry_files if d < first_selected_expiry]
    initial_prior_expiry = prior_candidates[-1] if prior_candidates else None

    index_local = hf_hub_download(
        repo_id=DATASET_REPO,
        filename="index/NIFTY.parquet",
        repo_type=DATASET_TYPE,
        revision=resolved_revision,
        token=token,
        cache_dir=str(cache_dir) if cache_dir else None,
    )
    index_df = pl.read_parquet(index_local).with_columns(
        pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata"))
    )
    dates = trading_dates(index_df)

    manifest = {
        "dataset_repo": DATASET_REPO,
        "dataset_type": DATASET_TYPE,
        "requested_revision": revision,
        "resolved_revision": resolved_revision,
        "token_configured": bool(token),
        "expiry_count": len(expiry_files),
        "expiry_files": [],
        "index_file": {
            "path": "index/NIFTY.parquet",
            "sha256": sha256_file(Path(index_local)),
        },
    }

    cycles: list[CycleRecord] = []
    selected_frames: list[pl.DataFrame] = []
    prior_expiry: date | None = initial_prior_expiry

    for expiry, source_path in expiry_files:
        local = hf_hub_download(
            repo_id=DATASET_REPO,
            filename=source_path,
            repo_type=DATASET_TYPE,
            revision=resolved_revision,
            token=token,
            cache_dir=str(cache_dir) if cache_dir else None,
        )
        source_sha = sha256_file(Path(local))
        manifest["expiry_files"].append(
            {"expiry": expiry.isoformat(), "path": source_path, "sha256": source_sha}
        )

        opt = pl.read_parquet(local).with_columns(
            pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata"))
        )

        entry_day = first_trading_day_after(dates, prior_expiry)
        lock_day = prior_trading_day(dates, expiry)

        if entry_day is None or lock_day is None:
            cycles.append(
                CycleRecord(
                    expiry.isoformat(),
                    prior_expiry.isoformat() if prior_expiry else None,
                    entry_day.isoformat() if entry_day else None,
                    "",
                    lock_day.isoformat() if lock_day else None,
                    "",
                    source_path,
                    source_sha,
                    None, None, None, None, None, None, None, None, None,
                    False, False, 0,
                    "UNUSABLE",
                    "Could not resolve entry or lock session.",
                )
            )
            prior_expiry = expiry
            continue

        entry_ts = datetime.combine(entry_day, datetime.min.time(), IST).replace(hour=10, minute=0)
        lock_ts = datetime.combine(lock_day, datetime.min.time(), IST).replace(hour=14, minute=0)

        spot_row = exact_row(index_df, entry_ts)
        spot = close_value(spot_row)

        entry_calls = opt.filter(
            (pl.col("timestamp") == entry_ts)
            & (pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"]))
        )

        if spot is None or entry_calls.height == 0:
            k1 = k2 = k3 = p1 = p2 = target = p3 = None
        else:
            k1, k2, k3, p1, p2, target, p3 = choose_strikes(entry_calls, spot)

        selected_strikes = [k for k in (k1, k2, k3) if k is not None]
        lock_rows = (
            opt.filter(
                (pl.col("timestamp") == lock_ts)
                & pl.col("strike").is_in(selected_strikes)
                & pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"])
            )
            if selected_strikes else opt.head(0)
        )

        entry_complete = all(x is not None for x in (k1, k2, k3, p1, p2, p3))
        lock_complete = len(selected_strikes) == 3 and lock_rows.height == 3

        target_error = None
        if target is not None and p3 is not None and target > 0:
            target_error = abs(p3 - target) / target

        if selected_strikes:
            chosen = opt.filter(
                pl.col("strike").is_in(selected_strikes)
                & pl.col("option_type").str.to_uppercase().is_in(["CE", "CALL"])
            ).with_columns(
                pl.lit(expiry.isoformat()).alias("target_expiry"),
                pl.lit(entry_ts.isoformat()).alias("entry_timestamp"),
                pl.lit(lock_ts.isoformat()).alias("lock_timestamp"),
            )
            selected_frames.append(chosen)

        cycles.append(
            CycleRecord(
                expiry.isoformat(),
                prior_expiry.isoformat() if prior_expiry else None,
                entry_day.isoformat(),
                entry_ts.isoformat(),
                lock_day.isoformat(),
                lock_ts.isoformat(),
                source_path,
                source_sha,
                spot,
                k1, k2, k3,
                p1, p2, target, p3,
                target_error,
                entry_complete,
                lock_complete,
                lock_rows.height,
                "USABLE_OHLC" if entry_complete and lock_complete else "INCOMPLETE",
                "1-minute OHLC reconstruction; source has no historical bid/ask field.",
            )
        )
        prior_expiry = expiry

    (out / "source_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    pl.DataFrame([asdict(x) for x in cycles]).write_csv(out / "weekly_cycle_manifest.csv")

    if selected_frames:
        pl.concat(selected_frames, how="diagonal").write_parquet(
            out / "selected_weekly_option_bars.parquet", compression="zstd"
        )

    print(json.dumps({
        "resolved_revision": resolved_revision,
        "expiry_count": len(expiry_files),
        "usable_ohlc_cycles": sum(c.status == "USABLE_OHLC" for c in cycles),
        "incomplete_cycles": sum(c.status != "USABLE_OHLC" for c in cycles),
    }, indent=2))


if __name__ == "__main__":
    main()
