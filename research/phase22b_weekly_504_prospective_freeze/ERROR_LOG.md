# Phase 22B Error Log

## E22B-001 — Execution-aware data still unavailable
- The available public NIFTY source provides OHLCV(+OI), not historical bid/ask/depth.
- Correction: Phase 22B labels the result as OHLC validation and retains execution-aware validation as a separate gate.

## E22B-002 — Short new-period sample
- The public archive currently reaches 2026-08-04, yielding only a limited number of weekly expiries after the Phase-21 sample.
- Impact: the new period cannot satisfy the existing 30-cycle capital-promotion minimum.
- Correction: evaluate the full frozen 504-family anyway for prospective evidence, but do not promote capital from this phase.
