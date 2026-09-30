# Phase 20W Error Log

No Phase 20 execution errors yet.

## Methodological controls
- Never replace a primary HF-03 observation with an alternate source when the primary observation exists.
- Never interpolate or synthesize missing option prices.
- Log all schema, timestamp, strike, expiry, duplicate, conflict, and provenance failures.


## E20-001 — 2026-09-30
- **Issue:** The first Phase 20 inventory run passed the short HF commit prefix `f90f7ac` to the Hub tree API, which returned 404.
- **Impact:** Source inventory stopped before any files were examined.
- **Correction:** Pin the full verified commit SHA `f90f7acad633ba5a803f25cf431fb5f13ce3d162` for Recovery-1. The public archive and commit page confirm the dataset and revision. No data were downloaded or altered.
