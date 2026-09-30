# Phase 21W Status

**State:** EXECUTING — deterministic combined-source rerun in progress.

**Frozen calendar:** 63 exact expiries from Phase 19 `baseline_calendar.json`.

**Source precedence:** HF-03 pinned primary; HF-02 pinned recovery only for the 27 previously missing expiries; no source blending; missing cells preserved.

**Expected executable coverage before backtest:** 11,702/14,112 variant-cycle cells (82.93%), comprising 55 fully covered expiries, 3 partial expiries, and 5 fully missing expiries.

**Frozen controls:** 224 variants; 37/12/14 chronology; 10:00 entry; 14:00 lock; 50-point stop; 0.50-point slippage per leg; Paytm Money/NSE cost model; 3000-rep block bootstrap; Holm adjustment; unchanged promotion gate.

**Next:** complete combined build, run all 224 variants, validate coverage/costs/statistics, and close the phase with the final gate.
