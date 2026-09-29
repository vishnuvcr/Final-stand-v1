# Final Stand v1 — Market Inefficiency Research

## Current status
**Phase 8 — Video-derived call-ladder-to-spread research: ACTIVE / design gate passed.**

The repository was initialized on 2026-09-29. Prior project research is preserved in the project-library artifacts; the new repository records the next reproducible phase.

## Current research objective
Test whether a video-derived NIFTY monthly-options strategy — long lower-strike call + short next-strike call + short farther OTM call selected by the `2 × premium-difference` rule, followed after a defined decay interval by buying back the middle strike — has a robust net edge after realistic Indian execution costs, margin requirements and risk controls.

The hypothesis is exploratory. No profitability is assumed.

## Phase map
- Phase 0 — Repository and research governance ✅
- Phases 1–7 — Prior market-inefficiency / volatility / option-surface research: preserved from project history.
- Phase 8 — Video-derived call-ladder-to-spread strategy: **ACTIVE**
- Phase 9 — Data acquisition + point-in-time option-chain reconstruction
- Phase 10 — Payoff/Greeks/margin validation and execution-cost model
- Phase 11 — In-sample / validation / walk-forward backtesting
- Phase 12 — CPCV / PBO / DSR / sensitivity / regime analysis
- Phase 13 — Untouched holdout + robustness gate
- Phase 14 — Final manuscript, figures, appendices and reproducibility package

## Phase 8 findings so far
The pre-lock position is mathematically a **bull call ladder**: one long lower-strike call and two short higher-strike calls. Its expiry payoff is capped in the middle zone but becomes theoretically unbounded-loss above the highest short strike. After buying back the middle short, the remaining position algebraically becomes a lower-strike-long / upper-strike-short bull call spread.

These are payoff identities, not evidence of profitability.

## Canonical files
- [Project instructions](PROJECT_INSTRUCTIONS.md)
- [Master research plan](RESEARCH_PLAN.md)
- [Phase 8 strategy specification](research/phase8/STRATEGY_SPEC.md)
- [Phase 8 research protocol](research/phase8/RESEARCH_PROTOCOL.md)
- [Phase 8 research questions](research/phase8/RESEARCH_QUESTIONS.md)
- [Phase 8 literature review](research/phase8/LITERATURE_REVIEW.md)
- [Phase 8 data-source manifest](research/phase8/DATA_SOURCE_MANIFEST.md)
- [Research log](research/logs/RESEARCH_LOG.md)
- [Error log](research/logs/ERROR_LOG.md)
- [Manual Phase 8 workflow](.github/workflows/phase-8-video-call-ladder.yml)

## Important methodological rule
The source video is a hypothesis generator, not proof of an edge. Video-reported rules are separated from independently verified payoff mechanics and from any parameters selected during validation. The untouched final holdout remains inaccessible to parameter optimization.

## Cost and broker realism
The execution model includes Paytm Money brokerage, statutory/regulatory/exchange charges, bid/ask spread, slippage, multi-leg execution, margin requirements and applicable overnight/square-off constraints. Paytm Money currently states Rs.10 brokerage per executed unique F&O order and that statutory/regulatory/exchange charges are levied at actuals; dated cost schedules will be maintained.

## No trading conclusion yet
No live-trading recommendation or profitability conclusion has been established. The strategy must pass the predefined statistical and economic gates before promotion.
