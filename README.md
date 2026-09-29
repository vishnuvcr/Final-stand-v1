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
