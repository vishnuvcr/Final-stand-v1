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
- **Correction:** Phase 21 will use the already-persisted Phase-19 HF-03 interface/results as its primary source and the admitted Phase-20 HF-02 recovery overlay, avoiding unnecessary redownload/rebuild. The frozen 63-cycle calendar and strategy parameters remain unchanged.

## E21-004 — 2026-09-30
- **Issue:** Phase-19 persisted outputs do not include the intermediate `variant_option_bars.parquet` required for exact re-execution.
- **Impact:** A direct persisted-input overlay cannot reproduce the original OHLC backtest interface.
- **Correction:** Rebuild the frozen HF-03 interface once from its pinned revision, then overlay admitted HF-02 cycles. The rebuild is data-interface reconstruction, not parameter retuning.

## E21-005 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the derived `trading_day` field required by the HF-03 interface.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Derive `trading_day` from the recovered bar timestamp at the adapter boundary; no timestamp or price values are modified.

## E21-006 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the static `symbol` field required by the HF-03 interface.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Set `symbol='NIFTY'` for HF-02 rows at the adapter boundary, matching the source instrument; no price/timestamp field is modified.

## E21-007 — 2026-09-30
- **Issue:** HF-02 recovered bars lack `option_type` in the frozen interface.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Set `option_type='CE'`, matching the recovered HF-02 NIFTY weekly call files. Added an explicit schema-difference guard after normalization.

## E21-007 — 2026-09-30
- **Issue:** HF-02 recovered bars lack `option_type`.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Set `option_type='CALL'`, matching the HF-02 recovery file and the frozen call-side strike-selection experiment.

## E21-008 — 2026-09-30
- **Issue:** GitHub cancelled two Phase-21 runs during the expensive HF-03 interface rebuild before the overlay stage.
- **Impact:** No combined empirical result from those runs.
- **Correction:** Split Phase 21 into a one-time HF-03 interface preparation job and a lightweight combined rerun job that reuses the persisted interface. This removes repeated long rebuilds while preserving the pinned source and frozen inputs.

## E21-009 — 2026-09-30
- **Issue:** The prepared HF-03 interface built successfully, but persisting its large files into the branch failed.
- **Impact:** The preparation workflow ended without a reusable branch copy.
- **Correction:** Use the successful preparation run artifact as the transport layer and consume it from Phase 21. No source or strategy change.

## E21-010 — 2026-09-30
- **Issue:** HF-02 recovered bars expose `expiry` while the HF-03 interface expects the same field under the frozen target-expiry schema.
- **Impact:** Overlay stopped at schema validation.
- **Correction:** Map `expiry` from `target_expiry` for HF-02 rows; no date values are changed.

## E21-007 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the `option_type` interface field.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Set `option_type='CE'` because the recovered HF-02 source files are explicitly the weekly NIFTY `*_CE` files. No price/timestamp data is changed.

## E21-008 — 2026-09-30
- **Issue:** HF-02 recovered bars expose the weekly contract expiry as `expiry`, while the frozen HF-03 interface expects the same value under `target_expiry`.
- **Impact:** Overlay construction stopped at schema validation.
- **Correction:** Map `expiry` to `target_expiry` for recovered rows; no value transformation or contract selection is changed.

## E21-009 — 2026-09-30
- **Issue:** The prior `expiry` normalization was inserted after the HF-02 bar-schema validation path, so the intended mapping was not applied.
- **Impact:** The same `expiry` error recurred.
- **Correction:** Normalize `expiry -> target_expiry` immediately after reading the HF-02 bar parquet, before any required-column validation.

## E21-010 — 2026-09-30
- **Issue:** HF-02 bars already contained `target_expiry` alongside redundant `expiry`; conditional renaming therefore left `expiry` and triggered the same schema check.
- **Correction:** Drop redundant `expiry` when `target_expiry` is already present.

## E21-011 — 2026-09-30
- **Issue:** The target HF-03 bar schema legitimately contains `expiry`; dropping HF-02's redundant `expiry` caused the validator to report it as missing.
- **Correction:** Preserve/add `expiry` as the same frozen weekly contract date represented by `target_expiry`.
