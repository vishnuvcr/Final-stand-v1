# Final Stand v1 — Market Inefficiency Research

## Current status

**Weekly research protocol completed through Phase 14W manuscript synthesis.**

The active study evaluates a deterministic weekly NIFTY call-ladder-to-spread strategy with explicit transaction costs, slippage, chronological validation, an untouched holdout and a 30-cell robustness audit.

### Phase status

- Phase 8W — weekly strategy definition: ✅
- Phase 9W — HF weekly data gate: ✅ 63 usable weekly cycles
- Phase 10W — mechanics, margin and costs: ✅
- Phase 11W — weekly backtest: ✅
- Phase 12W — robustness: ✅
- Phase 13W — frozen stop and untouched holdout: ✅
- Phase 14W — final manuscript: ✅

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