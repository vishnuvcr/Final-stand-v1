# Final Manuscript — Weekly NIFTY Option-Spread Strike-Range Expansion

## Title

**Weekly NIFTY Option-Spread Strike-Range Expansion: A 504-Configuration Retrospective Validation of K1, K2 and K3 Rules**

## Abstract

### Background
A weekly-horizon NIFTY options strategy was previously evaluated over 224 pre-registered combinations of strike-selection rules and a premium-target multiplier. The present phase expands the K1 strike-distance dimension to OTM1–OTM8 and ITM1–ITM8 while retaining ATM_NEAREST and ATM_UP, producing 504 total configurations.

### Objective
To test the complete expanded configuration family under the already-frozen weekly trading protocol and quantify the resulting K1/K2/K3 parameter surface without post-hoc configuration selection.

### Methods
All 504 combinations of 18 K1 rules, four K2 rules and seven K3 multipliers were evaluated over 63 weekly expiries using the recovered Phase-21 historical OHLC interface. Entry was 10:00 IST on the first trading day after the prior weekly expiry; the lock/exit decision was 14:00 IST on the trading day before the target expiry; residual exposure could continue to target expiry unless terminated by the frozen 50-point hard stop. Slippage was 0.50 NIFTY index points per leg and the registered Paytm Money/NSE transaction-cost model was retained. The entire 504-family was treated as one multiple-testing family with Holm adjustment.

### Results
All 504 configurations were valid across all 63 weekly cycles. 414/504 had positive training P&L, 239/504 positive validation P&L and 308/504 positive historical-holdout P&L. Mean historical-holdout P&L across configurations was ₹33,113.91 and mean annualized weekly Sharpe was 1.6885. The raw bootstrap test produced 323/504 p-values below 0.05, but 0/504 configurations had Holm-adjusted p<0.05; the minimum adjusted p-value was 0.167944. No configuration passed the frozen capital-promotion gate.

### Conclusion
The expansion provides a detailed empirical map of the historical surface. Deeper OTM rules were progressively weaker, while the highest mean historical outcomes clustered in deeper ITM, NEXT2/NEXT3 and higher-K3 regions. These are descriptive historical associations only. Because all returns remain OHLC-reconstructed and the same historical holdout has already been exposed to the earlier 224-family, the phase does not establish a new out-of-sample or executable trading edge.

---

## 1. Introduction

Systematic option strategies are vulnerable to parameter uncertainty and multiple testing. A configuration can appear attractive after searching many strike definitions even when the observed relationship is unstable. The earlier weekly NIFTY research therefore used a frozen configuration family and explicit statistical correction.

Phase 22A expands that family deliberately rather than choosing a single previously observed configuration. The purpose is to characterize the complete historical surface when K1 strike distance is widened through OTM8 and ITM8.

The scientific objective is not to identify a single winner from the expanded family. It is to measure how the whole family behaves under a fixed weekly protocol while preserving an auditable distinction between retrospective surface characterization and prospective validation.

## 2. Research question

When the strategy is executed as a weekly-horizon weekly-expiry trade, how does the empirical performance surface change when K1 strike selection is extended from OTM/ITM ranks 1–3 to ranks 1–8, while K2, K3, stop, timing, slippage and transaction-cost assumptions remain unchanged?

## 3. Aim

To quantify the complete expanded K1/K2/K3 weekly configuration surface over the available 63-expiry historical sample.

## 4. Objectives

1. Generate exactly 504 deterministic configuration IDs.
2. Evaluate every configuration under the same weekly protocol.
3. Preserve the Paytm Money/NSE cost assumptions and 0.50-point per-leg slippage.
4. Measure training, validation and historical-holdout net P&L.
5. Measure win rate, maximum drawdown, expected shortfall, annualized weekly Sharpe and mean cost.
6. Apply one Holm correction across the entire 504-family.
7. Document all data and implementation errors encountered before the final run.
8. Produce a complete reproducible result table and manuscript-style synthesis.

## 5. Methods

### 5.1 Configuration space

K1:
OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8.

K2:
NEXT1, NEXT2, NEXT3, MIRROR_GAP.

K3:
0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0.

Total:
18 × 4 × 7 = 504.

No configuration was added or removed after results were inspected.

### 5.2 Weekly trading protocol

The strategy is explicitly weekly-horizon. Intraday timestamps represent execution decision points inside the weekly holding period rather than an intraday-only strategy.

- Entry: 10:00 IST on the first trading day after the prior weekly expiry.
- Lock/exit decision: 14:00 IST on the trading day before the target expiry.
- Residual position: may persist to target expiry unless exited earlier.
- Hard stop: 50 NIFTY points.
- Baseline slippage: 0.50 NIFTY points per leg.
- Transaction costs: frozen Paytm Money/NSE model from the registered research engine.

### 5.3 Historical data

The primary run reused the recovered 63-expiry historical interface admitted during Phase 21W.

- 58 expiries used the original historical option source with SHA-256 checks from the frozen cycle manifest.
- Five previously recovered 2026 expiries used the pinned RISSIN revision 8f7739cab3f38abdcbc6332a6d0a83e1341326e3.
- The RISSIN file was upstox_intraday/NIFTY/NIFTY_2026.parquet.
- The source data provide OHLC/volume fields but no historical bid/ask book.

The data were cached in GitHub Actions and the final run was executed by workflow 36741881293.

### 5.4 Data-quality controls

The final pipeline required:

- exact entry and lock timestamps;
- valid K1/K2/K3 strike selection;
- three-leg OHLC observations;
- no interpolation;
- no strike substitution;
- no cross-source leg mixing;
- source SHA-256 consistency;
- explicit Asia/Kolkata timestamp casting;
- deterministic 504-configuration registry.

All 504 configurations passed the final validity gate over 63 cycles.

### 5.5 Statistical analysis

For each configuration, the engine computed:

- total and mean net P&L;
- median net P&L;
- win rate;
- maximum drawdown;
- 95% expected shortfall;
- mean transaction cost;
- annualized weekly Sharpe;
- valid-cycle rate;
- centered training bootstrap p-value.

The 504 raw p-values were corrected using one Holm multiple-testing family.

The capital-promotion gate remained unchanged from the registered research protocol. It requires sufficient validity and sample size, positive training and validation performance, and Holm-adjusted training p<0.05.

## 6. Results

### 6.1 Coverage

All 504 configurations had 63/63 valid cycles, corresponding to 100% configuration-level OHLC validity.

### 6.2 Family-wide performance

Positive training P&L occurred in 414/504 configurations, positive validation P&L in 239/504, and positive historical-holdout P&L in 308/504.

Across the 504 rows:

- mean training P&L = ₹131,783.69;
- mean validation P&L = ₹3,357.09;
- mean historical-holdout P&L = ₹33,113.91;
- mean historical-holdout annualized weekly Sharpe = 1.6885.

The historical-holdout P&L distribution ranged from -₹195,779.19 to ₹381,874.51. Its median was ₹15,259.05.

### 6.3 Multiple testing

323/504 raw bootstrap p-values were below 0.05.

After Holm correction across all 504 configurations:

- adjusted p<0.05: 0/504;
- minimum adjusted p: 0.167944.

Therefore no configuration satisfied the family-wise statistical gate.

### 6.4 K1 surface

The OTM side weakened materially beyond OTM3. Mean historical-holdout P&L was ₹30,720.09 at OTM1, ₹27,060.85 at OTM3, ₹7,918.04 at OTM5, -₹1,758.55 at OTM6 and -₹6,718.41 at OTM7.

The ITM side showed larger historical means. Mean historical-holdout P&L was ₹34,452.33 at ITM1, ₹51,806.65 at ITM3, ₹58,392.01 at ITM4, ₹70,270.86 at ITM7 and ₹63,403.91 at ITM8.

These are sample means across 28 configurations per K1 rule.

### 6.5 K2 surface

NEXT2 and NEXT3 had larger mean historical-holdout P&L than NEXT1 and MIRROR_GAP:

- NEXT1: ₹16,102.42;
- NEXT2: ₹56,237.76;
- NEXT3: ₹53,625.81;
- MIRROR_GAP: ₹6,489.66.

### 6.6 K3 surface

Mean historical-holdout P&L increased monotonically across the registered K3 values in the retrospective sample:

0.5 → -₹48,742.45  
1.0 → -₹14,421.54  
1.5 → ₹15,178.35  
2.0 → ₹39,007.50  
2.5 → ₹58,350.79  
3.0 → ₹80,755.37  
4.0 → ₹101,669.37

This ordering is informative for hypothesis formation but is not a prospective parameter-selection rule.

## 7. Inferences

### 7.1 What the run establishes

The expanded weekly family can be computed reproducibly over all 63 weekly cycles without K1 strike-coverage attrition.

The historical surface is not flat. K1, K2 and K3 choices have materially different sample-average outcomes.

The OTM and ITM sides are asymmetric in this sample, and K3 shows a strong monotone sample-average pattern toward larger multipliers.

### 7.2 What the run does not establish

The run does not establish that the observed surface will persist in a future period.

It does not establish executable fill quality because the underlying records do not provide historical bid/ask/depth.

It does not establish capital efficiency because margin reconstruction is a separate evidence layer.

It does not justify selecting a configuration from the same historical holdout after seeing the expanded surface.

## 8. Discussion

The principal methodological result is the difference between a compelling descriptive surface and a statistically validated configuration family.

Broadening the search space creates more opportunities for large raw test statistics and high historical P&L. The 504-family illustrates this directly: 323 raw bootstrap p-values were below 0.05, yet none remained below 0.05 after Holm correction.

The mean training P&L rose materially relative to the earlier 224-family while mean historical-holdout P&L remained almost unchanged. That divergence is a warning that wider search can increase historical fit without increasing robust out-of-sample evidence.

The K1 surface also shows an asymmetry that can generate plausible economic narratives after the fact. Such narratives are useful for future hypothesis testing, but they should not be mistaken for independent validation.

## 9. Strengths

1. Complete enumeration of the requested 504-family.
2. Same weekly protocol, stop logic, cost model and slippage assumption across all configurations.
3. One multiplicity correction across the entire expanded family.
4. Source provenance and SHA-256 checks.
5. Reproducible GitHub Actions execution.
6. All 63 weekly cycles were available for the final OHLC validity gate.
7. Explicit separation between retrospective surface analysis and future external validation.

## 10. Limitations

1. Historical bid/ask/depth are unavailable, so returns are OHLC reconstructions rather than verified executable fills.
2. The historical holdout used here was already exposed during Phase 21W; therefore Phase 22A is not a new unseen validation.
3. Transaction costs use the frozen research model rather than a historical fill ledger.
4. Configuration-level P&L totals overlap the same market periods and are not additive portfolio returns.
5. The observed surface can contain data-mining and selection effects despite family-wise correction, especially once the full surface is visually inspected.
6. Capital and margin validation is not included in this phase.
7. Regime and microstructure effects require separate prospective analysis.

## 11. Conclusion

Phase 22A successfully completed the requested weekly backtest of all 504 configurations, extending K1 through OTM8 and ITM8.

The principal descriptive patterns were:

- deeper OTM selections weakened beyond OTM3 in this sample;
- deeper ITM selections had higher mean historical-holdout P&L, although the deepest ITM groups were not uniformly positive across all combinations;
- NEXT2 and NEXT3 exceeded NEXT1 and MIRROR_GAP on mean historical-holdout P&L;
- higher K3 values were associated with higher sample-average P&L.

The controlling inferential result is that 0/504 configurations passed the Holm-adjusted statistical promotion criterion, with minimum adjusted p=0.167944. Accordingly, Phase 22A does not produce a statistically validated capital-ready configuration.

## 12. Future research

The next phase should preserve the complete 504-family audit trail and move to a genuinely new chronological period.

1. Freeze the prospective configuration family before opening any new holdout.
2. Obtain new post-Phase-21 weekly data, preferably with executable bid/ask/depth.
3. Repeat the weekly protocol with the same cost and stop assumptions.
4. Evaluate execution feasibility, spread cost, liquidity and partial/rejected fills where depth supports it.
5. Re-run statistical inference on the untouched new period.
6. Add NSE margin/peak-capital reconstruction before any capital-normalized interpretation.
7. Only after those gates, prepare a deployment specification.

## 13. Reproducibility and supplements

Primary outputs:

- output/variant_registry.json
- output/variant_summary.json
- output/ALL_504_CONFIG_RESULTS.csv
- output/ALL_504_CONFIG_RESULTS_COMPACT.csv
- output/K1_SURFACE_MEAN_HOLDOUT.csv
- output/K2_SURFACE_MEAN_HOLDOUT.csv
- output/K3_SURFACE_MEAN_HOLDOUT.csv

Method and audit files:

- PHASE_PLAN.md
- VARIANT_REGISTRY.md
- RESULTS.md
- PARAMETER_SURFACE_ANALYSIS.md
- RESEARCH_LOG.md
- ERROR_LOG.md
- .github/workflows/phase-22a-weekly-504-strike-expansion.yml

Workflow evidence:

- Run: 36741881293
- Artifact: phase22a-weekly-504-results
- Artifact ID: 11111230842
- Artifact digest: sha256:1a250f5ca0a39aaefb3b293758eedc41293387e720cf65491e720a5cdb243964
