# Phase 22A Parameter-Surface Analysis

## 1. K1 strike distance

The K1 surface is asymmetric in this retrospective sample.

### OTM side

OTM1–OTM3 retained positive mean historical-holdout P&L, while the average weakened sharply at deeper ranks:

| K1 | Mean validation P&L | Mean historical-holdout P&L |
|---|---:|---:|
| OTM1 | ₹7,688.62 | ₹30,720.09 |
| OTM3 | -₹107.10 | ₹27,060.85 |
| OTM5 | -₹9,630.15 | ₹7,918.04 |
| OTM6 | -₹10,044.01 | -₹1,758.55 |
| OTM7 | -₹9,761.26 | -₹6,718.41 |
| OTM8 | -₹7,774.27 | -₹672.77 |

The deeper OTM expansion therefore did not create a monotonic improvement.

### ITM side

The mean historical-holdout P&L was positive from ITM1 through ITM8:

| K1 | Mean historical-holdout P&L | Positive historical-holdout configurations |
|---|---:|---:|
| ITM1 | ₹34,452.33 | 19/28 |
| ITM2 | ₹40,515.42 | 19/28 |
| ITM3 | ₹51,806.65 | 21/28 |
| ITM4 | ₹58,392.01 | 21/28 |
| ITM5 | ₹51,346.06 | 21/28 |
| ITM6 | ₹61,981.58 | 14/28 |
| ITM7 | ₹70,270.86 | 16/28 |
| ITM8 | ₹63,403.91 | 13/28 |

The fall in positive-configuration breadth at ITM6–ITM8 shows why the marginal K1 mean cannot be treated as a uniform rule improvement.

## 2. K2 strike relation

Mean historical-holdout P&L:

- NEXT1: ₹16,102.42
- NEXT2: ₹56,237.76
- NEXT3: ₹53,625.81
- MIRROR_GAP: ₹6,489.66

NEXT2 and NEXT3 were also positive on average in validation, whereas NEXT1 and MIRROR_GAP were negative on average in validation.

This is useful for future hypothesis formation, but it is still retrospective.

## 3. K3 target multiplier

Mean historical-holdout P&L by K3:

| K3 | Mean historical-holdout P&L | Positive holdout configurations |
|---:|---:|---:|
| 0.5 | -₹48,742.45 | 0/72 |
| 1.0 | -₹14,421.54 | 17/72 |
| 1.5 | ₹15,178.35 | 40/72 |
| 2.0 | ₹39,007.50 | 58/72 |
| 2.5 | ₹58,350.79 | 63/72 |
| 3.0 | ₹80,755.37 | 65/72 |
| 4.0 | ₹101,669.37 | 65/72 |

The K3 surface is monotone in this retrospective sample. That observation is explicitly treated as descriptive because choosing a higher K3 after observing this result would be post-hoc selection.

## 4. Interaction pattern

The strongest historical region clusters around:

- deeper ITM K1 rules, especially ITM4–ITM8;
- NEXT2 or NEXT3 K2;
- K3 values at or above 2.

The full 504 rows show substantial within-group dispersion. For example, ITM8 has a high mean historical-holdout P&L, but only 13 of its 28 combinations are positive.

## 5. Multiple-testing interpretation

The family-wide statistical result dominates the visual surface:

- raw p<0.05: 323/504;
- Holm-adjusted p<0.05: 0/504;
- minimum Holm-adjusted p: 0.167944.

The expanded search therefore provides a useful map of parameter sensitivity but not a family-wise statistically validated configuration.

## 6. Comparison with the earlier 224 family

The previous 224-family had mean historical-holdout P&L of ₹33,660.78 and mean holdout annualized weekly Sharpe of 2.357.

The expanded 504-family had mean historical-holdout P&L of ₹33,113.91 and mean holdout annualized weekly Sharpe of 1.689.

Training mean increased from approximately ₹83.5k to ₹131.8k while historical-holdout mean was nearly unchanged. This divergence is consistent with an increased opportunity for in-sample fitting as the parameter family expands.

## 7. Interpretation

Phase 22A establishes a retrospective surface characterization:

- deeper OTM rules weaken beyond OTM3 in the tested sample;
- deeper ITM rules have higher mean historical outcomes, but not uniformly across combinations;
- NEXT2/NEXT3 are stronger on the surface than NEXT1 and MIRROR_GAP;
- larger K3 values have stronger sample-average outcomes.

These statements should be carried forward as hypotheses for a future frozen validation, not as deployment rules.
