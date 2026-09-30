from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import polars as pl
from huggingface_hub import HfApi, hf_hub_download

from research.phase17w_strike_alternatives import strike_alternatives as base

IST = ZoneInfo("Asia/Kolkata")

K1_RULES = [
    *[f"OTM{i}" for i in range(1, 9)],
    "ATM_NEAREST",
    "ATM_UP",
    *[f"ITM{i}" for i in range(1, 9)],
]
K2_RULES = ["NEXT1", "NEXT2", "NEXT3", "MIRROR_GAP"]
K3_MULTIPLIERS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
VARIANT_IDS = [
    base.make_variant_id(k1, k2, m)
    for k1 in K1_RULES
    for k2 in K2_RULES
    for m in K3_MULTIPLIERS
]
assert len(VARIANT_IDS) == 504 and len(set(VARIANT_IDS)) == 504

RISSIN_REPO = "rissin/nse-options-intraday"
RISSIN_FILE = "upstox_intraday/NIFTY/NIFTY_2026.parquet"
SPOT_REPO = "Jitendra12421/AlargeDatabase"
SPOT_FILE = "INDDEX FILES/NIFTY_minute.parquet"
SPOT_REVISION = os.getenv("SPOT_REVISION", "3420f004d1b4ce56975b06fcd594e0787cd6a83e")
FALLBACK_SPOT_REPO = "technovusin/nifty50-historical-data"
FALLBACK_SPOT_FILE = "1min/2026/NIFTY50_1min_20260101_to_20260908.csv"
FALLBACK_SPOT_REVISION = os.getenv("FALLBACK_SPOT_REVISION", "cd169a991ccfc8979e718ae5ebeb1891a788107d")
TRADEMARKK_REPO = "thetrademarkk/india-index-options-1m"
TRADEMARKK_REVISION = os.getenv("TRADEMARKK_REVISION", "51ca58c")


def choose_k1_extended(strikes, spot, rule):
    s = sorted(set(float(x) for x in strikes))
    if rule.startswith("OTM"):
        n = int(rule[3:])
        c = [k for k in s if k > spot]
        return c[n - 1] if len(c) >= n else None
    if rule.startswith("ITM"):
        n = int(rule[3:])
        c = [k for k in s if k < spot]
        return c[-n] if len(c) >= n else None
    if rule == "ATM_NEAREST":
        return min(s, key=lambda k: (abs(k - spot), -k)) if s else None
    if rule == "ATM_UP":
        c = [k for k in s if k >= spot]
        return c[0] if c else None
    raise ValueError(rule)


base.choose_k1 = choose_k1_extended
base.K1_RULES = K1_RULES
base.K2_RULES = K2_RULES
base.K3_MULTIPLIERS = K3_MULTIPLIERS
base.VARIANT_IDS = VARIANT_IDS


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ts_lit(dt: datetime):
    return pl.lit(dt).cast(pl.Datetime(time_unit="us", time_zone="Asia/Kolkata"))


def build_prospective_data(out: Path, cache: Path, start_date: str, end_date: str):
    token = os.getenv("HF_TOKEN") or None
    rissin_revision = os.getenv("RISSIN_REVISION", "main")

    rpath = Path(hf_hub_download(
        repo_id=RISSIN_REPO,
        filename=RISSIN_FILE,
        repo_type="dataset",
        revision=rissin_revision,
        token=token,
        cache_dir=str(cache),
    ))
    spath = Path(hf_hub_download(
        repo_id=SPOT_REPO,
        filename=SPOT_FILE,
        repo_type="dataset",
        revision=SPOT_REVISION,
        token=token,
        cache_dir=str(cache),
    ))

    # Resolve immutable source revision IDs for provenance.
    api = HfApi(token=token)
    rinfo = api.repo_info(RISSIN_REPO, repo_type="dataset", revision=rissin_revision)
    resolved_r = getattr(rinfo, "sha", None) or rissin_revision

    idx = pl.read_parquet(spath)
    if "symbol" in idx.columns:
        idx = idx.filter(pl.col("symbol").cast(pl.String).str.to_uppercase().is_in(["NIFTY", "NIFTY_50", "NIFTY50"]))
    if "timestamp" not in idx.columns and "date" in idx.columns:
        idx = idx.rename({"date": "timestamp"})
    if "timestamp" not in idx.columns:
        raise RuntimeError(f"Spot source columns: {idx.columns}")
    ts_dtype = idx.schema["timestamp"]
    if getattr(ts_dtype, "time_zone", None):
        idx = idx.with_columns(pl.col("timestamp").dt.convert_time_zone("Asia/Kolkata"))
    elif ts_dtype == pl.String:
        idx = idx.with_columns(pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata"))
    else:
        idx = idx.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))
    if "open" not in idx.columns or "close" not in idx.columns:
        raise RuntimeError(f"Spot source missing open/close columns: {idx.columns}")
    dates = idx.select(pl.col("timestamp").dt.date().alias("d")).unique().sort("d")["d"].to_list()

    fallback_path = Path(os.path.expanduser(str(cache))) / "technovusin_nifty50_2026_1min.csv"
    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    fallback_used = False
    fallback_sha256 = None
    option_fallback_expiries = []
    option_fallback_sha256 = {}

    lf = pl.scan_parquet(rpath)
    schema = lf.collect_schema()
    required = {"timestamp", "expiry", "strike", "option_type", "open", "volume", "underlying", "granularity"}
    missing = sorted(required - set(schema.names()))
    if missing:
        raise RuntimeError(f"RISSIN source missing columns: {missing}")

    # Discover target expiries from the primary RISSIN source and a gap-only
    # TradeMarkk expiry-file catalog. The latter is used only to recover
    # expiry files absent from RISSIN; it does not replace RISSIN rows.
    discovery = (
        lf.filter(pl.col("underlying") == "NIFTY")
        .filter(pl.col("granularity") == "1min")
        .with_columns(pl.col("expiry").cast(pl.String).str.slice(0, 10).alias("_expiry"))
        .filter((pl.col("_expiry") >= start_date) & (pl.col("_expiry") <= end_date))
        .select("_expiry")
        .unique()
        .collect(engine="streaming")
    )
    rissin_expiries = sorted(str(x) for x in discovery["_expiry"].to_list())
    tm_files = api.list_repo_files(repo_id=TRADEMARKK_REPO, repo_type="dataset", revision=TRADEMARKK_REVISION)
    tm_expiries = sorted(
        p.rsplit("/", 1)[-1].removesuffix(".parquet")
        for p in tm_files
        if p.startswith("options/NIFTY/") and p.endswith(".parquet")
        and start_date <= p.rsplit("/", 1)[-1].removesuffix(".parquet") <= end_date
    )
    all_expiries = sorted(set(rissin_expiries) | set(tm_expiries))
    latest_by_month = {}
    for e in all_expiries:
        key = e[:7]
        latest_by_month[key] = max(e, latest_by_month.get(key, e))
    monthly = set(latest_by_month.values())
    targets = [e for e in all_expiries if e not in monthly]
    if len(targets) < 7:
        raise RuntimeError(f"Only {len(targets)} weekly expiries admitted from primary/fallback sources in {start_date}..{end_date}: {targets}")

    target_dates = [date.fromisoformat(x) for x in targets]

    def weekly_prior_expiry(d):
        # NIFTY weekly expiry is Tuesday in this period. Use the exchange-calendar
        # date relation rather than source-file availability, so missing source
        # files cannot shift the entry week backward.
        return d - timedelta(days=7)

    def first_trading_day_after(d):
        return next((x for x in dates if x > d), None)

    def prior_trading_day(d):
        c = [x for x in dates if x < d]
        return c[-1] if c else None

    cycles = []
    raw_parts = []

    for expiry in target_dates:
        prior = weekly_prior_expiry(expiry)
        entry_day = first_trading_day_after(prior)
        lock_day = prior_trading_day(expiry)
        if entry_day is None or lock_day is None:
            raise RuntimeError(f"Cannot establish entry/lock trading days for {expiry}")
        entry_ts = datetime.combine(entry_day, time(10, 0), IST)
        lock_ts = datetime.combine(lock_day, time(14, 0), IST)

        # Causal spot selection: exact 10:00 if available; otherwise use the
        # latest minute at or before 10:00 within a fixed five-minute tolerance.
        # No future observation is allowed to determine the entry strikes.
        spot_row = (
            idx.filter(pl.col("timestamp") <= ts_lit(entry_ts))
            .filter(pl.col("timestamp") >= ts_lit(entry_ts - timedelta(minutes=5)))
            .sort("timestamp", descending=True)
            .head(1)
        )
        if spot_row.height != 1:
            import urllib.request
            if not fallback_path.exists():
                url = f"https://raw.githubusercontent.com/{FALLBACK_SPOT_REPO}/{FALLBACK_SPOT_REVISION}/{FALLBACK_SPOT_FILE}"
                urllib.request.urlretrieve(url, fallback_path)
            fallback_sha256 = sha256(fallback_path)
            fidx = pl.read_csv(
                fallback_path,
                columns=["Timestamp", "Open"],
                try_parse_dates=False,
            ).rename({"Timestamp": "timestamp", "Open": "open"})
            fidx = fidx.with_columns(
                pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata"),
                pl.col("open").cast(pl.Float64, strict=False),
            ).filter(pl.col("timestamp").is_not_null() & pl.col("open").is_not_null())
            spot_row = (
                fidx.filter(pl.col("timestamp") <= ts_lit(entry_ts))
                .filter(pl.col("timestamp") >= ts_lit(entry_ts - timedelta(minutes=5)))
                .sort("timestamp", descending=True)
                .head(1)
            )
            if spot_row.height == 1:
                fallback_used = True
            else:
                raise RuntimeError(f"No causal NIFTY spot row in either pinned primary or fallback archive within 5 minutes before {entry_ts} for {expiry}")
        spot = float(spot_row["open"][0])

        end_ts = datetime.combine(expiry, time(16, 0), IST)
        opt = (
            lf.filter(pl.col("underlying") == "NIFTY")
            .filter(pl.col("granularity") == "1min")
            .filter(pl.col("expiry").cast(pl.String).str.slice(0, 10) == expiry.isoformat())
            .filter(pl.col("option_type").cast(pl.String).str.to_uppercase().is_in(["CE", "CALL"]))
            # Filter the annual RISSIN file by its canonical trading-date string
            # before materializing; timestamp timezone normalization is performed
            # after collection to avoid Polars timezone-literal coercion.
            .filter(pl.col("date").cast(pl.String).str.slice(0, 10) >= entry_day.isoformat())
            .filter(pl.col("date").cast(pl.String).str.slice(0, 10) <= expiry.isoformat())
            .select(["timestamp", "strike", "open", "volume"])
            .collect(engine="streaming")
            .with_columns(
                pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")),
                pl.col("strike").cast(pl.Float64, strict=False),
                pl.col("open").cast(pl.Float64, strict=False),
                pl.col("volume").cast(pl.Float64, strict=False),
            )
            .filter(pl.col("strike").is_not_null() & pl.col("open").is_not_null())
        )
        if opt.height == 0 and expiry.isoformat() in tm_expiries:
            tm_path = Path(hf_hub_download(
                repo_id=TRADEMARKK_REPO,
                filename=f"options/NIFTY/{expiry.isoformat()}.parquet",
                repo_type="dataset",
                revision=TRADEMARKK_REVISION,
                token=token,
                cache_dir=str(cache),
            ))
            tm = pl.read_parquet(tm_path)
            required_tm = {"timestamp", "strike", "open", "volume", "option_type"}
            missing_tm = sorted(required_tm - set(tm.columns))
            if missing_tm:
                raise RuntimeError(f"TradeMarkk fallback missing columns for {expiry}: {missing_tm}")
            opt = (
                tm.filter(pl.col("option_type").cast(pl.String).str.to_uppercase().is_in(["CE", "CALL"]))
                .select(["timestamp", "strike", "open", "volume"])
                .with_columns(
                    pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")),
                    pl.col("strike").cast(pl.Float64, strict=False),
                    pl.col("open").cast(pl.Float64, strict=False),
                    pl.col("volume").cast(pl.Float64, strict=False),
                )
                .filter(pl.col("timestamp") >= ts_lit(datetime.combine(entry_day, time(9, 0), IST)))
                .filter(pl.col("timestamp") <= ts_lit(datetime.combine(expiry, time(16, 0), IST)))
                .filter(pl.col("strike").is_not_null() & pl.col("open").is_not_null())
            )
            if opt.height:
                option_fallback_expiries.append(expiry.isoformat())
                option_fallback_sha256[expiry.isoformat()] = sha256(tm_path)

        entry_calls = opt.filter((pl.col("timestamp") == ts_lit(entry_ts)) & (pl.col("volume") > 0))
        strikes = sorted(float(x) for x in entry_calls["strike"].unique().to_list())
        if not strikes:
            raise RuntimeError(f"No entry CE strikes at {entry_ts} for {expiry}")

        regime = base.historical_expiry_regime(expiry)

        for k1_rule in K1_RULES:
            k1 = choose_k1_extended(strikes, spot, k1_rule)
            for k2_rule in K2_RULES:
                k2 = base.choose_k2(strikes, spot, k1, k2_rule) if k1 is not None else None
                for mult in K3_MULTIPLIERS:
                    vid = base.make_variant_id(k1_rule, k2_rule, mult)
                    status = "USABLE_OHLC"
                    k3 = p1 = p2 = target = p3 = target_error = None
                    if k1 is None or k2 is None:
                        status = "INCOMPLETE"
                    else:
                        r1 = entry_calls.filter(pl.col("strike") == k1)
                        r2 = entry_calls.filter(pl.col("strike") == k2)
                        if r1.height == 0 or r2.height == 0:
                            status = "INCOMPLETE"
                        else:
                            p1 = float(r1["open"][0]); p2 = float(r2["open"][0])
                            d = p1 - p2
                            if d <= 0:
                                status = "INCOMPLETE_D_NONPOSITIVE"
                            else:
                                target = mult * d
                                k3, p3 = base.select_k3(entry_calls, k2, target)
                                if k3 is None:
                                    status = "INCOMPLETE"
                                else:
                                    target_error = abs(p3 - target) / target if target > 0 else None
                                    present = opt.filter(
                                        pl.col("strike").is_in([k1, k2, k3])
                                        & (
                                            (pl.col("timestamp") == ts_lit(entry_ts))
                                            | (pl.col("timestamp") == ts_lit(lock_ts))
                                        )
                                    )["strike"].n_unique()
                                    if int(present) != 3:
                                        status = "INCOMPLETE"
                    cycles.append({
                        "variant_id": vid,
                        "target_expiry": expiry.isoformat(),
                        "prior_expiry": prior.isoformat(),
                        "historical_expiry_regime": regime,
                        "entry_timestamp": entry_ts.isoformat(),
                        "lock_timestamp": lock_ts.isoformat(),
                        "source_file": RISSIN_FILE,
                        "source_sha256": sha256(rpath),
                        "entry_spot": spot,
                        "k1": k1, "k2": k2, "k3": k3,
                        "p1": p1, "p2": p2,
                        "target_premium": target,
                        "k3_multiplier": mult, "p3": p3,
                        "target_error": target_error, "status": status,
                    })
        raw_parts.append(
            opt.with_columns(pl.lit(expiry.isoformat()).alias("target_expiry"))
        )

    cycle_df = pl.DataFrame(cycles)
    option_df = pl.concat(raw_parts, how="diagonal_relaxed")
    cycle_df.write_csv(out / "variant_cycle_manifest.csv")
    option_df.write_parquet(out / "prospective_option_bars.parquet", compression="zstd")

    manifest = {
        "rissin_repo": RISSIN_REPO,
        "rissin_file": RISSIN_FILE,
        "rissin_requested_revision": rissin_revision,
        "rissin_resolved_revision": resolved_r,
        "rissin_sha256": sha256(rpath),
        "spot_repo": SPOT_REPO,
        "spot_file": SPOT_FILE,
        "spot_revision": SPOT_REVISION,
        "spot_sha256": sha256(spath),
        "fallback_spot_repo": FALLBACK_SPOT_REPO,
        "fallback_spot_file": FALLBACK_SPOT_FILE,
        "fallback_spot_revision": FALLBACK_SPOT_REVISION,
        "fallback_spot_sha256": fallback_sha256,
        "fallback_spot_used": fallback_used,
        "trademarkk_repo": TRADEMARKK_REPO,
        "trademarkk_revision": TRADEMARKK_REVISION,
        "option_fallback_expiries": option_fallback_expiries,
        "option_fallback_sha256": option_fallback_sha256,
        "requested_start": start_date,
        "requested_end": end_date,
        "weekly_expiries": targets,
        "monthly_expiries_excluded": sorted(monthly),
    }
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2))
    return cycle_df, option_df, targets


def run_all(cycles: pl.DataFrame, options: pl.DataFrame, spot_df: pl.DataFrame, out: Path):
    cfg = base.CostConfig()
    usable = cycles.filter(pl.col("status") == "USABLE_OHLC")
    spot_keyed = (
        spot_df.sort("timestamp")
        .with_columns(pl.col("timestamp").cast(pl.String).str.slice(0, 10).alias("_date"))
        .group_by("_date", maintain_order=True).agg(pl.col("close").last())
    )
    spot_close = {str(r["_date"]): float(r["close"]) for r in spot_keyed.iter_rows(named=True)}

    rows = []
    for expiry in sorted(usable["target_expiry"].unique().to_list()):
        part = options.filter(pl.col("target_expiry") == expiry)
        wide = (
            part.select(["timestamp", "strike", "open"])
            .unique(["timestamp", "strike"], keep="first")
            .with_columns(pl.col("timestamp").cast(pl.String).str.replace(r" ", "T").str.slice(0, 19))
            .pivot(on="strike", index="timestamp", values="open", aggregate_function="first")
            .sort("timestamp")
        )
        cycles_e = usable.filter(pl.col("target_expiry") == expiry)
        for row in cycles_e.iter_rows(named=True):
            result = base._fast_backtest_cycle(
                row, part, spot_close.get(expiry), cfg, stop_loss=50.0, precomputed_wide=wide
            )
            if result is not None:
                d = asdict(result); d["variant_id"] = row["variant_id"]; rows.append(d)

    result_df = pl.DataFrame(rows)
    result_df.write_csv(out / "all_variant_trades.csv")

    summary = []
    for vid in VARIANT_IDS:
        part = result_df.filter(pl.col("variant_id") == vid)
        row = {"variant_id": vid}
        row.update(base.metrics(part))
        pval = None
        if part.height >= 8:
            pval = base.centered_block_bootstrap_pvalue(part["net_rupees"].to_numpy(), block_len=3, reps=3000, seed=1727)
        row["raw_bootstrap_p"] = pval
        summary.append(row)
    holm = base.holm_adjust([(r["variant_id"], r["raw_bootstrap_p"]) for r in summary])
    for r in summary:
        r["holm_adjusted_p"] = holm.get(r["variant_id"])
    sdf = pl.DataFrame(summary).sort("variant_id")
    sdf.write_csv(out / "ALL_504_PROSPECTIVE_RESULTS.csv")
    sdf.write_json(out / "ALL_504_PROSPECTIVE_RESULTS.json")
    return result_df, sdf


def main():
    out = Path("research/phase22b_weekly_504_prospective_freeze/output")
    cache = Path(os.getenv("HF_HOME", ".hf_cache"))
    out.mkdir(parents=True, exist_ok=True)
    start_date = os.getenv("PROSPECTIVE_START", "2026-05-19")
    end_date = os.getenv("PROSPECTIVE_END", "2026-08-04")
    cycles, options, targets = build_prospective_data(out, cache, start_date, end_date)

    usable = cycles.filter(pl.col("status") == "USABLE_OHLC")
    if usable["variant_id"].n_unique() != 504:
        raise RuntimeError(f"Only {usable['variant_id'].n_unique()} variants have at least one usable cycle")
    if len(targets) < 7:
        raise RuntimeError(f"Only {len(targets)} weekly expiries admitted")

    # Reuse the exact spot source admitted during data construction.
    token = os.getenv("HF_TOKEN") or None
    spath = Path(hf_hub_download(
        repo_id=SPOT_REPO,
        filename=SPOT_FILE,
        repo_type="dataset",
        revision=SPOT_REVISION,
        token=token,
        cache_dir=str(cache),
    ))
    spot = pl.read_parquet(spath)
    if "timestamp" not in spot.columns and "date" in spot.columns:
        spot = spot.rename({"date": "timestamp"})
    if "symbol" in spot.columns:
        spot = spot.filter(pl.col("symbol").cast(pl.String).str.to_uppercase().is_in(["NIFTY", "NIFTY_50", "NIFTY50"]))
    ts_dtype = spot.schema["timestamp"]
    if getattr(ts_dtype, "time_zone", None):
        spot = spot.with_columns(pl.col("timestamp").dt.convert_time_zone("Asia/Kolkata"))
    elif ts_dtype == pl.String:
        spot = spot.with_columns(pl.col("timestamp").str.to_datetime(strict=False, time_zone="Asia/Kolkata"))
    else:
        spot = spot.with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))

    result_df, summary = run_all(cycles, options, spot, out)
    coverage = {
        "weekly_expiries": len(targets),
        "weekly_expiry_list": targets,
        "usable_cycle_rows": usable.height,
        "expected_cycle_rows": len(targets) * 504,
        "all_504_present": usable["variant_id"].n_unique() == 504,
        "positive_holdout": int((summary["total_net_rupees"] > 0).sum()),
        "holm_lt_05": int((summary["holm_adjusted_p"].cast(pl.Float64, strict=False).fill_null(float("nan")) < 0.05).fill_null(False).sum()),
        "min_holm": float(summary["holm_adjusted_p"].drop_nulls().min()) if summary["holm_adjusted_p"].drop_nulls().len() else None,
    }
    (out / "prospective_registry.json").write_text(json.dumps({
        "family_size": 504,
        "k1_rules": K1_RULES, "k2_rules": K2_RULES, "k3_multipliers": K3_MULTIPLIERS,
        "weekly_expiries": targets,
        "start_date": start_date, "end_date": end_date,
        "new_holdout": True, "selection_before_holdout": False,
    }, indent=2))
    (out / "coverage.json").write_text(json.dumps(coverage, indent=2))
    print(json.dumps(coverage, indent=2))


if __name__ == "__main__":
    main()
