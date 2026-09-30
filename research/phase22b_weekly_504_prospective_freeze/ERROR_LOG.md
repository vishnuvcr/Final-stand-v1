# Phase 22B Error / Recovery Log

## E22B-018 — Prospective window extension hit option-data coverage ceiling
- Date: 2026-10-01
- Trigger: prospective boundary extended to 2026-09-08.
- Workflow: 36763880416
- Result: successful workflow, but only 8 qualifying weekly expiries were admitted, ending 2026-07-21.
- Diagnosis: the requested date boundary exceeded the qualifying free option-data coverage available to the current source set.
- Impact: every configuration remained at n=6; bootstrap/Holm inference and capital promotion remained gated.
- Resolution: keep the frozen strategy unchanged; search additional approved sources before rerunning.
- Prevention: verify expiry-level source coverage before interpreting a date-window extension.

## E22B-017 — Prospective bootstrap minimum unmet
- Status: open as a statistical coverage limitation.
- Each configuration has n=6; frozen bootstrap requires n>=8.
- No post-hoc statistical relaxation permitted.
