# Phase 13W Status

## Branch
phase-13w-untouched-holdout

## State
Pipeline corrected after run 36595701035; awaiting re-execution.

## Selection
Mandatory stop selected from training only at fixed 0.50-point slippage.

## Latest execution note
Run 36595701035 ingested 100 expiry candidates and 63 USABLE_OHLC cycles, but generated zero backtest trades because the workflow did not pass Phase 9 data paths explicitly. This is logged as E-0028 and is not an empirical result.

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
