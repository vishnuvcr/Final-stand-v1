# Phase 12W Status

## Branch
phase-12w-robustness

## State
Primary 30-cell empirical stress execution passed. Supplemental robustness diagnostics are implemented; the first follow-up run exposed and fixed a workflow command defect, and a serialized rerun is now executing.

## Observed primary stress result
- 63 usable weekly cycles were processed in each of the 30 slippage x stop-loss cells.
- Slippage grid: 0, 0.25, 0.50, 1.00, 2.00 index points per leg.
- Stop grid: none, 50, 100, 150, 200, 300 index points.
- Canonical completed workflow: Phase 12W run 81, artifact `phase-12w-robustness-81` (artifact id 11051125242).
- The frozen Phase 13 cell (0.50 slippage, 50-point stop) produced mean net P&L ₹3,488.06 per weekly cycle over all 63 cycles; its 14-cycle chronological test segment produced mean net P&L ₹1,566.04.
- The primary dataset is 1-minute OHLC reconstruction rather than observed historical bid/ask.

## Supplemental robustness protocol
- CSCV-style combinatorial cross-validation with 6 blocks, 3 test blocks and a 1-week purge.
- PBO proxy based on the test percentile of the training-selected configuration across combinatorial paths.
- Holm step-down multiple-testing correction across all 30 candidate cells.
- DSR-style multiple-testing/non-normality diagnostic, explicitly labelled as an approximation rather than exact byte-for-byte DSR replication.
- Structural regime conditioning by historical contract-rule era and lot-size regime, plus K3 target-error regime.
- Additional stop-gap stress overlay for 0/5/10/20 index points.
- Historical SPAN/peak-margin integration remains blocked, so no capital-normalized return is reported.

## Governance restriction
The Phase 13 stop is frozen from training only at 0.50-point slippage. Supplemental diagnostics cannot change that rule. The Phase 13 holdout was observed before this supplemental audit, so it is treated as a locked descriptive out-of-sample result and will not be used for any further tuning.

## Next gate
Complete the serialized supplemental workflow, inspect its artifact, then update Phase 13/main README and proceed to Phase 14 manuscript only after the robustness supplement and margin caveat are documented.