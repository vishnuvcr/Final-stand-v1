# Final Stand v1 — Market Inefficiency Research

## Current status

**Weekly research protocol completed through Phase 17W strike-definition validation; Phase 16W capital/margin validation remains a downstream requirement.**

The active study evaluates a deterministic weekly NIFTY call-ladder-to-spread strategy with explicit transaction costs, slippage, chronological validation, an untouched holdout and a 30-cell robustness audit.

### Phase status

- Phase 8W — weekly strategy definition: ✅
- Phase 9W — HF weekly data gate: ✅ 63 usable weekly cycles
- Phase 10W — mechanics, margin and costs: ✅
- Phase 11W — weekly backtest: ✅
- Phase 12W — robustness: ✅
- Phase 13W — frozen stop and untouched holdout: ✅
- Phase 14W — final manuscript: ✅
- Phase 15W — historical execution-data discovery: ⚠️ no qualifying free historical weekly-options BBO archive
- Phase 16W — capital/margin validation: ⏳ pending downstream execution
- Phase 17W — K1/K2/K3 strike alternatives: ✅ 224 configurations evaluated; no variant passed the preregistered promotion gate

### Key empirical observations

- 63 usable weekly cycles.
- Frozen configuration: 0.50 index points slippage per leg + 50-point hard stop.
- Untouched 14-cycle holdout: mean net P&L ₹1,566.04/cycle; win rate 78.57%; annualized weekly Sharpe 2.02.
- Frozen Phase 12 robustness cell: mean net P&L ₹3,503.86/cycle; annualized weekly Sharpe 4.42.
- Holm-adjusted bootstrap p-value for the frozen cell across the 30-cell grid: 0.006.
- CSCV-style PBO proxy: 0.00 across 20 combinatorial paths.
- DSR-style probability: 0.9892; this is an implementation-specific approximation, not an exact published-estimator reproduction.

### Critical limitations

The primary dataset contains OHLC rather than historical bid/ask. Results therefore represent historical price reconstruction rather than verified executable fills. Historical NSE SPAN/peak-margin integration is still required before capital-normalized returns can be reported.

No live-trading profitability claim is established.

## Canonical research artifacts

- [Research plan](RESEARCH_PLAN.md)
- [Strategy specification](research/phase8_weekly/STRATEGY_SPEC.md)
- [Research questions](research/phase8_weekly/RESEARCH_QUESTIONS.md)
- [Research protocol](research/phase8_weekly/RESEARCH_PROTOCOL.md)
- [Literature review](research/phase8_weekly/LITERATURE_REVIEW.md)
- [Data-source manifest](research/phase8_weekly/DATA_SOURCE_MANIFEST.md)
- [Cost and margin model](research/phase8_weekly/COST_MARGIN_MODEL.md)
- [Phase 12 status](research/phase12_weekly/STATUS.md)
- [Phase 12 robustness outputs](research/phase12_weekly/robustness.json)
- [Phase 12 supplemental robustness](research/phase12_weekly/robustness_supplement.json)
- [Phase 13 holdout result](research/phase13_weekly/holdout.json)
- [Phase 14 final manuscript](research/phase14_weekly/FINAL_MANUSCRIPT.md)
- [Phase 14 status](research/phase14_weekly/STATUS.md)
- [Research execution log](research/logs/RESEARCH_LOG.md)
- [Error log](research/logs/ERROR_LOG.md)

## Research governance

All phases remain on separate branches. Empirical workflows have manual dispatch controls, cached Hugging Face data, reproducible artifacts and explicit error logging. The Phase 13 holdout is locked against any subsequent parameter tuning.

### Phase 15W — expanded free-source audit (active)
- Expanded search across Hugging Face, Kaggle, Zenodo, GitHub and broker/API routes.
- Free OHLC archives are available, including Hugging Face and Zenodo, but no free historical NIFTY weekly-options best-bid/ask archive has been qualified.
- Public GitHub projects prove BBO/L2 schemas exist, but complete historical archives are licensed, subscription-based, private, or not tracked in the public repository.
- [Phase 15W execution-data status](research/phase15w_execution_data/STATUS.md)
- [Phase 15W expanded free-source audit](research/phase15w_execution_data/FREE_SOURCE_AUDIT_EXPANDED.md)
- [Phase 15W paid-source shortlist](research/phase15w_execution_data/PAID_SOURCE_SHORTLIST.md)
### Phase 17W — strike-definition alternatives
- Registered and evaluated 224 configurations: 8 K1 rules × 4 K2 rules × 7 K3 multipliers.
- Full run: workflow 36626050986; 224 variants and 8,736 reconstructed trade rows passed the global audit.
- No variant met the promotion gate. Maximum usable coverage was 39/63, below the required 50/63, and no Holm-adjusted training p-value was below 0.05.
- No alternative was promoted and the Phase 13 holdout remains locked.
- [Phase 17W status](research/phase17w_strike_alternatives/STATUS.md)
- [Phase 17W results](research/phase17w_strike_alternatives/RESULTS.md)
- [Phase 17W variant registry](research/phase17w_strike_alternatives/VARIANT_REGISTRY.md)
