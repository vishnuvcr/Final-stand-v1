# Phase 22A Error Log

## E22A-001 — Configuration-family expansion changes the multiple-testing family
- Observed: extending K1 from 8 rules to 18 rules increases the total family from 224 to 504.
- Impact: the earlier 224-way Holm-adjusted inference cannot be reused for the expanded family.
- Correction: this phase declares one 504-configuration family and recomputes the multiple-testing correction across all 504 configurations.

## E22A-002 — Weekly strategy wording needed to remain consistent
- Observed: prior discussion sometimes used the shorthand intraday strategy.
- Correction: all Phase 22A documentation uses weekly-horizon weekly-expiry strategy with intraday execution timestamps.
- No rule change: entry/lock timestamps remain the frozen weekly protocol.

## E22A-003 — Old holdout cannot be called new out-of-sample evidence
- Observed: the Phase-21 63-expiry dataset includes the historical holdout already examined in the completed 224-family study.
- Impact: testing 504 variants on it is a parameter-expansion/reassessment, not a fresh unseen-data validation.
- Correction: keep any future post-Phase-21 period reserved as the separate unseen validation layer.