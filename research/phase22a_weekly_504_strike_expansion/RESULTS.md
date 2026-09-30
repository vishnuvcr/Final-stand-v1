# Phase 22A Results — Weekly 504-Configuration Strike-Range Expansion

## Executive result

Phase 22A completed the full weekly-horizon backtest for all 504 pre-registered configurations:

- 18 K1 strike rules: OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8
- 4 K2 rules: NEXT1, NEXT2, NEXT3, MIRROR_GAP
- 7 K3 multipliers: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0
- Total: 504 configurations

Every configuration had 63/63 valid weekly cycles in the OHLC data contract.

The key inferential result is that 0/504 configurations passed the frozen capital-promotion gate. The minimum Holm-adjusted training p-value across the full 504-family was 0.167944, while the minimum raw bootstrap p-value was 0.000333.

This phase is a retrospective parameter-expansion study, not a fresh unseen-data validation. The 63-expiry sample includes the historical holdout segment already examined in Phase 21W.

## Protocol

| Element | Frozen rule |
|---|---|
| Trading horizon | Weekly |
| Entry | 10:00 IST on first trading day after prior weekly expiry |
| Lock/exit decision | 14:00 IST on trading day before target expiry |
| Residual exposure | May continue to target expiry unless stopped/exited |
| Hard stop | 50 NIFTY points |
| Baseline slippage | 0.50 NIFTY points per leg |
| Transaction costs | Existing Paytm Money/NSE registered model |
| Statistical family | All 504 configurations with one Holm correction |

## Global results

| Metric | Result |
|---|---:|
| Configurations tested | 504 |
| Validity rate, minimum | 100.0% |
| Validity rate, mean | 100.0% |
| Positive training P&L | 414 / 504 |
| Positive validation P&L | 239 / 504 |
| Positive historical holdout P&L | 308 / 504 |
| Positive holdout Sharpe | 308 / 504 |
| Raw bootstrap p < 0.05 | 323 / 504 |
| Holm-adjusted p < 0.05 | 0 / 504 |
| Capital-promotion pass | 0 / 504 |
| Minimum Holm-adjusted p | 0.167944 |
| Minimum raw p | 0.000333 |
| Positive in training + validation + historical holdout | 229 / 504 |

### Aggregate P&L distribution across configurations

| Metric | Training | Validation | Historical holdout |
|---|---:|---:|---:|
| Mean net P&L | ₹131,783.69 | ₹3,357.09 | ₹33,113.91 |
| Median net P&L | ₹89,994.83 | -₹2,224.56 | ₹15,259.05 |
| Minimum | -₹586,633.26 | -₹330,658.19 | -₹195,779.19 |
| Maximum | ₹1,208,370.83 | ₹332,678.36 | ₹381,874.51 |

Historical-holdout annualized weekly Sharpe across configurations:
mean 1.6885, median 1.5898, minimum -21.6953, maximum 18.8849.

## K1 strike-range surface

| K1 rule | Mean training P&L | Mean validation P&L | Mean historical holdout P&L | Mean holdout Sharpe | Positive historical holdouts |
|---|---:|---:|---:|---:|---:|
| OTM1 | ₹145,426.68 | ₹7,688.62 | ₹30,720.09 | 2.172 | 19/28 |
| OTM2 | ₹125,099.51 | ₹3,893.34 | ₹27,472.50 | 2.263 | 21/28 |
| OTM3 | ₹90,959.88 | -₹107.10 | ₹27,060.85 | 2.460 | 22/28 |
| OTM4 | ₹66,762.90 | -₹5,855.99 | ₹16,687.17 | 1.661 | 18/28 |
| OTM5 | ₹46,825.12 | -₹9,630.15 | ₹7,918.04 | 0.584 | 13/28 |
| OTM6 | ₹43,693.43 | -₹10,044.01 | -₹1,758.55 | -2.423 | 12/28 |
| OTM7 | ₹38,174.60 | -₹9,761.26 | -₹6,718.41 | -6.515 | 11/28 |
| OTM8 | ₹43,114.56 | -₹7,774.27 | -₹672.77 | -1.535 | 10/28 |
| ATM_NEAREST | ₹144,856.78 | ₹7,802.27 | ₹32,452.60 | 2.223 | 19/28 |
| ATM_UP | ₹145,426.68 | ₹7,688.62 | ₹30,720.09 | 2.172 | 19/28 |
| ITM1 | ₹158,316.28 | ₹12,632.39 | ₹34,452.33 | 2.157 | 19/28 |
| ITM2 | ₹174,663.06 | ₹17,145.29 | ₹40,515.42 | 2.383 | 19/28 |
| ITM3 | ₹206,009.99 | ₹16,700.45 | ₹51,806.65 | 2.958 | 21/28 |
| ITM4 | ₹194,497.68 | ₹10,878.48 | ₹58,392.01 | 3.781 | 21/28 |
| ITM5 | ₹196,767.49 | ₹7,197.30 | ₹51,346.06 | 2.776 | 21/28 |
| ITM6 | ₹202,855.53 | -₹896.32 | ₹61,981.58 | 3.508 | 14/28 |
| ITM7 | ₹209,522.30 | -₹5,334.85 | ₹70,270.86 | 5.580 | 16/28 |
| ITM8 | ₹139,134.02 | ₹18,204.76 | ₹63,403.91 | 4.186 | 13/28 |

The deeper OTM region did not improve monotonically. OTM6 and OTM7 were negative on average in the historical holdout. The deeper ITM region had larger historical means, but the deepest ITM groups were not uniformly positive across all 28 K2/K3 combinations.

## K2 surface

| K2 rule | Mean training P&L | Mean validation P&L | Mean historical holdout P&L | Mean holdout Sharpe | Positive historical holdouts |
|---|---:|---:|---:|---:|---:|
| NEXT1 | ₹110,101.13 | -₹17,615.90 | ₹16,102.42 | 1.055 | 66/126 |
| NEXT2 | ₹205,335.56 | ₹20,554.66 | ₹56,237.76 | 3.495 | 87/126 |
| NEXT3 | ₹164,545.97 | ₹15,126.47 | ₹53,625.81 | 3.084 | 100/126 |
| MIRROR_GAP | ₹47,152.11 | -₹4,636.88 | ₹6,489.66 | -0.879 | 55/126 |

## K3 surface

| K3 multiplier | Mean training P&L | Mean validation P&L | Mean historical holdout P&L | Mean holdout Sharpe | Positive historical holdouts |
|---:|---:|---:|---:|---:|---:|
| 0.5 | -₹104,752.35 | -₹75,802.17 | -₹48,742.45 | -3.746 | 0/72 |
| 1.0 | ₹26,190.76 | -₹31,918.28 | -₹14,421.54 | -1.781 | 17/72 |
| 1.5 | ₹106,907.49 | -₹3,579.16 | ₹15,178.35 | 0.720 | 40/72 |
| 2.0 | ₹165,565.11 | ₹14,211.64 | ₹39,007.50 | 2.491 | 58/72 |
| 2.5 | ₹210,995.06 | ₹30,777.62 | ₹58,350.79 | 3.567 | 63/72 |
| 3.0 | ₹239,028.73 | ₹39,283.08 | ₹80,755.37 | 4.969 | 65/72 |
| 4.0 | ₹278,551.06 | ₹50,526.88 | ₹101,669.37 | 5.599 | 65/72 |

The K3 ordering is a retrospective sample characteristic, not a post-hoc deployment rule.

## Illustrative historical extremes

The largest historical-holdout totals were concentrated in deeper ITM K1, NEXT2/NEXT3 and larger K3 combinations. Examples are shown for audit transparency only:

| Configuration | Training P&L | Validation P&L | Historical holdout P&L | Holdout Sharpe |
|---|---:|---:|---:|---:|
| ITM8_NEXT2_K3M4 | ₹1,208,370.83 | ₹332,678.36 | ₹381,874.51 | 17.902 |
| ITM8_NEXT3_K3M4 | ₹884,598.83 | ₹205,287.97 | ₹357,469.15 | 16.402 |
| ITM7_NEXT2_K3M4 | ₹995,080.59 | ₹263,244.58 | ₹356,073.73 | 17.782 |
| ITM8_NEXT3_K3M3 | ₹878,173.09 | ₹205,287.97 | ₹340,415.93 | 17.190 |
| ITM6_NEXT2_K3M4 | ₹894,789.29 | ₹206,581.10 | ₹329,567.76 | 17.108 |

These are descriptive historical observations, not a selected live configuration list.

## Comparison with the earlier 224-family

Phase 21W mean results were approximately:

- training: ₹83,517.66
- validation: ₹4,960.88
- historical holdout: ₹33,660.78
- mean holdout annualized weekly Sharpe: 2.357

Phase 22A produced:

- training: ₹131,783.69
- validation: ₹3,357.09
- historical holdout: ₹33,113.91
- mean holdout annualized weekly Sharpe: 1.689

The broader search therefore increased mean in-sample training P&L while leaving historical-holdout mean P&L almost unchanged and reducing the mean holdout Sharpe.

## Data and execution boundary

The analysis remains OHLC-reconstructed. The tested source records do not provide historical bid/ask/depth for the contracts. The frozen transaction-cost and slippage model was applied, but actual historical fills, market impact and liquidity constraints could not be directly observed.

Therefore:

1. the run answers the historical parameter-surface question;
2. it does not answer the historical executable-fill question;
3. it does not establish future profitability;
4. it does not justify capital deployment.

## Reproducibility

Primary outputs:

- output/variant_registry.json
- output/variant_summary.json
- output/ALL_504_CONFIG_RESULTS.csv
- output/ALL_504_CONFIG_RESULTS_COMPACT.csv
- output/K1_SURFACE_MEAN_HOLDOUT.csv
- output/K2_SURFACE_MEAN_HOLDOUT.csv
- output/K3_SURFACE_MEAN_HOLDOUT.csv

Workflow run: 36741881293
Artifact: phase22a-weekly-504-results
Artifact ID: 11111230842
Artifact digest: sha256:1a250f5ca0a39aaefb3b293758eedc41293387e720cf65491e720a5cdb243964
