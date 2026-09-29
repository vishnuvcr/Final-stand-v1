# Phase 19W Error Log

## E19-001 — 2026-09-30
- **Issue:** Initial workflow template generation produced malformed GitHub Actions expressions because the file-generation code interpolated GitHub `${{ ... }}` tokens.
- **Impact:** The first committed workflow definition was syntactically invalid and was not executed.
- **Correction:** Replaced the workflow with a fixed manual `workflow_dispatch` job using the frozen 224-variant range. No empirical result was generated from the malformed workflow.
- **Prevention:** Future workflow generation treats GitHub expression syntax as literal configuration text.

## Inherited limitation
Phase 17W maximum usable coverage was 39/63 for the registered family. This remained a Phase 18W data-recovery question, not a Phase 19W empirical result.

## E19-002 — 2026-09-30
- **Issue:** Direct local execution could not reach Hugging Face because the runtime has DNS/network isolation (`NameResolutionError` for `huggingface.co`).
- **Impact:** No local empirical result was produced and no local result was substituted for the GitHub Actions/HF pipeline.
- **Correction:** The empirical rerun remains delegated to GitHub Actions, where `HF_TOKEN` and the existing cache are available.
- **Prevention:** Treat network-isolated local execution as a diagnostic only.

## E19-003 — 2026-09-30
- **Issue:** An early automatic trigger used an unsupported job-level `hashFiles()` gate.
- **Impact:** No empirical computation ran and no result was produced.
- **Correction:** Removed the unsupported gate; the Phase 18 admission record is the repository admission record.

## E19-004 — 2026-09-30
- **Issue:** The first live Phase 19 execution bridge reached the runner but failed with `ModuleNotFoundError: No module named 'research'`.
- **Impact:** No empirical computation ran and no output was admitted.
- **Correction:** Set `PYTHONPATH` to the checked-out repository workspace. No strategy, data, cost, or statistical parameter was changed.

## E19-005 — 2026-09-30
- **Issue:** The first run with the corrected module path failed because `research/phase9_weekly/output/weekly_cycle_manifest.csv` was not committed to the Phase 19 branch.
- **Impact:** The strategy code could not resolve the frozen 63-cycle baseline interface; no empirical result was produced.
- **Correction:** Phase 19 now rebuilds the frozen Phase 9 interface from the admitted HF-03 revision before the 224-variant rerun, validates exactly 63 usable cycles and nonempty frozen spot bars, and then runs the existing strategy unchanged.
- **Prevention:** Phase 19 no longer assumes generated Phase 9 artifacts are permanently present in the Git tree.


## E19-005 — 2026-09-30
- **Issue:** The Phase-9 frozen cycle manifest is generated output and is not present in the historical branches available to the Phase-19 runner.
- **Impact:** The exact 63-cycle calendar could not be consumed by the script, despite the frozen expiry list being present and independently versioned.
- **Correction:** Restoring a deterministic two-column manifest directly from the versioned `FROZEN_63_EXPIRIES.csv`, preserving its exact 63-expiry order. No synthetic market observations are created; this file is only the frozen calendar control input.


## E19-005 — 2026-09-30
- **Issue:** The corrected Phase 19 runner reached the strategy build but could not find `research/phase9_weekly/output/weekly_cycle_manifest.csv` on the Phase 19 branch.
- **Impact:** No empirical computation ran; the frozen Phase 9 interface had not been carried into this branch.
- **Correction:** The execution bridge now restores the exact frozen Phase 9 Actions artifact `11060261904` before execution, including `weekly_cycle_manifest.csv` and `selected_weekly_spot_bars.parquet`. The strategy and statistical parameters remain unchanged.


## E19-006 — 2026-09-30
- **Issue:** The Phase-9 selected weekly spot-bar parquet was also generated output and absent from the Phase-19 branch.
- **Impact:** The strategy runner could not reach the backtest stage.
- **Correction:** Added a deterministic restoration script that reconstructs the exact entry-to-lock NIFTY index slices from the pinned HF-03 `index/NIFTY.parquet` and the frozen 63-cycle calendar. No alternate spot source or synthetic prices are introduced.


## E19-006 — 2026-09-30
- **Issue:** After the frozen Phase 9 interface was restored, the empirical runner failed with `UnboundLocalError: option_source` because `main()` assigned `option_df` on the normal build path but later passed the undefined `option_source` to `run_variants()`.
- **Impact:** No empirical results were produced.
- **Correction:** Bound `option_source` to the generated `variant_option_bars.parquet`. This is an execution-variable fix only; the variant family, data, costs, slippage, stop, chronology, and statistics remain unchanged.


## E19-007 — 2026-09-30
- **Issue:** GitHub runner Polars rejected the HF parquet timezone metadata `+05:30` while restoring the NIFTY index (`POLARS_IGNORE_TIMEZONE_PARSE_ERROR` was not enabled).
- **Impact:** Spot-interface restoration stopped before reading market observations.
- **Correction:** Enable Polars timezone-parse compatibility for this frozen source format. This does not alter timestamps or strategy calculations; it only permits the existing parquet timezone metadata to be read.


## E19-007 — 2026-09-30
- **Issue:** The execution bridge invoked a recovery helper that attempted to reconstruct Phase 9 spot bars from HF-03 and failed on Polars timezone parsing of `+05:30`.
- **Impact:** No empirical results were produced.
- **Correction:** Removed the helper invocation. The bridge already restores the exact frozen Phase 9 `selected_weekly_spot_bars.parquet` artifact, so reconstruction is unnecessary and would introduce an avoidable data-path deviation.
