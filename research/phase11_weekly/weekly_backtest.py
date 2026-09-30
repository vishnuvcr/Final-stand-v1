from __future__ import annotations

import argparse
import json
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path

import polars as pl


@dataclass(frozen=True)
class CostConfig:
    brokerage_per_order: float = 10.0
    stt_sell_rate: float = 0.0015
    exchange_turnover_rate: float = 0.0003503
    sebi_turnover_rate: float = 0.000001
    stamp_buy_rate: float = 0.00003
    ipft_turnover_rate: float = 0.000005
    gst_rate: float = 0.18
    slippage_points_per_leg: float = 0.25
    lot_size_pre_2026: int = 75
    lot_size_2026: int = 65


@dataclass
class TradeResult:
    target_expiry: str
    entry_timestamp: str
    lock_timestamp: str
    exit_timestamp: str
    k1: float
    k2: float
    k3: float
    entry_spot: float
    d: float
    target_premium: float
    k3_target_error: float | None
    lot_size: int
    stop_loss_points: float | None
    exit_reason: str
    gross_points: float
    costs_points: float
    net_points: float
    gross_rupees: float
    costs_rupees: float
    net_rupees: float
    orders: int
    locked: bool
    data_quality: str


def lot_size_for_expiry(expiry: str, cfg: CostConfig) -> int:
    return cfg.lot_size_pre_2026 if expiry < "2026-01-06" else cfg.lot_size_2026


def cost_rates_for_date(trade_date: str, cfg: CostConfig) -> tuple[float, float, float, float]:
    """Return dated STT, NSE option transaction, SEBI and IPFT rates."""
    if trade_date < "2024-10-01":
        return 0.000625, 0.000495, 0.000001, cfg.ipft_turnover_rate
    if trade_date < "2026-04-01":
        return 0.001, 0.0003503, 0.000001, cfg.ipft_turnover_rate
    return cfg.stt_sell_rate, cfg.exchange_turnover_rate, cfg.sebi_turnover_rate, cfg.ipft_turnover_rate


def cost_rupees(buy_turnover: float, sell_turnover: float, orders: int, cfg: CostConfig, trade_date: str) -> float:
    brokerage = cfg.brokerage_per_order * orders
    stt_rate, exchange_rate, sebi_rate, ipft_rate = cost_rates_for_date(trade_date, cfg)
    stt = sell_turnover * stt_rate
    exchange = (buy_turnover + sell_turnover) * exchange_rate
    sebi = (buy_turnover + sell_turnover) * sebi_rate
    ipft = (buy_turnover + sell_turnover) * ipft_rate
    stamp = buy_turnover * cfg.stamp_buy_rate
    gst_base = brokerage + exchange + sebi + ipft
    gst = gst_base * cfg.gst_rate
    return brokerage + stt + exchange + sebi + ipft + stamp + gst


def intrinsic(spot: float, strike: float) -> float:
    return max(spot - strike, 0.0)


def entry_cf(p1: float, p2: float, p3: float, slip: float) -> float:
    return (p2 - slip) + (p3 - slip) - (p1 + slip)


def lock_cf(p2: float, slip: float) -> float:
    return -(p2 + slip)


def exit_prelock_cf(p1: float, p2: float, p3: float, slip: float) -> float:
    return -(p1 - slip) + (p2 + slip) + (p3 + slip)


def exit_locked_cf(p1: float, p3: float, slip: float) -> float:
    return -(p1 - slip) + (p3 + slip)


def _timestamp_key(timestamp: str) -> str:
    return str(timestamp).replace(" ", "T")[:19]


def _timestamp_key_expr(column: str = "timestamp") -> pl.Expr:
    return pl.col(column).cast(pl.String).str.replace(r" ", "T").str.slice(0, 19)


def marks_at(df: pl.DataFrame, timestamp: str, strikes: list[float]) -> dict[float, float]:
    rows = df.filter(
        (_timestamp_key_expr() == _timestamp_key(timestamp))
        & pl.col("strike").is_in(strikes)
    )
    return {float(r["strike"]): float(r["open"]) for r in rows.iter_rows(named=True)}


def backtest_cycle(cycle: dict, options: pl.DataFrame, spot: pl.DataFrame, stop_loss: float | None, cfg: CostConfig):
    if cycle["status"] != "USABLE_OHLC":
        return None

    expiry = cycle["target_expiry"]
    k1, k2, k3 = float(cycle["k1"]), float(cycle["k2"]), float(cycle["k3"])
    lot = lot_size_for_expiry(expiry, cfg)
    slip = cfg.slippage_points_per_leg
    entry_ts, lock_ts = cycle["entry_timestamp"], cycle["lock_timestamp"]

    entry = marks_at(options, entry_ts, [k1, k2, k3])
    if len(entry) != 3:
        return None

    net_cf = entry_cf(entry[k1], entry[k2], entry[k3], slip)
    entry_buy = (entry[k1] + slip) * lot
    entry_sell = ((entry[k2] - slip) + (entry[k3] - slip)) * lot
    orders = 3

    pre = options.filter(
        (_timestamp_key_expr() > _timestamp_key(entry_ts))
        & (_timestamp_key_expr() < _timestamp_key(lock_ts))
        & pl.col("strike").is_in([k1, k2, k3])
    ).select(["timestamp", "strike", "open"]).sort("timestamp")

    if stop_loss is not None and pre.height:
        for ts_key, g in pre.group_by("timestamp", maintain_order=True):
            ts = str(ts_key[0] if isinstance(ts_key, tuple) else ts_key)
            m = {float(r["strike"]): float(r["open"]) for r in g.iter_rows(named=True)}
            if len(m) != 3:
                continue
            mtm = net_cf + m[k1] - m[k2] - m[k3]
            if mtm <= -abs(stop_loss):
                later = options.filter(
                    (_timestamp_key_expr() > _timestamp_key(ts))
                    & pl.col("strike").is_in([k1, k2, k3])
                ).select(["timestamp", "strike", "open"]).sort("timestamp")
                if later.height:
                    nt = str(later["timestamp"][0])
                    nm = marks_at(options, nt, [k1, k2, k3])
                    if len(nm) == 3:
                        net_cf += exit_prelock_cf(nm[k1], nm[k2], nm[k3], slip)
                        orders += 3
                        buy_turn = entry_buy + (nm[k2] + slip) * lot + (nm[k3] + slip) * lot
                        sell_turn = entry_sell + (nm[k1] - slip) * lot
                        costs = cost_rupees(buy_turn, sell_turn, orders, cfg, nt[:10])
                        gross = net_cf
                        return TradeResult(
                            expiry, entry_ts, lock_ts, nt, k1, k2, k3,
                            float(cycle["entry_spot"]), float(cycle["p1"]) - float(cycle["p2"]),
                            float(cycle["target_premium"]),
                            float(cycle["target_error"]) if cycle["target_error"] is not None else None,
                            lot, stop_loss, "stop_prelock", gross, costs / lot,
                            gross - costs / lot, gross * lot, costs, gross * lot - costs,
                            orders, False, "OHLC_RECONSTRUCTION"
                        )

    lock = marks_at(options, lock_ts, [k1, k2, k3])
    if len(lock) != 3:
        return None

    net_cf += lock_cf(lock[k2], slip)
    orders += 1

    post = options.filter(
        (_timestamp_key_expr() > _timestamp_key(lock_ts))
        & pl.col("strike").is_in([k1, k3])
    ).select(["timestamp", "strike", "open"]).sort("timestamp")

    if stop_loss is not None and post.height:
        for ts_key, g in post.group_by("timestamp", maintain_order=True):
            ts = str(ts_key[0] if isinstance(ts_key, tuple) else ts_key)
            m = {float(r["strike"]): float(r["open"]) for r in g.iter_rows(named=True)}
            if len(m) != 2:
                continue
            mtm = net_cf + m[k1] - m[k3]
            if mtm <= -abs(stop_loss):
                later = options.filter(
                    (pl.col("timestamp").cast(pl.String) > ts)
                    & pl.col("strike").is_in([k1, k3])
                ).select(["timestamp", "strike", "open"]).sort("timestamp")
                if later.height:
                    nt = str(later["timestamp"][0])
                    nm = marks_at(options, nt, [k1, k3])
                    if len(nm) == 2:
                        net_cf += exit_locked_cf(nm[k1], nm[k3], slip)
                        orders += 2
                        buy_turn = entry_buy + (lock[k2] + slip) * lot + (nm[k3] + slip) * lot
                        sell_turn = entry_sell + (nm[k1] - slip) * lot
                        costs = cost_rupees(buy_turn, sell_turn, orders, cfg, nt[:10])
                        gross = net_cf
                        return TradeResult(
                            expiry, entry_ts, lock_ts, nt, k1, k2, k3,
                            float(cycle["entry_spot"]), float(cycle["p1"]) - float(cycle["p2"]),
                            float(cycle["target_premium"]),
                            float(cycle["target_error"]) if cycle["target_error"] is not None else None,
                            lot, stop_loss, "stop_postlock", gross, costs / lot,
                            gross - costs / lot, gross * lot, costs, gross * lot - costs,
                            orders, True, "OHLC_RECONSTRUCTION"
                        )

    spot_exp = spot.filter(
        pl.col("timestamp").cast(pl.String).str.starts_with(expiry)
    ).sort("timestamp")
    if spot_exp.height == 0:
        return None

    s = float(spot_exp["close"][-1])
    gross = net_cf + intrinsic(s, k1) - intrinsic(s, k3)
    buy_turn = entry_buy + (lock[k2] + slip) * lot
    sell_turn = entry_sell
    costs = cost_rupees(buy_turn, sell_turn, orders, cfg, expiry)

    return TradeResult(
        expiry, entry_ts, lock_ts, f"{expiry}T15:30:00+05:30", k1, k2, k3,
        float(cycle["entry_spot"]), float(cycle["p1"]) - float(cycle["p2"]),
        float(cycle["target_premium"]),
        float(cycle["target_error"]) if cycle["target_error"] is not None else None,
        lot, stop_loss, "expiry", gross, costs / lot,
        gross - costs / lot, gross * lot, costs, gross * lot - costs,
        orders, True, "OHLC_RECONSTRUCTION"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="research/phase9_weekly/output/weekly_cycle_manifest.csv")
    ap.add_argument("--options", default="research/phase9_weekly/output/selected_weekly_option_bars.parquet")
    ap.add_argument("--spot", default="research/phase9_weekly/output/selected_weekly_spot_bars.parquet")
    ap.add_argument("--output", default="research/phase11_weekly/output/trade_results.csv")
    ap.add_argument("--stop-loss-points", type=float, default=None)
    ap.add_argument("--slippage-points", type=float, default=0.25)
    args = ap.parse_args()

    cycles = pl.read_csv(args.manifest)
    options = pl.read_parquet(args.options)
    spot = pl.read_parquet(args.spot)
    cfg = CostConfig(slippage_points_per_leg=args.slippage_points)
    results = []

    for row in cycles.iter_rows(named=True):
        try:
            out = backtest_cycle(row, options, spot, args.stop_loss_points, cfg)
            if out:
                results.append(asdict(out))
        except Exception as exc:
            print(f"cycle {row.get('target_expiry')} failed: {exc}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    result_columns = [f.name for f in TradeResult.__dataclass_fields__.values()]
    result_df = pl.DataFrame(results, schema=result_columns) if results else pl.DataFrame({c: [] for c in result_columns})
    result_df.write_csv(out)

    summary = {
        "trades": len(results),
        "stop_loss_points": args.stop_loss_points,
        "net_rupees": sum(x["net_rupees"] for x in results),
        "mean_net_rupees": (sum(x["net_rupees"] for x in results) / len(results)) if results else None,
        "win_rate": (sum(x["net_rupees"] > 0 for x in results) / len(results)) if results else None,
        "total_costs_rupees": sum(x["costs_rupees"] for x in results),
        "lot_size_rule": "75 through 2025-12-23; 65 from 2026-01-06",
        "execution_quality": "OHLC_RECONSTRUCTION",
    }
    (out.parent / (out.stem + ".summary.json")).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
