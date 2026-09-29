# Phase 13W Status

## Branch
phase-13w-untouched-holdout

## State
Backtest eligibility diagnostic required after run 36596109078; awaiting diagnostic rerun.

## Selection
Mandatory stop selected from training only at fixed 0.50-point slippage.

## Latest execution note
Run 36596109078 ingested 100 expiry candidates and 63 USABLE_OHLC cycles, but generated zero backtest trades even after explicit Phase 9 data paths were supplied. This is logged as E-0029 and is not an empirical result; a row-level data-interface diagnostic has been added.

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
