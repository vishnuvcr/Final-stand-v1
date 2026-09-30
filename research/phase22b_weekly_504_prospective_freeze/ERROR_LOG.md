# Phase 22B Error / Recovery Log

## E22B-018 — Prospective window extension hit option-data coverage ceiling
- Date: 2026-10-01
- Trigger: Prospective boundary extended from 2026-08-04 to 2026-09-08 without changing the frozen strategy.
- Workflow: 36763880416
- Result: workflow succeeded, but only 8 weekly expiries were admissible, ending 2026-07-21.
- Diagnosis: the requested date boundary is not equivalent to available qualifying weekly option history. The successful source manifest recorded no TradeMarkk option-fallback expiries.
- Impact: each of the 504 variants still has n=6; pre-specified bootstrap and Holm inference remain unavailable.
- Resolution: do not alter strategy parameters to manufacture more observations. Treat this as a data-coverage limitation and search approved external archives before the next prospective rerun.
- Prevention: every future extension must verify source-level weekly-expiry coverage before interpreting the resulting sample size.

## E22B-017 — Prospective bootstrap minimum unmet
- Status: open as a statistical coverage limitation.
- Each configuration has n=6; the frozen bootstrap requires n>=8.
- No post-hoc change to the statistical rule is permitted.
