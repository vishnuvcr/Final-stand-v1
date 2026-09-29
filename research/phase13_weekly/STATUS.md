# Phase 13W Status

## Branch
phase-13w-untouched-holdout

## State
Design implemented; awaiting workflow execution.

## Selection
Mandatory stop selected from training only at fixed 0.50-point slippage.

## Required outputs
- frozen stop-loss rule;
- train / validation / holdout net P&L;
- win rate;
- maximum drawdown;
- expected shortfall;
- weekly Sharpe;
- trade count and cost burden;
- target-error distribution;
- lock frequency;
- stop frequency;
- explicit data-quality and OHLC-reconstruction limitations.

## Restriction
No holdout observation may influence parameter selection.
