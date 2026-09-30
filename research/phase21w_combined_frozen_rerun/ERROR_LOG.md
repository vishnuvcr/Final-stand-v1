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
- **Issue:** Workflow run 36706822914 failed because the HF-02 bar adapter lacked repeated HF-03 interface fields `entry_timestamp`, `lock_timestamp`, and `k3_multiplier`.
- **Correction:** Reconstruct these fields from the admitted cycle manifest and registered variant id without restoring the large metadata join.

## E21-014 — 2026-09-30
- **Issue:** Workflow run 36707810280 was cancelled by the GitHub-hosted runner during combined-input construction; the job log reported `The runner has received a shutdown signal` and no Python traceback.
- **Impact:** Coverage validation and the exact frozen 224-variant backtest were skipped; no empirical result was produced.
- **Diagnosis:** Most consistent with runner/resource termination during large-table construction; this is an execution diagnosis, not a proven root cause.
- **Correction:** Replace eager `read_parquet`/in-memory concatenation with Polars lazy `scan_parquet`, streaming source-local duplicate queries, a streamed normalized HF-02 parquet, and streamed vertical concatenation.
- **Prevention:** Phase-21 large-file adapters must remain streaming/bounded-memory end-to-end; do not materialize both frozen and recovered bar tables simultaneously.

## E21-015 — 2026-09-30
- **Issue:** Workflow run 36708232073 built the combined input successfully but the coverage validator asserted that the executable combined set must contain all 63 expiries.
- **Impact:** The exact frozen backtest was skipped even though the admitted combined dataset met the planned 11,702-cell threshold.
- **Root cause:** The validator conflated the frozen 63-expiry experimental denominator with the subset of expiries for which executable bars have been recovered. Five baseline expiries remain completely unrecovered.
- **Correction:** Validate 63 baseline expiries plus exactly five missing expiries, while requiring at least 11,702 combined variant-cycle cells and zero unexpected-expiry/overlap conditions.
- **Prevention:** Coverage validators must distinguish baseline chronology, executable observations, and missing observations as separate fields.
