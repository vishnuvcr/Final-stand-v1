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


## E22C-001 — Public-source coverage claim not yet independently qualified
- Date: 2026-10-01
- Candidate: Cloud Trader Pro / Shoonya Trader public expired-options dataset.
- Claim: 1-minute NIFTY expired options with OHLCV + OI, including weekly/monthly expiries and all strikes.
- Limitation: exact machine-readable 2026 expiry coverage and provenance are not established from public documentation alone.
- Action: do not admit candidate data until expiry, schema, duplicate, hash and overlap checks pass.


## E22C-002 — Free sample download could not be machine-ingested in this run
- Date: 2026-10-01
- Cloud Trader Pro links a free NIFTY sample to Google Drive.
- Web connector returned HTTP 401 when following the Drive file.
- Local runtime has no external-network/DNS access, so a second direct download path was unavailable.
- Impact: candidate schema/coverage could be documented from the public page but the sample bytes could not be hashed or empirically inspected in this run.
- Resolution: retain candidate as unadmitted; do not use it in Phase 22B/22C calculations.
