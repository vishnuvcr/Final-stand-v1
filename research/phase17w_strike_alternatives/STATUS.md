# Phase 17W — K1/K2 Strike Alternatives

## State
Closed — 224 registered configurations evaluated; no variant passed the preregistered promotion gate.

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

ALTERNATIVE BACKTEST: OPTIMIZED AFTER RUNNER CANCELLATION; FORCE-TRIGGERING CLEAN PUSH RUN

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
- Run 36625523052 completed input construction/merge but variant evaluation hit runner memory limits (E-0059); no empirical result was admitted.
- Memory-bounded variant execution was committed at d63931f7213a24c90da4d959cd1004ac97bc0571; the next push-triggered run is the validation run.
- No alternative empirical result has been admitted yet.

## Exit state
The phase closes after the 224-configuration family is evaluated and the promotion gate is applied. No second optimization loop is opened automatically.
