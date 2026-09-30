# Phase 22A — Economic Robustness & Traceability Analysis

## Purpose
This analysis treats the 504 weekly configurations as a robustness grid, not as 504 candidates from which a statistically significant winner must be selected. Holm-adjusted inference remains an inferential diagnostic, but it is not the primary economic decision criterion.

## Research question
Does the weekly strategy show broad, traceable economic behavior across the frozen 504-configuration surface — including profitability, win rate, drawdown, profit factor, expectancy and resilience to additional execution costs — rather than depending on a narrow configuration?

## Baseline breadth
| Metric | Result |
|---|---:|
| Configurations | 504 |
| Weekly cycles/configuration | 63 |
| Positive total net P&L | 367/504 (72.8%) |
| Win rate >= 50% | 300/504 (59.5%) |
| Win rate >= 55% | 282/504 (56.0%) |
| Profit factor >= 1.2 | 352/504 (69.8%) |
| Maximum drawdown <= ₹150,000 | 431/504 (85.5%) |
| Additional cost buffer >= 1 point/order | 352/504 (69.8%) |
| Additional cost buffer >= 2 points/order | 323/504 (64.1%) |
| Median total net P&L | ₹109,249 |
| Median win rate | 61.9% |
| Median profit factor | 2.64 |
| Median maximum drawdown | ₹22,255 |
| Median additional cost buffer | 5.30 points/order |

These thresholds are diagnostic screens introduced after the original 504 run; they are not capital-promotion gates.

## Data-quality finding
The trade-level artifact contains 31,752 configuration-cycle rows, but 39 rows have missing net_rupees values across 24 configurations. Every configuration still has 63 cycle records, so this is not a missing-cycle problem; it is a missing realized-net-P&L field problem. Robustness metrics exclude these observations rather than imputing them. This discrepancy must be resolved before the trade-level robustness table is treated as final authoritative evidence.

## Additional execution-cost stress
Additional cost was imposed directly on each recorded order using the recorded lot size. This does not rerun historical fills; it measures tolerance to additional all-in execution cost.

| Additional cost/order | Positive configurations | Median net P&L | Median max drawdown |
|---:|---:|---:|---:|
| 0.00 | 367/504 (72.8%) | ₹109,249 | ₹22,255 |
| 0.25 | 362/504 (71.8%) | ₹103,492 | ₹22,942 |
| 0.50 | 361/504 (71.6%) | ₹97,895 | ₹23,858 |
| 1.00 | 352/504 (69.8%) | ₹87,200 | ₹24,564 |
| 1.50 | 338/504 (67.1%) | ₹76,557 | ₹26,595 |
| 2.00 | 323/504 (64.1%) | ₹66,607 | ₹28,914 |
| 3.00 | 305/504 (60.5%) | ₹46,707 | ₹36,290 |

## Traceability interpretation
At baseline, positive total P&L, win rate >=50%, profit factor >=1.2 and maximum drawdown <=₹150k are simultaneously satisfied by 282/504 configurations (56.0%). Adding the >=1-point/order additional-cost screen leaves the same 282/504 intersection under these diagnostic screens. This is evidence of breadth in the retrospective surface, not deployment approval.

The next visualization layer should map K1 × K2 × K3 slices for win rate, profit factor, drawdown, cost buffer and positive-P&L breadth under progressively higher cost stress.

## Statistical interpretation
The original Phase 22A result remains unchanged: 323/504 raw bootstrap p-values were below 0.05 and 0/504 Holm-adjusted p-values were below 0.05. Holm remains appropriate for simultaneous inferential claims, but it is not the primary lens for this economic-robustness question.

## Methodological boundary
No strategy rule was changed and no configuration was selected using these results. No new holdout was opened. This analysis uses the completed 63-week retrospective artifact and remains OHLC-reconstructed, so it cannot establish future profitability or historical executable fill quality.

## Next research gate
1. Resolve the 39 missing net_rupees observations.
2. Make the robustness calculation reproducible inside the Phase-22A workflow.
3. Run the same metrics on the genuinely prospective weekly period.
4. Perform explicit execution-cost/slippage stress there.
5. Keep historical and prospective results separate.
6. Retain bid/ask/depth and capital/margin validation as independent evidence gates.

**Conclusion:** Phase 22A now provides a retrospective robustness map rather than merely a significance test. The evidence supports further prospective validation of the strategy family, while the current data/execution boundary prevents a deployment conclusion.