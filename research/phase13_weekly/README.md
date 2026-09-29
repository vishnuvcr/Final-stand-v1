# Phase 13W — Untouched Weekly Holdout

## Purpose
Freeze one mandatory hard-stop rule using training data only, then evaluate that frozen rule on chronological validation and untouched holdout periods.

## Frozen selection protocol
- Candidate stops: 25, 50, 75, 100, 150, 200, 300 index points.
- Slippage used for selection: 0.50 index points per leg.
- Selection statistic: highest training-period mean net P&L.
- Tie-break: lower training maximum drawdown, then lower stop threshold.
- No-stop is not eligible because the research protocol requires a hard stop.
- Validation is descriptive only and cannot change the selected rule.
- Holdout is never used for rule selection.

## Margin dependency
The holdout result is not a return-on-capital result until dated NSE SPAN/peak-margin data are integrated.

## Decision gate
Phase 13 may produce a factual empirical result, including a negative result. It may not be used to tune the frozen stop after the holdout is inspected.
