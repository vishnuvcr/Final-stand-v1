# Final Stand v1 — Market Inefficiency Research

## Latest research status — 2026-09-29

**Weekly NIFTY strategy research has completed the empirical protocol through Phase 14W manuscript synthesis.**

### Phase status

- Phase 8W — weekly strategy definition: ✅
- Phase 9W — HF weekly data gate: ✅ 63 usable weekly cycles
- Phase 10W — mechanics / margin / costs: ✅
- Phase 11W — weekly backtest: ✅
- Phase 12W — robustness: ✅
- Phase 13W — frozen stop + untouched holdout: ✅
- Phase 14W — final manuscript: ✅

### Key results

- 63 usable weekly cycles.
- Frozen configuration: 0.50 index points slippage per leg and 50-point hard stop.
- Untouched 14-cycle holdout: mean net P&L ₹1,566.04/cycle; win rate 78.57%; annualized weekly Sharpe 2.02.
- Frozen Phase 12 cell: mean net P&L ₹3,503.86/cycle; annualized weekly Sharpe 4.42.
- Holm-adjusted bootstrap p-value for the frozen cell across 30 candidate cells: 0.006.
- CSCV-style PBO proxy: 0.00 across 20 paths.
- DSR-style probability: 0.9892, explicitly treated as an implementation-specific approximation.

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
