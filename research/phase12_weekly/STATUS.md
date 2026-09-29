# Phase 12W Status

## Branch
phase-12w-robustness

## State
Implementation complete; execution depends on successful upstream data ingestion.

## Robustness design
- Chronological train/validation/test split.
- Weekly block bootstrap for mean P&L uncertainty.
- Annualized weekly Sharpe.
- Maximum drawdown.
- 95% expected shortfall.
- Stop-loss sensitivity.
- Slippage stress: 0, 0.25, 0.50, 1.00 and 2.00 index points per leg.
- No parameter is promoted to the final holdout from full-sample results.

## Restriction
This phase cannot establish robustness until Phase 11 produces admissible weekly trade results.


- 2026-09-29: corrected Phase 11 timestamp interface propagated to Phase 12; robustness execution retrigger pending after CI startup failures.
