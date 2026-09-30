# Phase 22B Error Log

## E22B-001 — Execution-aware data still unavailable
- The available public NIFTY source provides OHLCV(+OI), not historical bid/ask/depth.
- Correction: Phase 22B labels the result as OHLC validation and retains execution-aware validation as a separate gate.

## E22B-002 — Short new-period sample
- The public archive currently reaches 2026-08-04, yielding only a limited number of weekly expiries after the Phase-21 sample.
- Impact: the new period cannot satisfy the existing 30-cycle capital-promotion minimum.
- Correction: evaluate the full frozen 504-family anyway for prospective evidence, but do not promote capital from this phase.

## E22B-003 — Push-triggered workflow inputs were empty
- Observed: GitHub Actions exposes `inputs.*` only for workflow_dispatch. The controlled push run therefore passed empty environment variables.
- Impact: the run stopped before data acquisition with an integer-conversion error.
- Correction: workflow environment variables now use explicit defaults when dispatch inputs are absent. The manual workflow_dispatch interface remains available.

## E22B-004 — TradeMarkk post-Phase-21 NIFTY file coverage was insufficient
- Observed: the source-catalog discovery over 2026-05-19..2026-08-04 admitted only one weekly expiry from TradeMarkk's NIFTY expiry-file tree.
- Impact: it could not provide a meaningful new weekly validation window.
- Correction: the prospective phase switched acquisition to RISSIN's current 2026 NIFTY 1-minute archive, which documents year-level intraday coverage and expiry/strike/CE/PE/OHLC/volume fields. The 504 family and trading protocol were not changed.

## E22B-005 — Source gaps must not redefine the trading calendar
- Observed: RISSIN contains only 7 of the weekly expiries in the requested post-Phase-21 window.
- Risk: deriving the prior expiry from available source files would incorrectly move entry dates backward whenever an expiry file is missing.
- Correction: the prospective builder now derives the prior weekly expiry from the frozen Tuesday weekly calendar relation (target expiry minus 7 days) for this period. Missing source files cause a missing cycle, not a calendar shift.

## E22B-006 — RISSIN timestamp timezone mismatch in lazy filtering
- Observed: the annual RISSIN file reports timestamps with a +05:30 timezone representation that Polars would not directly compare with an Asia/Kolkata literal inside the lazy scan.
- Impact: prospective data extraction stopped before cycle construction.
- Correction: the annual file is now date-filtered using its canonical date field before collection; timestamps are normalized only after materialization.

## E22B-007 — Polars nested timezone literals in coverage check
- Observed: using `Expr.is_in([timezone-literal, timezone-literal])` produced a nested-object construction error.
- Impact: the run stopped after loading the weekly option data, before completing cycle admission.
- Correction: the exact entry/lock coverage check now uses two explicit equality predicates joined with OR.
