# Phase 21W Error Log

## E21-001 — 2026-09-30
- **Issue:** HF-02 recovered cycle manifest lacks Phase-9 `prior_expiry` and `status` columns required by the frozen backtester interface.
- **Impact:** Combined-input construction stopped before backtesting.
- **Correction:** Join those fields from the frozen 63-cycle Phase-9 calendar by `target_expiry`. No strategy/data values changed.

## E21-002 — 2026-09-30
- **Issue:** HF-02 recovered bars use `oi` while the HF-03 frozen bar interface uses `open_interest`.
- **Impact:** Combined-input construction stopped before coverage validation.
- **Correction:** Rename `oi` to the frozen interface field `open_interest` at the adapter boundary; values are unchanged.

## E21-003 — 2026-09-30
- **Issue:** The third Phase-21 run was cancelled during a redundant HF-03 interface rebuild.
- **Impact:** No empirical result was produced.
- **Correction:** Reuse the prepared HF-03 interface artifact and the admitted Phase-20 HF-02 recovery overlay. The frozen calendar and strategy parameters remain unchanged.

## E21-004 — 2026-09-30
- **Issue:** Phase-19 persisted outputs did not include the intermediate `variant_option_bars.parquet` required for exact re-execution.
- **Impact:** A direct persisted-input overlay could not reproduce the original OHLC backtest interface.
- **Correction:** Rebuild the frozen HF-03 interface once from its pinned revision, then overlay admitted HF-02 cycles.

## E21-005 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the derived `trading_day` field required by the HF-03 interface.
- **Correction:** Derive `trading_day` from the recovered bar timestamp at the adapter boundary.

## E21-006 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the static `symbol` field required by the HF-03 interface.
- **Correction:** Set `symbol='NIFTY'` for HF-02 rows at the adapter boundary.

## E21-007 — 2026-09-30
- **Issue:** HF-02 recovered bars lack `option_type` in the frozen interface.
- **Correction:** Set `option_type='CE'` because the recovered HF-02 files are weekly NIFTY `*_CE` files.

## E21-008 — 2026-09-30
- **Issue:** GitHub cancelled two Phase-21 runs during the expensive HF-03 interface rebuild.
- **Correction:** Split preparation from the combined rerun and reuse the prepared interface artifact.

## E21-009 — 2026-09-30
- **Issue:** The prepared HF-03 interface built successfully, but persisting its large files to the branch failed.
- **Correction:** Use the successful preparation workflow artifact as the transport layer.

## E21-010 — 2026-09-30
- **Issue:** HF-02 recovered bars expose `expiry` while the frozen interface also requires an `expiry` field.
- **Correction:** Preserve/add `expiry` as the same weekly contract date represented by `target_expiry`.

## E21-011 — 2026-09-30
- **Issue:** Conditional expiry normalization was initially inserted in the wrong order and interacted with an already-present `target_expiry` field.
- **Correction:** Ensure the frozen `expiry` field exists before bar-schema validation; do not alter the contract date.

## E21-012 — 2026-09-30
- **Issue:** The combined-bar build became unnecessarily slow when every HF-02 bar was joined to cycle metadata and the complete combined bar table was grouped for duplicate checks.
- **Impact:** No empirical result was produced.
- **Correction:** Remove the large metadata join and validate duplicates source-locally before concatenation.

## E21-013 — 2026-09-30
- **Issue:** Workflow run 36706822914 failed in `build_combined.py` because the HF-02 reconstructed bar parquet lacks the repeated HF-03 interface fields `entry_timestamp`, `lock_timestamp`, and `k3_multiplier`.
- **Impact:** Coverage validation and the exact frozen 224-variant backtest were skipped; no empirical result was produced.
- **Root cause:** E21-012 removed the prior metadata join to solve the large-join performance problem, but the replacement did not recreate the three non-price metadata columns required by the frozen bar schema.
- **Correction:** Reconstruct `entry_timestamp` and `lock_timestamp` from the compact recovery manifest keyed by `target_expiry`, and reconstruct `k3_multiplier` from the registered variant id. Reject nulls and retain source-local duplicate validation.
- **Prevention:** Future schema optimizations must compare the complete target column contract before removing an adapter stage; source price/timestamp/strike data remain immutable and only schema metadata may be derived from the admitted same-source manifest.
