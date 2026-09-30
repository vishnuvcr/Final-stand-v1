# Final Stand v1 — Market Inefficiency Research

## Current status

Phase 21W combined frozen rerun completed on the currently admitted 82.93% executable-cell sample. The active next phase is external full-strike source recovery for the five missing weekly expiries.

The study evaluates a deterministic weekly NIFTY call-ladder-to-spread strategy with explicit transaction costs, slippage, chronological validation, an untouched holdout and preregistered multiple-testing controls.

### Phase status
- Phase 8W — weekly strategy definition: ✅
- Phase 9W — weekly data gate: ✅ 63 chronological weekly cycles
- Phase 10W — mechanics, margin and costs: ✅
- Phase 11W — weekly backtest: ✅
- Phase 12W — robustness: ✅
- Phase 13W — frozen stop and untouched holdout: ✅
- Phase 14W — final manuscript: ✅
- Phase 15W — historical execution-data discovery: ⚠️ no qualifying free historical weekly-options BBO archive
- Phase 16W — capital/margin validation: ⏳ downstream
- Phase 17W — K1/K2/K3 alternatives: ✅ 224 configurations evaluated
- Phase 20W — public executable-bar recovery: ✅ 11,702/14,112 variant-cycle cells admitted
- Phase 21W combined frozen rerun: ✅ 224 variants; 0/224 passed the preregistered promotion gate
- Phase 21W external full-strike recovery: 🔄 active

### Phase 21W combined result
- 11,702/14,112 variant-cycle cells were executable (82.93%).
- 58/63 weekly expiries are currently covered; 5 remain completely unrecovered.
- 0/224 variants had Holm-adjusted training p < 0.05.
- 0/224 variants were promoted to the capital phase.
- The backtest remains OHLC-based rather than historical bid/ask fill validation.

### Canonical artifacts
- [Phase 21W combined results](research/phase21w_combined_frozen_rerun/RESULTS.md)
- [Phase 21W status](research/phase21w_combined_frozen_rerun/STATUS.md)
- [Phase 21W research log](research/phase21w_combined_frozen_rerun/RESEARCH_LOG.md)
- [Phase 21W error log](research/phase21w_combined_frozen_rerun/ERROR_LOG.md)
- [Phase 21W variant summary](research/phase21w_combined_frozen_rerun/output/variant_summary.json)
- [Phase 21W coverage](research/phase21w_combined_frozen_rerun/combined_input/coverage.json)
- [Phase 21W external recovery plan](research/phase21w_external_full_strike_recovery/PHASE_PLAN.md)
- [Phase 21W external recovery status](research/phase21w_external_full_strike_recovery/STATUS.md)
- [Research execution log](research/logs/RESEARCH_LOG.md)
- [Error log](research/logs/ERROR_LOG.md)

## Research governance
All phases remain on separate branches. Empirical workflows use manual dispatch controls; large generated datasets are kept as workflow artifacts when GitHub's single-file limit prevents direct persistence.
