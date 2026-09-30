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


## E22B-020 — Robustness envelope cannot yet be statistically confirmed
- Date: 2026-10-01
- Frozen prospective envelope contains 30 configurations.
- Existing qualifying prospective data provide n=6 per configuration.
- Although all 30 are positive with win rate >=83.33% in this short sample, the frozen bootstrap minimum and 30-cycle capital gate are not met.
- Correction: retain all 30 members unchanged and continue chronological source recovery. No member is promoted or selected.
