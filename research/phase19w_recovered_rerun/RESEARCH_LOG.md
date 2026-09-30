# Phase 19W Research Log

## 2026-09-30 — Phase prepared
- Created a separate Phase 19W branch for the empirical rerun that follows Phase 18W data recovery.
- Kept the full 224-variant family and all Phase 17W statistical/execution rules frozen.
- Added a manual GitHub Actions workflow; it is not being executed until Phase 18W establishes an admitted recovered-data revision and coverage record.
- No empirical conclusion has been changed.

## 2026-09-30 — Workflow correction
- Initial workflow text was malformed by host-language interpolation of GitHub expression syntax.
- Corrected before execution and logged as E19-001.

## 2026-09-30 — Phase 19W closure
- Authoritative GitHub Actions run 36642638097 completed successfully.
- All 224 preregistered configurations were evaluated on the recovered dataset.
- 13,956/14,112 variant-cycle cells were available (98.895%); each variant produced 36/63 usable strategy cycles (57.143%), with 21 training, 7 validation and 8 holdout observations.
- 193 variants had positive training mean, 136 positive validation mean and 180 positive holdout mean, but 0/224 satisfied the frozen promotion gate.
- No Holm-adjusted training p-value was below 0.05; 107 were below 0.10.
- Phase 19 is closed without capital promotion. The binding limitation is contract-level coverage/evidence completeness, not inability to execute the computation.
