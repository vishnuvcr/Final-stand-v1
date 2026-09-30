# Phase 22A Error Log

## E22A-001 — Configuration-family expansion changes the multiple-testing family
- Observed: extending K1 from 8 rules to 18 rules increases the total family from 224 to 504.
- Impact: the earlier 224-way Holm-adjusted inference cannot be reused for the expanded family.
- Correction: this phase declares one 504-configuration family and recomputes the multiple-testing correction across all 504 configurations.

## E22A-002 — Weekly strategy wording needed to remain consistent
- Observed: prior discussion sometimes used the shorthand intraday strategy.
- Correction: all Phase 22A documentation uses weekly-horizon weekly-expiry strategy with intraday execution timestamps.
- No rule change: entry/lock timestamps remain the frozen weekly protocol.

## E22A-003 — Old holdout cannot be called new out-of-sample evidence
- Observed: the Phase-21 63-expiry dataset includes the historical holdout already examined in the completed 224-family study.
- Impact: testing 504 variants on it is a parameter-expansion/reassessment, not a fresh unseen-data validation.
- Correction: keep any future post-Phase-21 period reserved as the separate unseen validation layer.
## E22A-004 — Initial 504 wrapper did not override the base K1 selector
- Observed: the frozen Phase-17 engine's original `choose_k1` implementation only recognized OTM1–OTM3 and ITM1–ITM3.
- Impact: simply expanding `K1_RULES` to OTM4–OTM8/ITM4–ITM8 would fail during data construction.
- Detection: source inspection before the full 504 backtest completed.
- Correction: Phase 22A now injects a generalized K1 selector supporting OTM1–OTM8 and ITM1–ITM8 while leaving K2, K3, execution, cost and statistical functions unchanged.
- The full 504 run is therefore restarted from the corrected wrapper.
## E22A-005 — Phase-21 recovery artifact did not contain the expected Phase-9 interface
- Observed: the downloaded Phase-21 external-recovery artifact contained the final rerun/output tree but not `research/phase9_weekly/output/weekly_cycle_manifest.csv` or `selected_weekly_spot_bars.parquet`.
- Impact: the first corrected 504 workflow stopped at the interface-location step before the backtest.
- Correction: use the immutable Phase-21 combined branch as the authoritative source for the frozen Phase-9 manifest and spot parquet, while retaining the pinned HF revision for option reconstruction. The workflow no longer depends on the external-recovery artifact for those two interface files.
## E22A-006 — Frozen engine source/revision mismatch
- Observed: the inherited Phase-17 engine's `DATASET_REPO` is `thetrademarkk/india-index-options-1m`, while the Phase-21 recovery revision `8f7739...` belongs to RISSIN. Passing that revision to the inherited builder produced a 404 revision-not-found error.
- Impact: the first 504 backtest did not start.
- Correction: Phase 22A now uses the exact TheTrademarkk source files for the 58 non-recovered expiries at the configured `main` revision with SHA-256 validation against the frozen Phase-9 manifest, and uses the pinned RISSIN revision only for the five externally recovered 2026 expiries.

## E22A-007 — Variant-bar replication would create unnecessary memory pressure
- Observed: an initial custom-builder design repeated every OHLC observation for every variant that used the strike.
- Impact: the 504-family would create a much larger intermediate parquet than necessary.
- Correction: the builder now writes each expiry/strike source observation once; the custom backtest runner maps the cycle-level variant strikes onto a shared per-expiry OHLC pivot.
## E22A-008 — RISSIN duplicate check initially ignored expiry identity
- Observed: the annual RISSIN NIFTY parquet contains multiple weekly option expiries sharing the same timestamp and strike. A duplicate check on only `(timestamp, strike)` therefore reported 79,066 false duplicate groups.
- Impact: the 504 run stopped before reading any per-expiry source.
- Correction: duplicate identity for the RISSIN annual file now includes `_expiry`; true duplicates within the same expiry/timestamp/strike remain a hard error.
## E22A-009 — Explicit IST casting required for Polars timestamp literals
- Observed: normalized option timestamps were `Datetime(..., Asia/Kolkata)`, while Polars converted Python timezone-aware literals to UTC during comparison.
- Impact: the 504 workflow stopped on the first weekly expiry with an incompatible timestamp comparison.
- Correction: entry and expiry-end literals are explicitly cast to `Datetime(us, Asia/Kolkata)` before filtering. No trading timestamp changed.
## E22A-010 — Entry timestamp literal also needed explicit IST casting
- Observed: the first timezone correction fixed the weekly range filter but the separate exact-entry filter still used a Python datetime literal that Polars interpreted as UTC.
- Impact: the 504 run stopped before K1/K2/K3 selection for the first expiry.
- Correction: the entry timestamp comparison now uses the same explicit `Datetime(us, Asia/Kolkata)` cast as the range filter.
## E22A-011 — RISSIN per-expiry filter retained the same UTC-literal mismatch
- Observed: the generic IST correction was applied to TheTrademarkk filtering and entry selection, but the special five-expiry RISSIN filter still compared an IST series to a UTC-converted Python literal.
- Impact: the workflow reached the first recovered expiry, then stopped before configuration construction.
- Correction: RISSIN's external entry/end literals are explicitly cast to `Datetime(us, Asia/Kolkata)`.