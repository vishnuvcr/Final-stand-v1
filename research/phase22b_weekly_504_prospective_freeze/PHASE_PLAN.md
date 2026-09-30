# Phase 22B — Weekly 504 Prospective Validation

## Status
**ACTIVE — protocol and 504 family frozen; new chronological OHLC holdout opened only after freeze.**

## Research question
Does the complete 504-configuration weekly strategy family retain its historical behavior on a genuinely new chronological period after the Phase-21/22A sample?

## Frozen family
- K1: OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8
- K2: NEXT1, NEXT2, NEXT3, MIRROR_GAP
- K3: 0.5, 1, 1.5, 2, 2.5, 3, 4
- Total: **504 configurations**

No configuration is selected from the new period before the family-level results are computed.

## Weekly protocol
- Entry: 10:00 IST on the first trading day after the prior weekly expiry.
- Lock/exit decision: 14:00 IST on the trading day before the target weekly expiry.
- Remaining exposure may continue to target expiry unless stopped/exited.
- Hard stop: 50 NIFTY points.
- Baseline slippage: 0.50 NIFTY points per leg.
- Paytm Money/NSE transaction-cost model: unchanged.

## New-data boundary
The new validation starts after the last Phase-21 target expiry (2026-05-12). The admitted public archive currently reaches 2026-08-04, so the requested new period is 2026-05-19 through 2026-08-04, subject to the source's weekly-expiry catalog and data-quality checks. The source documents 1-minute NIFTY option OHLCV(+OI) bars and notes partial coverage for illiquid/far strikes. citeturn7search2turn8search0

This is a genuinely chronological external period relative to the Phase-21 sample, but it is **OHLC-based**, not bid/ask/depth executable.

## Statistical analysis
For every configuration:
- valid cycle count;
- total/mean/median net P&L;
- win rate;
- max drawdown;
- expected shortfall;
- annualized weekly Sharpe;
- mean transaction cost;
- centered block-bootstrap p-value where sample size permits;
- Holm correction across all 504 configurations.

Because the new period is short, no configuration is promoted solely from this phase. The existing 30-cycle capital-promotion minimum remains a separate gate.

## Required outputs
- complete 504 registry;
- selected weekly-expiry manifest;
- source SHA/revision manifest;
- full row-level prospective results;
- Holm-adjusted statistics;
- coverage report;
- error log;
- research log;
- final manuscript and README update.

## Exit criteria
Phase 22B closes only after:
1. every admitted new weekly expiry is tested;
2. all 504 configurations are evaluated;
3. data-quality/coverage is reported;
4. family-level statistical inference is complete;
5. no result is selected post hoc;
6. manuscript and README are updated.
