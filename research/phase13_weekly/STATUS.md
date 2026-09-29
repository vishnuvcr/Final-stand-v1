# Phase 13W Status

## Branch
phase-13w-untouched-holdout

## State
**Completed.** The frozen weekly stop rule was selected from training data only and the chronological validation and untouched holdout were successfully evaluated in Phase 13 workflow run 36600595100.

## Selection
- Slippage for selection: 0.50 index points per leg.
- Candidate hard stops: 25, 50, 75, 100, 150, 200, 300 index points.
- Frozen stop: 50 index points.
- Selection statistic: training mean net rupees; tie-break lower training maximum drawdown, then lower stop.
- Holdout was not used for selection.

## Empirical result
- Training: 37 cycles; total net P&L ₹180,867.62; mean ₹4,888.31/cycle; win rate 83.78%; annualized weekly Sharpe 6.82.
- Validation: 12 cycles; total net P&L ₹16,955.48; mean ₹1,412.96/cycle; win rate 75.00%; annualized weekly Sharpe 1.49.
- Untouched holdout: 14 cycles; total net P&L ₹21,924.63; mean ₹1,566.04/cycle; win rate 78.57%; annualized weekly Sharpe 2.02.
- All 63 cycles: total net P&L ₹219,747.72; mean ₹3,488.06/cycle; win rate 80.95%; annualized weekly Sharpe 4.37.
- Holdout maximum drawdown: -₹12,874.90.
- Holdout expected shortfall 95%: -₹12,874.90.

## Data-quality and capital caveats
- Execution quality is OHLC_RECONSTRUCTION; the primary HF source does not contain historical bid/ask.
- These rupee P&L figures are not returns on capital.
- Historical NSE SPAN/peak-margin series is still required before capital-normalized performance can be reported.
- The Phase 12 supplemental robustness audit was performed after the holdout was observed. Therefore the holdout is locked as a descriptive out-of-sample observation and cannot be used for any subsequent parameter tuning.

## Required manuscript treatment
Report the holdout as an observed historical reconstruction result, clearly separating it from live-fill performance and capital-normalized returns.