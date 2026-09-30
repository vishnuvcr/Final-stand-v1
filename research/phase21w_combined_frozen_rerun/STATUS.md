# Phase 21W Status

**State:** RUNNING — combined-source frozen 224-variant rerun.

- Phase 20 public-source recovery admitted 11,702/14,112 variant-cycle cells (82.93%).
- Source precedence: HF-03 pinned revision first; HF-02 pinned revision only for previously missing cells.
- No synthetic bars; no source blending within a variant-cycle.
- Frozen family: 224 variants; 63 chronological cycles; 37/12/14 train/validation/holdout; 10:00 entry; 14:00 lock; 50-point hard stop; 0.50-point/leg slippage; Paytm Money/NSE cost model; block bootstrap length 3, 3,000 reps; Holm adjustment.
- Current run: interface rebuild → deterministic overlay → coverage validation → exact backtest/statistics → artifact persistence.


## Preparation checkpoint — 2026-09-30
- HF-03 frozen interface preparation succeeded in run 36700360409 and produced the reusable artifact `phase21w-hf03-interface`.
- Combined experiment is now ready to consume the prepared artifact plus admitted Phase-20 HF-02 recovery.
