# Phase 8 — Strategy Specification: Video-Derived Call-Ladder-to-Spread

## 1. Source hypothesis

The user supplied a step-by-step description of a YouTube strategy. The video-reported construction is:

1. Select a monthly NIFTY options expiry.
2. Identify the ATM strike.
3. Buy a slightly OTM call (lower strike K1).
4. Sell the next higher strike call (K2).
5. Compute the premium difference D = premium(K1) - premium(K2).
6. Multiply D by 2 and find a farther OTM call K3 whose premium is closest to 2D.
7. Sell K3.
8. After several days to about one week, buy the K2 call back as a lock-in move.
9. Retain the resulting long K1 / short K3 bull call spread.
10. Use a hard stop-loss throughout.

The supplied timestamps are treated as source-video metadata, not independent evidence.

## 2. Mathematical identity

Before the lock-in, the position is +1 C(K1) - 1 C(K2) - 1 C(K3), with K1 < K2 < K3.

At expiry, ignoring costs:

P(S_T) = (S_T-K1)^+ - (S_T-K2)^+ - (S_T-K3)^+ + E,

where E is the entry cashflow measured as a positive credit:
E = premium(K2) + premium(K3) - premium(K1).

Piecewise:
- S_T <= K1: P = E
- K1 < S_T <= K2: P = E + S_T - K1
- K2 < S_T <= K3: P = E + K2 - K1
- S_T > K3: P = E + K2 - K1 - (S_T - K3)

Therefore the pre-lock structure is a standard bull call ladder: one long lower call and two short higher calls. It has a capped profit zone and theoretically unbounded loss for sufficiently large upside moves.

## 3. Lock-in identity

When the K2 call is bought back later, the K2 short is cancelled:

(+C(K1) - C(K2) - C(K3)) + C(K2) = +C(K1) - C(K3).

The remaining structure is a conventional defined-risk bull call spread.

## 4. Entry strike rules

Primary preregistered rule:
- K1 = first listed call strike strictly above the spot reference used at entry.
- K2 = the next listed call strike above K1.
- D = K1 call reference premium - K2 call reference premium.
- Target premium = 2D.
- K3 = listed call strike above K2 whose reference premium is closest to the target premium, subject to liquidity and data-quality filters.

Use midpoint when valid bid and ask are available. Use last traded price only when a valid two-sided quote is unavailable, and flag such observations as lower quality. Actual simulated fills use executable bid/ask rules.

## 5. Execution model

For each leg:
- buys execute at ask plus slippage;
- sells execute at bid minus slippage;
- multi-leg execution is used only when reliable historical spread quotes exist; otherwise leg-level execution is mandatory;
- crossed, locked, zero or negative quotes are excluded;
- stale quotes are excluded by a preregistered quote-age threshold;
- insufficient-liquidity observations are rejected.

Slippage sensitivity will include base, stressed and adverse-fill scenarios.

## 6. Timing model

Entry occurs at a fixed predeclared timestamp or end-of-day convention.

Lock-in timing candidates are a limited preregistered family:
- 2 trading days after entry;
- 3 trading days;
- 5 trading days;
- 7 calendar days where an eligible session exists;
- a fixed K3-premium-decay trigger, if formally preregistered before validation.

One final lock rule is frozen before the untouched holdout.

## 7. Stop-loss model

The source description says a hard stop-loss is mandatory but does not specify a numeric trigger.

Therefore the research distinguishes the source-faithful qualitative rule from a mechanical quantitative implementation.

Candidate stop classes are limited to:
- total-trade P&L threshold;
- loss multiple of a predefined initial risk unit;
- underlying-price trigger relative to K2/K3;
- post-lock spread stop.

No stop parameter may be tuned on the final holdout.

## 8. Exit model

Distinct policies:
- hold to expiry unless stopped;
- exit at lock-in;
- exit after lock-in at a fixed profit target;
- exit at a fixed number of trading days before expiry.

The source-faithful primary candidate is entry -> decay window -> lock -> retain bull call spread -> exit at expiry or hard stop.

## 9. Margin model

Track margin at:
- pre-entry;
- three-leg entry;
- intermediate decay states;
- immediately after K2 buyback;
- post-lock bull call spread;
- adverse move near K3.

Report peak margin, median margin, margin reduction percentage, return on peak margin and margin efficiency versus a plain bull call spread.

Margin will be based on historical exchange/broker data where available rather than a single video example.

## 10. Costs

Every trade includes Paytm Money brokerage, statutory/regulatory/exchange charges, STT, stamp duty where applicable, GST, bid/ask spread, slippage and any applicable execution or square-off fee.

Paytm Money currently states Rs.10 brokerage per executed unique F&O order and that statutory/regulatory/exchange charges are levied at actuals. These inputs will be versioned by date rather than treated as timeless constants.

## 11. Research hypotheses

H0-1: The strategy does not produce positive mean net return after all costs in out-of-sample testing.
H1-1: The strategy produces positive mean net return after all costs in out-of-sample testing.

H0-2: The lock-in step does not materially improve risk-adjusted economics relative to the same entry held unmanaged.
H1-2: The lock-in step improves risk-adjusted economics.

H0-3: The margin reduction after the K2 buyback is not economically material relative to the pre-lock ladder.
H1-3: The K2 buyback materially reduces required margin.

H0-4: Any apparent edge is not robust across volatility, trend, skew, expiry-distance and liquidity regimes.
H1-4: The edge remains detectable across multiple preregistered regimes.

H0-5: The strategy's apparent benefit disappears after realistic bid/ask, slippage and brokerage costs.
H1-5: Positive net economics remain after realistic execution costs.

## 12. Primary endpoints

- annualized net Sharpe ratio;
- mean and median net trade P&L;
- maximum drawdown;
- probability of loss;
- annualized return/CAGR where meaningful;
- profit factor;
- expected shortfall / CVaR;
- return on peak margin.

Secondary endpoints: margin reduction, lock-in contribution, theta attribution, vega/gamma exposure, tail-loss frequency and costs as a share of gross P&L.

## 13. Statistical framework

Use chronological training, validation and locked final holdout sets.

Use walk-forward evaluation, CPCV where sample structure permits, PBO/CSCV-style diagnostics, deflated Sharpe ratio, bootstrap confidence intervals, block bootstrap where needed, multiple-testing correction and preregistered sensitivity analysis.

The strategy must not be promoted because of one favorable period.

## 14. Regime conditioning

Where data permits, synchronize NIFTY realized volatility, India VIX, global volatility, USD/INR, gold, NIFTY trend/drawdown state, FII/FPI and DII activity, option skew/term structure, volume/OI, breadth and major event windows.

Regime labels must use only information available at decision time.

## 15. Comparative controls

Minimum controls:
1. plain bull call spread K1/K3;
2. original three-leg ladder without lock;
3. locked strategy;
4. matched-risk bull call spread;
5. simple long-call control where comparable.

These controls test whether the formula and lock sequence add value rather than merely reshaping a standard payoff.

## 16. Falsification gates

Do not promote if any critical gate fails, including negative net expectancy in the locked holdout, unstable sign/Sharpe across robustness paths, concentration in a few trades, tail loss incompatible with the declared risk budget, extreme sensitivity to tiny slippage changes, dependence on illiquid/stale quotes, non-reproducible margin claims, or leakage.

## 17. Reproducibility

Every result records the source data version/hash, quote convention, timestamp convention, strike-selection rule, lock rule, stop rule, transaction-cost schedule, margin data version, code version/commit and random seeds where applicable.

No manual post-hoc trade selection.