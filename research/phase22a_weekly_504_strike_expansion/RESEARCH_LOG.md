# Phase 22A Research Log

## 2026-09-30 — Weekly 504-family extension initiated
- User instruction changed the requested evaluation to an explicit weekly-trade framing and widened the K1 strike range through OTM8 and ITM8.
- The existing Phase-22 registry was already weekly-horizon, so the change was implemented as a separately branched parameter-expansion phase rather than rewriting the frozen 224-family history.
- Frozen family: 18 K1 rules × 4 K2 rules × 7 K3 values = 504 configurations.
- The test uses the immutable Phase-21 63-expiry recovered historical interface so that this run isolates K1-range expansion.
- The earlier Phase-21 historical holdout is not relabeled as a new holdout.
- No configuration selection is performed before the full 504-family run.

## 2026-09-30 — Pre-run compatibility corrections
- Source inspection found that the inherited Phase-17 K1 selector was hard-coded to ranks 1–3; the wrapper was corrected to support ranks through 8.
- The Phase-21 recovery artifact did not contain the required Phase-9 interface files; the workflow was changed to source the frozen manifest and spot interface from the combined branch.
- The inherited engine contained a dataset-revision mismatch between TheTrademarkk and RISSIN; the custom Phase 22A builder now uses source-specific revisions and SHA checks.
- Shared source bars replaced an unnecessary per-variant replication design.
- RISSIN duplicate identity was corrected to include expiry.
- Asia/Kolkata timestamp casts were made explicit for all entry/range comparisons.
- All corrections were logged in ERROR_LOG.md before interpreting final results.

## 2026-09-30 — Final 504-configuration run completed
- GitHub Actions run 36741881293 completed successfully.
- Registry validation passed with exactly 504 configuration IDs.
- Backtest executed all 504 configurations over all 63 weekly expiries.
- Every configuration achieved 63/63 valid cycles.
- 414/504 had positive training P&L; 239/504 positive validation P&L; 308/504 positive historical-holdout P&L.
- 323/504 raw bootstrap p-values were below 0.05, but 0/504 Holm-adjusted p-values were below 0.05.
- Minimum Holm-adjusted p-value was 0.167944.
- No configuration passed the capital-promotion gate.
- Full result tables, parameter surfaces, manuscript and static charts were published.
- Workflow artifact: phase22a-weekly-504-results, artifact ID 11111230842, digest sha256:1a250f5ca0a39aaefb3b293758eedc41293387e720cf65491e720a5cdb243964.
- Phase 22A is closed as a retrospective parameter-expansion phase. The next evidence layer remains a genuinely new chronological validation, preferably execution-aware.


## 2026-10-01 — Economic robustness reinterpretation
- User clarified that the objective is not to find a statistically significant winner among 504 configurations.
- The 504 configurations are retained as a robustness grid for traceability: profitability, win rate, profit factor, drawdown, expectancy and execution-cost resilience are the primary descriptive dimensions.
- The completed 63-week trade-level artifact was downloaded from workflow run 36741881293 and independently recalculated.
- Baseline breadth: 367/504 positive total net P&L; 300/504 >=50% win rate; 431/504 max drawdown <=₹150k.
- Additional all-in execution-cost stress was applied using recorded order counts and lot sizes. At +3 points/order, 305/504 configurations remained positive.
- A data-quality audit found 39 missing net-P&L fields across 24 configurations. No imputation was performed.
- Holm remains retained for inferential completeness but is no longer treated as the primary economic robustness gate.
