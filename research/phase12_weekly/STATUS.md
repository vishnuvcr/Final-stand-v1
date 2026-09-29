# Phase 12W Status

## Branch
phase-12w-robustness

## State
**Completed.** Primary 30-cell stress testing and the supplemental robustness audit both passed in canonical Phase 12 workflow run 94. The generated robustness outputs were successfully committed after adding a pre-push rebase.

## Primary stress matrix
- 63 usable weekly cycles in each of 30 cells.
- Slippage: 0, 0.25, 0.50, 1.00, 2.00 index points per leg.
- Stop-loss: none, 50, 100, 150, 200, 300 index points.
- Frozen Phase 13 cell: 0.50-point slippage per leg and 50-point stop.
- Frozen cell full-sample mean net P&L: ₹3,503.86/cycle; annualized weekly Sharpe 4.42.

## Multiple-testing and dependence diagnostics
- Holm step-down adjustment across all 30 candidate cells.
- Frozen cell block-bootstrap two-sided p = 0.0002; Holm-adjusted p = 0.006.
- CSCV-style diagnostic: 20 combinatorial paths, 6 blocks, 3 test blocks, 1-week purge; PBO proxy = 0.00.
- The PBO value is explicitly a proxy from the repository implementation, not an exact reproduction of the published PBO estimator.

## DSR-style diagnostic
- Frozen cell annualized weekly Sharpe: 4.42.
- DSR-style probability: 0.9892 with 30 trials.
- This is an approximation using a multiple-testing null Sharpe threshold and non-normality-adjusted probabilistic Sharpe ratio; it is not a byte-for-byte reproduction of published DSR code.

## Regime conditioning
- Contract-rule era: pre-2025-08-28 mean ₹4,275.11/cycle (n=43); post-2025-08-28 mean ₹1,845.67/cycle (n=20).
- Lot regime: 75-lot mean ₹3,969.05/cycle (n=52); 65-lot mean ₹1,304.76/cycle (n=11).
- Target-error regime: low ₹3,743.34/cycle, mid ₹4,183.50/cycle, high ₹2,584.73/cycle; each n=21.
- These subgroup estimates are descriptive and have materially different sample sizes; they are not parameter-selection criteria.

## Tail-gap stress
- Additional 0-point gap: mean ₹3,503.86/cycle.
- +5 points on stopped trades: ₹3,350.68/cycle.
- +10 points: ₹3,197.51/cycle.
- +20 points: ₹2,891.16/cycle.
- 26 of 63 trades were stopped in the frozen cell.

## Capital and execution caveats
- Execution quality: OHLC_RECONSTRUCTION; no historical bid/ask is available in the primary HF source.
- Historical NSE SPAN/peak-margin series remains unintegrated; therefore no capital-normalized return is reported.
- The Phase 13 holdout was observed before this supplemental audit. The holdout is locked descriptively and cannot be used for tuning.

## Canonical outputs
- research/phase12_weekly/robustness.json
- research/phase12_weekly/robustness_supplement.json
- research/phase12_weekly/weekly_grid_fast.py
- research/phase12_weekly/robustness_supplement.py

## Next gate
Phase 12 is closed. Phase 13 holdout is already completed and locked. Proceed to Phase 14 manuscript synthesis with explicit separation of training, validation, holdout, robustness diagnostics, execution-quality limitations and margin dependency.