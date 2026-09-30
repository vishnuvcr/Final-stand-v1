from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import date, datetime, time
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
THEMARKET_REPO = "thetrademarkk/india-index-options-1m"
THEMARKET_INDEX = "index/NIFTY.parquet"


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
    tm_revision = os.getenv("THEMARKET_REVISION", "main")

    rpath = Path(hf_hub_download(
        repo_id=RISSIN_REPO,
        filename=RISSIN_FILE,
        repo_type="dataset",
        revision=rissin_revision,
        token=token,
        cache_dir=str(cache),
    ))
    tpath = Path(hf_hub_download(
        repo_id=THEMARKET_REPO,
        filename=THEMARKET_INDEX,
        repo_type="dataset",
        revision=tm_revision,
        token=token,
        cache_dir=str(cache),
    ))

    # Resolve immutable source revision IDs for provenance.
    api = HfApi(token=token)
    rinfo = api.repo_info(RISSIN_REPO, repo_type="dataset", revision=rissin_revision)
    tinfo = api.repo_info(THEMARKET_REPO, repo_type="dataset", revision=tm_revision)
    resolved_r = getattr(rinfo, "sha", None) or rissin_revision
    resolved_t = getattr(tinfo, "sha", None) or tm_revision

    idx = pl.read_parquet(tpath).with_columns(
        pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata"))
    )
    dates = idx.select(pl.col("timestamp").dt.date().alias("d")).unique().sort("d")["d"].to_list()

    lf = pl.scan_parquet(rpath)
    schema = lf.collect_schema()
    required = {"timestamp", "expiry", "strike", "option_type", "open", "volume", "underlying", "granularity"}
    missing = sorted(required - set(schema.names()))
    if missing:
        raise RuntimeError(f"RISSIN source missing columns: {missing}")

    # Discover target expiries from the source itself, then exclude the latest
    # expiry in each month (monthly contract) to retain weekly expiries.
    discovery = (
        lf.filter(pl.col("underlying") == "NIFTY")
        .filter(pl.col("granularity") == "1min")
        .with_columns(pl.col("expiry").cast(pl.String).str.slice(0, 10).alias("_expiry"))
        .filter((pl.col("_expiry") >= start_date) & (pl.col("_expiry") <= end_date))
        .select("_expiry")
        .unique()
        .collect(engine="streaming")
    )
    all_expiries = sorted(str(x) for x in discovery["_expiry"].to_list())
    latest_by_month = {}
    for e in all_expiries:
        key = e[:7]
        latest_by_month[key] = max(e, latest_by_month.get(key, e))
    monthly = set(latest_by_month.values())
    targets = [e for e in all_expiries if e not in monthly]
    if len(targets) < 8:
        raise RuntimeError(f"Only {len(targets)} weekly expiries admitted from RISSIN in {start_date}..{end_date}: {targets}")

    target_dates = [date.fromisoformat(x) for x in targets]
    first_target = target_dates[0]
    prior_candidates = [date.fromisoformat(x) for x in all_expiries if date.fromisoformat(x) < first_target]
    if not prior_candidates:
        raise RuntimeError("No prior weekly/monthly expiry available to define the first entry.")
    prior_expiry = prior_candidates[-1]

    def first_trading_day_after(d):
        return next((x for x in dates if x > d), None)

    def prior_trading_day(d):
        c = [x for x in dates if x < d]
        return c[-1] if c else None

    cycles = []
    raw_parts = []

    for expiry in target_dates:
        prev_candidates = [date.fromisoformat(x) for x in all_expiries if date.fromisoformat(x) < expiry and date.fromisoformat(x) not in monthly]
        prior = prev_candidates[-1] if prev_candidates else prior_expiry
        entry_day = first_trading_day_after(prior)
        lock_day = prior_trading_day(expiry)
        if entry_day is None or lock_day is None:
            raise RuntimeError(f"Cannot establish entry/lock trading days for {expiry}")
        entry_ts = datetime.combine(entry_day, time(10, 0), IST)
        lock_ts = datetime.combine(lock_day, time(14, 0), IST)

        spot_row = idx.filter(pl.col("timestamp") == ts_lit(entry_ts))
        if spot_row.height != 1:
            raise RuntimeError(f"Exact NIFTY spot row missing at {entry_ts} for {expiry}")
        spot = float(spot_row["open"][0])

        end_ts = datetime.combine(expiry, time(16, 0), IST)
        opt = (
            lf.filter(pl.col("underlying") == "NIFTY")
            .filter(pl.col("granularity") == "1min")
            .filter(pl.col("expiry").cast(pl.String).str.slice(0, 10) == expiry.isoformat())
            .filter(pl.col("option_type").cast(pl.String).str.to_uppercase().is_in(["CE", "CALL"]))
            .filter(pl.col("timestamp") >= ts_lit(entry_ts))
            .filter(pl.col("timestamp") <= ts_lit(end_ts))
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
                                        & pl.col("timestamp").is_in([ts_lit(entry_ts), ts_lit(lock_ts)])
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
        "thetrademarkk_index_repo": THEMARKET_REPO,
        "thetrademarkk_index_file": THEMARKET_INDEX,
        "thetrademarkk_requested_revision": tm_revision,
        "thetrademarkk_resolved_revision": resolved_t,
        "thetrademarkk_index_sha256": sha256(tpath),
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
    if len(targets) < 8:
        raise RuntimeError(f"Only {len(targets)} weekly expiries admitted")

    # Use the cached NIFTY spot source only for expiry-date close in the frozen engine.
    token = os.getenv("HF_TOKEN") or None
    tpath = Path(hf_hub_download(
        repo_id=THEMARKET_REPO,
        filename=THEMARKET_INDEX,
        repo_type="dataset",
        revision=os.getenv("THEMARKET_REVISION", "main"),
        token=token,
        cache_dir=str(cache),
    ))
    spot = pl.read_parquet(tpath).with_columns(pl.col("timestamp").cast(pl.Datetime(time_zone="Asia/Kolkata")))

    result_df, summary = run_all(cycles, options, spot, out)
    coverage = {
        "weekly_expiries": len(targets),
        "weekly_expiry_list": targets,
        "usable_cycle_rows": usable.height,
        "expected_cycle_rows": len(targets) * 504,
        "all_504_present": usable["variant_id"].n_unique() == 504,
        "positive_holdout": int((summary["total_net_rupees"] > 0).sum()),
        "holm_lt_05": int((summary["holm_adjusted_p"] < 0.05).fill_null(False).sum()),
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
