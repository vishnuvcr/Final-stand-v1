# Phase 22B — Weekly 504 Prospective Validation Plan

## Purpose
Prospectively validate the frozen weekly-options strategy family on a genuinely unseen period without selecting or tuning a configuration from the holdout.

## Frozen research family
- K1: OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8 (18 rules)
- K2: NEXT1, NEXT2, NEXT3, MIRROR_GAP (4 rules)
- K3 multipliers: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0 (7 values)
- Total: 18 × 4 × 7 = 504 configurations

## Frozen weekly protocol
- Entry: 10:00 IST on the first trading day after the prior weekly expiry.
- Lock/exit decision: 14:00 IST on the trading day before target expiry.
- Remaining exposure may continue to target expiry unless the hard stop is triggered.
- Hard stop: 50 NIFTY points.
- Baseline slippage: 0.50 NIFTY points per leg.
- Transaction-cost/brokerage model: frozen Paytm Money/NSE model used by the preceding phases.
- Causal entry spot: latest observation at or before 10:00 IST, within the frozen five-minute tolerance.
- No post-hoc configuration selection.

## Data methodology
1. Use the pinned independent spot archive and the primary NIFTY intraday option archive.
2. Use approved secondary sources only for gap recovery when the primary source cannot cover an eligible expiry.
3. Record source revisions, hashes, admitted expiries and fallback usage in the run manifest.
4. Cache/reuse retrieved data rather than redownloading unnecessarily.
5. Treat OHLC-derived fills as a separate execution-evidence layer; do not call them historical bid/ask execution.

## Statistical methodology
- Evaluate all 504 configurations on the same admitted weekly cycles.
- Report net rupee P&L, mean/median, win rate, drawdown, expected shortfall, Sharpe and costs.
- Compute the frozen centered block bootstrap only when each configuration has at least 8 completed observations.
- Use the frozen block length and replication count from the implementation.
- Apply Holm correction across all 504 configurations.
- Capital promotion remains gated by the pre-specified minimum 30 completed cycles and all existing risk/cost checks.
- No configuration is promoted solely from descriptive positive P&L.

## Phase gates
- Gate A: frozen registry and protocol validated.
- Gate B: prospective period begins after freeze.
- Gate C: source coverage and causal data checks pass.
- Gate D: all 504 configurations are evaluated on every admitted cycle.
- Gate E: statistical inference runs only when its pre-specified sample-size gate is met.
- Gate F: capital promotion requires the existing 30-cycle evidence gate.
- If data coverage prevents later cycles, record the limitation and search approved external archives before changing the strategy.

## Current execution status
The 2026-10-01 extension requested 2026-05-19 through 2026-09-08 but admitted only eight qualifying weekly expiries ending 2026-07-21. All 504 configurations were evaluated, but each has n=6, so statistical confirmation and capital promotion remain pending additional qualifying cycles.

## Stop rule
Do not tune, rank, or select a configuration from the current six-trade prospective sample. Continue only through the planned source-recovery and prospective-validation path until the pre-specified phase gates are either satisfied or a documented data limitation prevents further progress.


## 2026-10-01 — Frozen robustness-envelope prospective sub-analysis
The retrospective Phase 22A robustness surface identified the 30-member envelope ITM3–ITM7 × NEXT2/NEXT3 × K3 2.5/3/4. This sub-analysis freezes that entire region without selecting an individual member and evaluates it alongside the full 504-family.

Preliminary existing Phase 22B result (8 admitted expiries; n=6 completed observations/configuration): all 30 envelope members have positive cumulative net P&L, win rate >=83.33%, and zero recorded cumulative drawdown. Mean cumulative net P&L is approximately ₹94,845 and median approximately ₹90,885. These figures are **not confirmatory** because n=6 is below the frozen bootstrap minimum and far below the 30-cycle capital gate.

The next qualifying prospective cycles must be appended without changing the envelope. Every member will be reported separately and as an aggregate region. No member will be selected from this preliminary result.
