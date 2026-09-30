# Final Stand — Quantitative Research

## Current research status
**Phase 22B — Weekly 504 Prospective Validation**

- Frozen configuration family: **504**
- Weekly protocol: frozen
- Historical 63-cycle expansion (Phase 22A): complete
- Prospective extension run: **36763880416 — successful**
- Requested prospective boundary: 2026-09-08
- Qualifying weekly expiries actually admitted: **8**, ending 2026-07-21
- Variant-cycle rows: **4,032 / 4,032 usable**
- Configurations with positive total prospective net P&L: **376 / 504**
- Completed observations per configuration: **n=6**
- Bootstrap/Holm confirmation: **not yet available** because the frozen bootstrap requires at least 8 observations
- Capital promotion: **not reached**; existing minimum is 30 completed cycles
- Configuration selection: **none**

The September 8 extension did not add qualifying weekly option cycles. This is recorded as a **data-coverage limitation**, not as evidence for or against a strategy configuration.

## Research records
- [Phase 22B plan](research/phase22b_weekly_504_prospective_freeze/PHASE_PLAN.md) — frozen prospective methodology and gates.
- [Phase 22B status](research/phase22b_weekly_504_prospective_freeze/STATUS.md) — latest validation state and interpretation boundary.
- [Phase 22B research updates](research/phase22b_weekly_504_prospective_freeze/RESEARCH_UPDATES.md) — chronological research-step updates.
- [Phase 22B error log](research/phase22b_weekly_504_prospective_freeze/ERROR_LOG.md) — recorded errors and recoveries.

## Research principles
1. Test the complete frozen 504 family; do not select configurations from the holdout.
2. Keep historical and prospective evidence separate.
3. Account for slippage, brokerage and transaction costs.
4. Prefer cached, pinned datasets and record source revisions/hashes.
5. Search approved independent data sources before treating missing data as strategy failure.
6. Do not change statistical gates after observing results.
7. Stop only at the pre-specified research gates and provide a complete manuscript at the end.
