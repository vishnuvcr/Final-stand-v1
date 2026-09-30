# Final Stand v1 — Market Inefficiency Research

## Latest research status — 2026-09-30

**Weekly NIFTY strategy research has completed Phase 22A's full 504-configuration retrospective expansion. Phase 22W prospective execution-aware validation remains active.**

### Phase status

- Phase 21W — final five-expiry external recovery and 63-expiry frozen rerun: ✅ complete; 12,822 admitted cells, 224 variants rerun, 0 promoted
- Phase 22A — weekly 504-configuration strike-range expansion: ✅ complete; 504/504 tested, 0 promoted

- Phase 8W — weekly strategy definition: ✅
- Phase 9W — HF weekly data gate: ✅ 63 usable weekly cycles
- Phase 10W — mechanics / margin / costs: ✅
- Phase 11W — weekly backtest: ✅
- Phase 12W — robustness: ✅
- Phase 13W — frozen stop + untouched holdout: ✅
- Phase 14W — final manuscript: ✅
- Phase 15W — execution-data discovery/validation: 🔄 active (frozen strategy; holdout remains locked)

### Key results

- 63 usable weekly cycles.
- Frozen configuration: 0.50 index points slippage per leg and 50-point hard stop.
- Untouched 14-cycle holdout: mean net P&L ₹1,566.04/cycle; win rate 78.57%; annualized weekly Sharpe 2.02.
- Frozen Phase 12 cell: mean net P&L ₹3,503.86/cycle; annualized weekly Sharpe 4.42.
- Holm-adjusted bootstrap p-value for the frozen cell across 30 candidate cells: 0.006.
- CSCV-style PBO proxy: 0.00 across 20 paths.
- DSR-style probability: 0.9892, explicitly treated as an implementation-specific approximation.

### Phase 15W current status

Public TickBytes and OptionVault samples contain NIFTY option Level-1/Level-2 bid/ask fields, but their documentation distinguishes these evaluation samples from subscription/licensed historical archives. A free complete historical quote archive has not yet been qualified. Phase 15W is therefore auditing public sources before any paid data purchase is considered.

[Phase 15W execution-data discovery branch](../phase-15w-execution-data-discovery)

### Critical limitations

The primary historical source provides OHLC rather than historical bid/ask. Results are therefore historical OHLC reconstructions rather than verified executable fills. Historical NSE SPAN/peak-margin integration remains required before capital-normalized returns can be reported.

The study does not establish live-trading profitability.

### Research branches and artifacts

- [Phase 8W — weekly strategy](../phase-8-weekly-expiry-restart)
- [Phase 9W — HF data gate](../phase-9w-hf-data-gate)
- [Phase 10W — mechanics / margin / costs](../phase-10w-mechanics-margin-costs)
- [Phase 11W — weekly backtest](../phase-11w-weekly-backtest)
- [Phase 12W — robustness](../phase-12w-robustness)
- [Phase 13W — untouched holdout](../phase-13w-untouched-holdout)
- [Phase 14W — final manuscript](../phase-14w-manuscript)

Canonical files are maintained inside the respective phase branches. The research plan, execution log and error log remain the governing audit trail.

### Phase 15W expanded free-source audit — 2026-09-30
- Searched Hugging Face, Kaggle, Zenodo, GitHub and broker/API routes for historical NIFTY weekly-option BBO/depth.
- No new free historical BBO archive was qualified.
- Free OHLC sources remain useful for cross-validation; public BBO schemas/samples remain schema-qualified but archive-unqualified.
- New audit: [Phase 15W expanded free-source audit](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-15w-execution-data-discovery/research/phase15w_execution_data/FREE_SOURCE_AUDIT_EXPANDED.md)
- Next zero-cost gate: empirical coverage probe of any user-authorized free API credentials for expired NIFTY contracts.

### Phase 15W API probe gate — 2026-09-30
- ICICI Breeze and Dhan provide historical option OHLC/OI routes, not documented historical BBO responses. citeturn2search1turn1search0
- Upstox provides expired 1-minute OHLC but its expired-instrument APIs require Plus. citeturn0search0turn0search2
- TrueData remains the directly BBO-capable historical candidate; exact historical expired-weekly coverage still requires authenticated verification.
- [API probe protocol](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-15w-execution-data-discovery/research/phase15w_execution_data/API_PROBE_PROTOCOL.md)
- [Expanded free-source audit](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-15w-execution-data-discovery/research/phase15w_execution_data/FREE_SOURCE_AUDIT_EXPANDED.md)


## Phase 15W closure and Phase 16W transition — 2026-09-30
- Phase 15W free historical-BBO discovery is closed: no qualifying free historical NIFTY weekly-options BBO archive was found across the documented GitHub, Hugging Face, Kaggle, Zenodo, public broker/API and NSE-source scope.
- Angel One SmartAPI is retained only as a potential free OHLC/OI cross-check; it does not resolve historical BBO validation.
- No commercial quote data were purchased, no credentials were stored, and the strategy/holdout remain unchanged.
- **Phase 16W — Capital and Margin Validation: 🔄 active**
- Phase 16W uses official NSE historical SPAN/risk-parameter and margin-report infrastructure where accessible to reconstruct peak capital requirements and capital-normalized diagnostics.
- [Phase 16W branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-16w-capital-validation)
- [Phase 16W plan](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-16w-capital-validation/research/phase16w_capital_validation/PHASE_PLAN.md)
- [Phase 16W source protocol](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-16w-capital-validation/research/phase16w_capital_validation/SOURCE_PROTOCOL.md)

### Phase 16W evidence boundary
Capital/margin reconstruction is a separate evidence layer from execution validation. Until a qualified historical bid/ask archive is obtained, all performance results remain **OHLC-reconstructed**, even if historical capital requirements are successfully reconstructed.


### Phase 17W — K1/K2/K3 strike-definition validation — 2026-09-30
- **Phase 17W — K1/K2/K3 alternatives: 🔄 active** on a separate branch.
- The experiment now tests **224 preregistered configurations**: 8 K1 rules × 4 K2 rules × 7 K3 premium multipliers.
- K3 target is `M × (P1 − P2)` with M ∈ {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0}; the historical frozen control is OTM1 + NEXT1 + M=2.0.
- Phase 13W's untouched holdout and all previous results remain locked and unchanged.
- The 224-variant family uses one Holm multiple-testing family and no post-observation expansion.
- [Phase 17W branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-17w-strike-alternatives)
- [Phase 17W plan](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-17w-strike-alternatives/research/phase17w_strike_alternatives/PHASE_PLAN.md)
- [Phase 17W variant registry](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-17w-strike-alternatives/research/phase17w_strike_alternatives/VARIANT_REGISTRY.md)



## Phase 19W — Recovered-data 224-variant rerun — 2026-09-30
- **Status: COMPLETE — no capital promotion.** Authoritative GitHub Actions run [36642638097](https://github.com/vishnuvcr/Final-stand-v1/actions/runs/36642638097) completed all 224 preregistered variants successfully.
- Recovered coverage: 13,956/14,112 variant-cycle cells (98.895%); strategy-level usable coverage was 36/63 cycles (57.143%) for every variant, producing 21 training, 7 validation and 8 holdout observations.
- 193/224 variants had positive training means; 136/224 positive validation means; 180/224 positive holdout means. However, **0/224 passed the frozen promotion gate**. No Holm-adjusted training p-value was <0.05.
- The binding limitation is contract-level historical coverage and executable evidence, not inability to run the strategy computation.
- Full derived option bars are preserved in workflow artifact [phase19w-recovered-results-issue-bridge](https://github.com/vishnuvcr/Final-stand-v1/actions/runs/36642638097#artifacts), while repository-safe summaries/trades are committed on the [Phase 19W branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-19w-recovered-rerun).
- [Phase 19W result](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-19w-recovered-rerun/research/phase19w_recovered_rerun/PHASE_RESULT.md)
- **Phase 20W — Multi-Source Contract Recovery: 🔄 prepared**. It will exhaust the registered public fallback sources for the remaining contract-level gaps before any further strategy conclusion.
- [Phase 20W branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-20w-multisource-recovery) · [Phase 20W plan](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-20w-multisource-recovery/research/phase20w_multisource_recovery/PHASE_PLAN.md)

## Phase 21W — Final 63-expiry recovery result — 2026-09-30

- **Final status: COMPLETE.** The five previously missing weekly expiries were recovered and the full 63-expiry, 224-configuration rerun completed.
- Final admitted coverage: **12,822 variant-cycle cells** across 63 weekly expiries.
- The final frozen 224-family had **0/224 capital-promotion passes**; minimum Holm-adjusted training p-value was approximately 0.074642.
- Historical results remain OHLC-reconstructed rather than verified bid/ask fills.
- [Phase 21W combined rerun branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-21w-combined-frozen-rerun)
- [Phase 21W external recovery branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-21w-external-full-strike-recovery)

## Phase 22A — Weekly 504-configuration strike-range expansion — 2026-09-30

- **Status: COMPLETE.** All **504 configurations** were tested across all **63 weekly expiries**.
- K1 was extended to **OTM1–OTM8 and ITM1–ITM8**, while ATM_NEAREST and ATM_UP were retained. K2 and K3 families were unchanged.
- Every configuration had **63/63 valid OHLC cycles**.
- Positive training P&L: **414/504**; positive validation P&L: **239/504**; positive historical-holdout P&L: **308/504**.
- Mean historical-holdout P&L: **₹33,113.91** per configuration total; mean annualized weekly Sharpe: **1.6885**.
- Raw bootstrap p<0.05: 323/504; **Holm-adjusted p<0.05: 0/504**; minimum adjusted p: **0.167944**.
- **0/504 configurations passed the capital-promotion gate.**
- Descriptive surface pattern: deeper OTM rules weakened beyond OTM3; deeper ITM, NEXT2/NEXT3 and larger K3 values showed higher retrospective sample averages.
- This phase is not a new unseen-data result. The historical holdout was already exposed during Phase 21W, and all results remain OHLC-reconstructed.
- [Phase 22A branch](https://github.com/vishnuvcr/Final-stand-v1/tree/phase-22a-weekly-504-strike-expansion)
- [Phase 22A plan](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-22a-weekly-504-strike-expansion/research/phase22a_weekly_504_strike_expansion/PHASE_PLAN.md)
- [Phase 22A results](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-22a-weekly-504-strike-expansion/research/phase22a_weekly_504_strike_expansion/RESULTS.md)
- [Phase 22A parameter-surface analysis](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-22a-weekly-504-strike-expansion/research/phase22a_weekly_504_strike_expansion/PARAMETER_SURFACE_ANALYSIS.md)
- [Phase 22A manuscript](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-22a-weekly-504-strike-expansion/research/phase22a_weekly_504_strike_expansion/FINAL_MANUSCRIPT.md)
- [Phase 22A workflow run](https://github.com/vishnuvcr/Final-stand-v1/actions/runs/36741881293)

## Phase 22W — Prospective execution-aware validation — 2026-09-30

- **Status: ACTIVE.** Execution-data acquisition remains the main blocker to opening a genuinely new execution-aware holdout.
- The 504-family result is preserved as a retrospective parameter-surface layer; no configuration is promoted or selected post hoc.
- Historical bid/ask/depth, liquidity and margin evidence remain separate gates before deployment interpretation.


## Phase 22A robustness reinterpretation — 2026-10-01
- The 504 configurations are now treated as a **robustness grid**, not a 504-way winner-selection exercise.
- New retrospective diagnostics: net-P&L breadth, win-rate breadth, profit factor, maximum drawdown, additional execution-cost buffer, and cost-stress survival.
- Baseline: 367/504 configurations had positive total net P&L; 300/504 had >=50% win rate; 431/504 had max drawdown <=₹150k.
- Additional execution-cost stress of 3 points/order still left 305/504 configurations with positive total net P&L.
- A trade-level audit found 39 missing net-P&L fields across 24 configurations; these are excluded from the robustness calculations and logged as E22A-012. They must be resolved before this table is treated as final authoritative evidence.
- Holm remains a multiple-testing diagnostic, not the primary economic robustness criterion.
- [Phase 22A robustness analysis](https://github.com/vishnuvcr/Final-stand-v1/blob/phase-22a-weekly-504-strike-expansion/research/phase22a_weekly_504_strike_expansion/ROBUSTNESS_ANALYSIS.md)
