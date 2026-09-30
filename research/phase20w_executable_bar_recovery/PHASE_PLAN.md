# Phase 20W — Executable-Bar Recovery

## Research question
Can the 27 cycles missing from the Phase-19 executable path be recovered from independent, auditable sources without changing the frozen weekly strategy rules or introducing synthetic bars?

## Scope
1. Identify every missing cycle/leg/timestamp from Phase 19.
2. Audit HF-01, HF-02 and other public datasets for exact NIFTY option bars.
3. Where credentials are available, test Upstox/Dhan expired-option OHLC APIs as independent recovery routes.
4. Recover missing NIFTY spot expiry settlement bars separately.
5. Apply deterministic source precedence; never blend conflicting observations.
6. Validate timestamp, expiry, strike, option side, OHLC, volume/OI, duplicates and conflicts.
7. Produce a recovered executable-bar manifest with provenance and hashes.
8. Re-run the exact Phase-19 frozen 224 variants only after coverage admission.
9. Compare recovered-vs-original results and run the same bootstrap/Holm gate.
10. Stop this phase once recovery is exhausted or executable coverage reaches the frozen 50/63 gate threshold.

## Frozen strategy controls
Entry 10:00 IST; lock 14:00 IST; 50 NIFTY-point stop; 0.50 NIFTY-point slippage per leg; existing Paytm Money/NSE cost model; 224 variants; 37/12/14 chronology; block bootstrap length 3 with 3000 reps; Holm adjustment; no post-hoc gate changes.

## Source precedence
Primary: pinned HF-03 exact bars.
Secondary: independently versioned public HF sources where schema and timestamps permit exact reconstruction.
Credentialed broker APIs: recovery/validation only unless their raw observations can be archived with reproducible provenance.
Conflicts are logged and excluded from blending until resolved.

## Exit criteria
- Missing-cycle inventory complete.
- Every attempted source logged.
- Recovered bars either admitted with provenance or documented unavailable.
- Frozen rerun completed if coverage is admitted.
- Gate and limitations documented.
