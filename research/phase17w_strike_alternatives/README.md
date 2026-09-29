# Phase 17W — K1/K2 Strike-Selection Alternatives

This phase evaluates 224 preregistered K1/K2/K3 definitions while preserving the original weekly strategy as a frozen control.

## Scope
The experiment varies only:
- K1 moneyness/location rule;
- K2 spacing rule.

K3 selection uses a preregistered multiplier family; timing, stop, slippage, transaction-cost model and weekly chronology remain fixed.

## Outputs
- PHASE_PLAN.md — preregistered methodology and stopping rule.
- STATUS.md — live phase state.
- VARIANT_REGISTRY.md — exact 32-configuration matrix.
- strike_alternatives.py — deterministic data builder and analysis engine.
- test_strike_alternatives.py — unit tests.
- research/logs/RESEARCH_LOG.md — auditable research decisions.
- research/logs/ERROR_LOG.md — auditable errors and corrective actions.
- workflow artifacts — machine-readable variant results.

## Evidence boundary
The Phase 13W holdout remains locked and is used here only for descriptive post-analysis reporting. No variant is promoted using holdout performance.

## Baseline control
OTM1_NEXT1_K3M2 exactly matches the currently frozen K1/K2/K3 definition used in the historical Phase 13W evidence.


## K3 multiplier family
The target K3 premium is M × (P1 − P2), with M ∈ {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0}. The current baseline is M=2.0.
