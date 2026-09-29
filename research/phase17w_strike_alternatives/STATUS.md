# Phase 17W — K1/K2 Strike Alternatives

## State
Active — the phase has been expanded to a preregistered 224-configuration family: 8 K1 rules × 4 K2 rules × 7 K3 multipliers.

## Why this phase exists
The weekly strategy's K1/K2 selection has a material structural effect on K3, D, entry cash flow and risk. The current implementation uses OTM1 + NEXT1. The user requested testing of alternatives.

## Integrity rules
- Phase 13W untouched holdout remains locked.
- Existing Phase 12/13 results are immutable historical evidence.
- No Phase 16W margin result will be silently mixed into this phase.
- No BBO substitution.
- No post-hoc expansion of the registered variant family.
- Holdout cannot be used for selection.

## Registered family
8 K1 rules × 4 K2 rules × 7 K3 multipliers = 224 configurations.

## Current gate
ALTERNATIVE BACKTEST: RUNNING / restarting after registered K3 expansion.

## Planned sequence
1. Re-read protocol and verify branch artifacts.
2. Build full-call-chain variant manifests using the existing cached HF data route.
3. Run the existing cost/slippage/stop engine at 0.50 points/leg and 50-point stop.
4. Run deterministic tests and coverage diagnostics.
5. Compute training/validation/holdout statistics.
6. Compute centered moving-block bootstrap p-values on training data and Holm-adjust across 224 variants.
7. Apply the preregistered promotion gate without using holdout outcomes.
8. Update results, logs, main README and downstream-phase recommendation.

## Latest execution
- Previous 32-variant workflow runs were superseded by the registered K3 expansion.
- Current registered family: 224 configurations.
- Phase 9 data gate remains fixed at 63 usable baseline cycles.
- Latest corrected run will cancel older in-progress Phase 17W runs through workflow concurrency.
- No alternative empirical result has been admitted yet.

## Exit state
The phase closes after the 224-configuration family is evaluated and the promotion gate is applied. No second optimization loop is opened automatically.
