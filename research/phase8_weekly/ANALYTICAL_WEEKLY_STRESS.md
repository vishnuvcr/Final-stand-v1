# Phase 10W — Analytical Weekly Stress Test (Non-Empirical)

## Purpose

Before historical data are available, use a Black–Scholes benchmark only to understand the mechanics of the weekly formula. This is **not** a market backtest and must not be interpreted as evidence of profitability.

## Benchmark

Assumptions:
- NIFTY-like spot = 25,000;
- risk-free rate = 0 for simplicity;
- weekly time-to-expiry = 1, 2 or 4 trading days;
- annualized implied volatility = 12%, 18%, 25%, 35%;
- 1% strike spacing for the illustration;
- K1 = first OTM call;
- K2 = next call;
- K3 selected by the closest premium to 2 × (C(K1)-C(K2)).

## Observed mechanical behavior

Across the tested horizons and volatility levels, the formula can produce a farther OTM K3 whose premium is materially different from the target because weekly option premiums are discrete and collapse rapidly near expiry.

Illustrative 1-day-to-expiry, 18% IV case:
- K1 = 25,250;
- K2 = 25,500;
- K3 = 25,750;
- C(K1) ≈ ₹29.81;
- C(K2) ≈ ₹4.67;
- target = 2 × (29.81 − 4.67) ≈ ₹50.27.

The next available farther-strike premium in the simplified grid is much lower than the target. Therefore the empirical strategy must not assume that the target premium is actually attainable.

## Mandatory diagnostic

For every weekly trade calculate:

`target_error = abs(actual_K3_premium - target_premium) / target_premium`

Report:
- median target error;
- 75th/90th/95th percentile;
- target error by IV regime;
- target error by days-to-expiry;
- target error by liquidity.

## Tail-risk implication

The pre-lock structure remains a bull call ladder. Once spot moves above K3, every additional point of underlying upside increases expiry loss by approximately one point per option unit.

The weekly horizon does not remove tail risk. It compresses the time available for recovery and makes jump/gap behavior more important.

## Lock implication

Buying K2 later removes the middle short. After lock, the tail is bounded by the K1/K3 spread width.

The lock is therefore a **risk-topology transformation** from unbounded upside loss before lock to a bounded-risk bull call spread after lock.

## Research requirement

Target error must be reported rather than silently hidden. Trades with large target error remain in the primary sample under the exact closest-strike rule unless excluded by a preregistered liquidity/data-quality rule.

## Conclusion

The weekly formula is mechanically testable, but its success depends on the discrete option surface. The weekly experiment therefore needs to test not only whether the strategy makes money, but whether the premium-selection formula is actually realizable at available weekly strikes.
