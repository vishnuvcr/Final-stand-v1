# Phase 22W — Execution-Aware Prospective Validation

## Status
**PROPOSED — not executed yet.**

Phase 21W is complete. It recovered the five missing weekly holdouts and reran all 224 frozen configurations over 63 expiries. No configuration passed the preregistered promotion gate. Therefore Phase 22W must not select a configuration from the Phase 21W holdout after inspecting those results.

## Research question

Does the apparent Phase 21W parameter-surface pattern persist under a **new, prospectively frozen, execution-aware out-of-sample test** using executable bid/ask or order-book evidence and a predeclared transaction-cost/liquidity model?

## Primary hypothesis

The Phase 21W descriptive pattern suggests stronger historical outcomes around higher K3 values and ITM/NEXT2–NEXT3 combinations. Phase 22W will test this hypothesis prospectively rather than treating any Phase 21W configuration as already selected.

## Mandatory safeguards

1. No Phase 21W holdout result may be used to tune the Phase 22W holdout.
2. Any Phase 22W candidate family and parameter subset must be frozen **before** its new holdout is opened.
3. No synthetic bars, strike substitution, interpolation, or cross-source leg mixing.
4. Prefer executable bid/ask or order-book observations; OHLC is fallback only and must be explicitly labeled.
5. Preserve Paytm Money/NSE transaction costs, brokerage, statutory charges, slippage and liquidity constraints.
6. Keep the Phase 21W 224-way inference result immutable.
7. Every source failure and data-contract failure must be logged.
8. Important source data must be cached in GitHub Actions and reused.

## Phases

### Phase 22.1 — Data-source audit
Search and qualify:
- NSE/BSE public historical routes
- Hugging Face datasets
- GitHub repositories
- Kaggle
- broker/API routes where credentials/entitlements are available
- other public archives with historical option bid/ask/order-book information

Admission requires provenance, timestamp quality, strike/expiry coverage, and reproducibility.

### Phase 22.2 — Execution-data contract
Define exact requirements for:
- bid/ask timestamp
- bid/ask size
- trade/quote ordering
- option expiry
- strike
- call/put
- market status
- missing quote handling
- stale quote detection
- spread/liquidity filters

### Phase 22.3 — Prospective configuration freeze
Before opening the new holdout:
- define the candidate family from a predeclared rule
- freeze K1/K2/K3 candidates
- freeze entry/lock times
- freeze stop logic
- freeze slippage/cost model
- freeze statistical tests and multiplicity correction

### Phase 22.4 — Chronological evaluation
Use a new chronological train/validation/holdout period not used by Phase 21W.

### Phase 22.5 — Execution-aware backtest
Calculate:
- bid/ask executable fills
- spread cost
- slippage
- brokerage
- exchange/statutory charges
- liquidity/size constraints
- rejected/partial fills where data permit
- P&L
- drawdown
- expected shortfall
- Sharpe
- turnover and capital efficiency

### Phase 22.6 — Statistical inference
Predeclared:
- bootstrap/block-bootstrap procedure
- confidence intervals
- multiple-testing correction
- robustness checks
- regime-stratified analysis

### Phase 22.7 — Final decision
Possible outcomes:
1. no candidate survives;
2. candidate survives statistical and execution gates and is eligible for a separate capital/margin validation phase;
3. data quality prevents a defensible conclusion.

No live-trading deployment is implied by outcome 2.

## Exit criteria

Phase 22W ends when:
- source audit is exhausted;
- execution contract is frozen;
- prospective configuration set is frozen;
- new holdout is evaluated;
- statistical tests are complete;
- execution costs are included;
- manuscript and audit artifacts are published.

## Required outputs

- phase plan
- variant registry
- source manifest
- cached data manifest
- execution-contract specification
- backtest results
- statistical results
- error log
- research log
- final manuscript
- README update

## Explicit non-goal

Do **not** simply take ITM3/NEXT1/K3=4 because it was the best Phase 21W holdout configuration. Doing so would constitute post-hoc holdout selection.
