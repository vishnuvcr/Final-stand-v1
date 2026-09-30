# Phase 21W Status

**State:** PATCHED — streaming combined-input builder committed; rerun queued by workflow trigger.

- Phase 20 public-source recovery admitted 11,702/14,112 variant-cycle cells (82.93%).
- Source precedence: HF-03 pinned revision first; HF-02 pinned revision only for previously missing cells.
- No synthetic bars; no source blending within a variant-cycle.
- Frozen family: 224 variants; 63 chronological cycles; 37/12/14 train/validation/holdout; 10:00 entry; 14:00 lock; 50-point hard stop; 0.50-point/leg slippage; Paytm Money/NSE cost model; block bootstrap length 3, 3,000 reps; Holm adjustment.
- Run 36707810280 was cancelled by the GitHub runner during combined-input construction after the metadata-adapter fix; the job log shows a runner shutdown signal rather than a Python exception.
- The builder is now fully lazy/streaming for the large option parquets. It reconstructs the three repeated metadata fields, validates source-local duplicates, normalizes the HF-02 schema, and streams both sources into the combined parquet without materializing the full tables together.
- E21-014 records the runner-shutdown/resource event. No empirical result was produced by the cancelled run.
- Next gate: successful combined-input build, exact coverage validation, then the frozen 224-variant backtest/statistics.
