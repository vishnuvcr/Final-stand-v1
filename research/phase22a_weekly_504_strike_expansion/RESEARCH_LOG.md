# Phase 22A Research Log

## 2026-09-30 — Weekly 504-family extension initiated
- User instruction changed the requested evaluation to an explicit weekly-trade framing and widened the K1 strike range through OTM8 and ITM8.
- The existing Phase-22 registry was already weekly-horizon, so the change is implemented as a separately branched parameter-expansion phase rather than rewriting the frozen 224-family history.
- Frozen family is 18 K1 rules × 4 K2 rules × 7 K3 values = 504 configurations.
- The test uses the immutable Phase-21 63-expiry recovered historical interface so that this run isolates K1-range expansion.
- The earlier Phase-21 14-cycle holdout is not relabeled as a new holdout.
- No configuration selection is performed before the full 504-family run.
## 2026-09-30 — Pre-run compatibility correction
- Source inspection found that the inherited Phase-17 K1 selector was hard-coded to ranks 1–3.
- The wrapper was corrected to inject a generalized OTM/ITM rank selector through rank 8.
- The registry remains 504; no K2/K3, execution, cost, split or statistical rule changed.
- The correction was logged as E22A-004 before interpreting any 504 result.