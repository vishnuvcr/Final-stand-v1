# Phase 21W Research Log

## 2026-09-30 — E21-013 validation run
- The E21-013 schema correction was executed in workflow run 36707810280.
- The Python adapter passed dependency setup and reached combined-input construction, but the runner received a shutdown signal during the streaming-free builder implementation before coverage validation.
- No Python data/schema exception was emitted in the job log and no empirical backtest result was produced.
- The event is treated as an execution-resource failure, not an empirical finding.
- Builder redesign: use `scan_parquet`/lazy expressions for both large option tables; perform source-local duplicate queries in streaming mode; stream normalized HF-02 output to a temporary parquet; then stream-concatenate HF-03 and HF-02 to the final combined parquet.
- The frozen 224-variant family, 63-cycle chronology, train/validation/holdout split, strike definitions, stop, slippage, costs and statistical gate remain unchanged.

## 2026-09-30 — E21-015 coverage-contract correction
- Workflow run 36708232073 completed the bounded-memory combined-input build successfully.
- Reported coverage: 8,064 HF-03 variant-cycle cells + 3,638 HF-02 usable recovered cells = 11,702 combined cells; zero overlap; zero source-local duplicate groups.
- The validator then failed because it required `combined_unique_expiries==63`. The executable combined set has 58 expiries because five of the frozen 63 baseline expiries remain completely unrecovered.
- Correction: validate the frozen denominator of 63 baseline expiries separately from the currently executable subset, requiring exactly five missing baseline expiries and no unexpected expiries. No strategy or data values were changed.

## 2026-09-30 — E21-016 Phase-9 artifact path correction
- Coverage validation passed in workflow run 36708651392 with the expected 63 baseline expiries, 11,702 combined variant-cycle cells, 58 covered expiries and 5 missing expiries.
- The frozen backtest then failed before any trades because the downloaded Phase-9 artifact was extracted to `phase9_weekly/output`, while the frozen engine searches `research/phase9_weekly/output` (or `prepared/phase9`) for the selected spot interface.
- Correction: extract the prepared artifact under `research/`, preserving its original internal paths. This restores the exact Phase-9 interface expected by the frozen backtester without changing data or strategy parameters.

## 2026-09-30 — E21-017 Phase-9 baseline path mismatch
- Workflow run 36708865255 failed before reading any option bars because `build_combined.py` still referenced `phase9_weekly/output/weekly_cycle_manifest.csv` after the workflow was correctly changed to restore the Phase-9 artifact under `research/`.
- Correction: update the builder's frozen-baseline manifest path to `research/phase9_weekly/output/weekly_cycle_manifest.csv`. No source data or strategy parameter changed.

## 2026-09-30 — E21-018 repository persistence limit
- Workflow run 36709072723 completed the exact frozen 224-variant backtest and uploaded the results artifact successfully.
- The final commit/push failed only because `research/phase21w_combined_frozen_rerun/combined_input/variant_option_bars.parquet` is 346.32 MB and GitHub rejects individual files over 100 MB.
- Correction: commit the compact coverage/manifest files and all backtest output summaries/trades, while retaining the full combined parquet in the successful workflow artifact. The combined parquet is deterministically reproducible from the pinned HF-03 artifact and admitted HF-02 source.
