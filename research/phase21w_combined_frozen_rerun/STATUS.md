# Phase 21W Status

**State:** PATCHED — corrected schema adapter is committed; deterministic combined-source rerun is the next execution gate.

- Phase 20 public-source recovery admitted 11,702/14,112 variant-cycle cells (82.93%).
- Source precedence: HF-03 pinned revision first; HF-02 pinned revision only for previously missing cells.
- No synthetic bars; no source blending within a variant-cycle.
- Frozen family: 224 variants; 63 chronological cycles; 37/12/14 train/validation/holdout; 10:00 entry; 14:00 lock; 50-point hard stop; 0.50-point/leg slippage; Paytm Money/NSE cost model; block bootstrap length 3, 3,000 reps; Holm adjustment.
- Run 36706822914 reached the combined build stage but failed before coverage validation because the HF-02 bar adapter did not supply `entry_timestamp`, `lock_timestamp`, and `k3_multiplier`.
- The correction preserves the source bars and frozen research parameters. The three fields are reconstructed at the adapter boundary from the admitted cycle manifest and registered variant ids, without reintroducing the large full-bar metadata join.
- Source-local duplicate validation and memory-bounded execution remain in place.
- Next gate: successful combined-input build, exact coverage validation, then the frozen 224-variant backtest/statistics.
