"""Deterministic mechanics for the Phase 8W weekly call-ladder research.

This module deliberately does not fetch market data. It implements only:
- strike selection from a point-in-time option snapshot;
- executable-fill accounting;
- lifecycle leg cancellation;
- expiry payoff;
- simple cost accounting.

Empirical backtests must provide point-in-time data externally.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Quote:
    strike: float
    bid: float
    ask: float
    ltp: float


@dataclass(frozen=True)
class Leg:
    strike: float
    quantity: int  # +1 long, -1 short


@dataclass(frozen=True)
class CostSchedule:
    brokerage_per_order: float
    stt_rate_sell: float
    exchange_txn_rate: float
    sebi_rate: float
    stamp_rate_buy: float
    gst_rate: float


def valid_quote(q: Quote) -> bool:
    return q.bid > 0 and q.ask > 0 and q.ask >= q.bid and q.ltp >= 0


def choose_strikes(spot: float, quotes: Iterable[Quote]):
    qs = sorted((q for q in quotes if valid_quote(q) and q.strike > spot), key=lambda q: q.strike)
    if len(qs) < 3:
        raise ValueError("At least three valid OTM call strikes are required")
    k1, k2 = qs[0], qs[1]
    d = (k1.bid + k1.ask) / 2 - (k2.bid + k2.ask) / 2
    if d <= 0:
        raise ValueError("Premium difference must be positive")
    target = 2 * d
    candidates = qs[2:]
    k3 = min(candidates, key=lambda q: abs(((q.bid + q.ask) / 2) - target))
    return k1, k2, k3, d, target


def entry_cashflow(k1: Quote, k2: Quote, k3: Quote, slippage: float = 0.0) -> float:
    """Positive = cash received. Buy K1 at ask, sell K2/K3 at bid."""
    return (k2.bid - slippage) + (k3.bid - slippage) - (k1.ask + slippage)


def lock_cashflow(k2: Quote, slippage: float = 0.0) -> float:
    """Buying back K2: negative cashflow."""
    return -(k2.ask + slippage)


def expiry_payoff(spot_expiry: float, k1: float, k2: float, k3: float, entry_cf: float) -> float:
    call = lambda s, k: max(s - k, 0.0)
    return entry_cf + call(spot_expiry, k1) - call(spot_expiry, k2) - call(spot_expiry, k3)


def locked_expiry_payoff(spot_expiry: float, k1: float, k3: float, net_cashflow: float) -> float:
    call = lambda s, k: max(s - k, 0.0)
    return net_cashflow + call(spot_expiry, k1) - call(spot_expiry, k3)


def transaction_costs(
    buy_turnover: float,
    sell_turnover: float,
    orders: int,
    schedule: CostSchedule,
) -> float:
    brokerage = schedule.brokerage_per_order * orders
    stt = sell_turnover * schedule.stt_rate_sell
    exchange = (buy_turnover + sell_turnover) * schedule.exchange_txn_rate
    sebi = (buy_turnover + sell_turnover) * schedule.sebi_rate
    stamp = buy_turnover * schedule.stamp_rate_buy
    pre_gst = brokerage + stt + exchange + sebi + stamp
    gst = pre_gst * schedule.gst_rate
    return pre_gst + gst
