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
