# Final Stand v1 — Market Inefficiency Research

## Current status
**Phase 8 is active on branch `phase-8-video-call-ladder`.** The main branch carries the governance baseline; the active research implementation is isolated on its phase branch.

## Research objective
Test whether a video-derived NIFTY monthly-options strategy — an initial long call / middle short call / farther short call ladder followed, after time decay, by purchasing the middle strike to convert the position into a defined-risk bull call spread — produces a statistically robust, executable net edge after realistic Indian transaction costs, bid/ask slippage, margin constraints, and risk controls.

The hypothesis is exploratory. No profitability is assumed.

## Phase map
- Phase 0 — Repository and research governance ✅
- Phases 1–7 — Prior market-inefficiency / volatility / option-surface research: preserved from project history; not recreated here.
- Phase 8 — Video-derived call-ladder-to-spread strategy: **INITIALIZED**
- Phase 9 — Data acquisition + point-in-time option-chain reconstruction
- Phase 10 — Payoff/Greeks/margin validation and execution-cost model
- Phase 11 — In-sample / validation / walk-forward backtesting
- Phase 12 — CPCV / PBO / DSR / sensitivity / regime analysis
- Phase 13 — Untouched holdout + robustness gate
- Phase 14 — Final manuscript, figures, appendices and reproducibility package

## Canonical files
- [Project instructions](PROJECT_INSTRUCTIONS.md)
- [Phase 8 strategy specification](research/phase8/STRATEGY_SPEC.md)
- [Phase 8 research protocol](research/phase8/RESEARCH_PROTOCOL.md)
- [Phase 8 research questions](research/phase8/RESEARCH_QUESTIONS.md)
- [Research log](research/logs/RESEARCH_LOG.md)
- [Error log](research/logs/ERROR_LOG.md)

## Important methodological rule
The source video is treated as a hypothesis generator, not as proof of an edge. Video-reported rules will be separated from rules that are later chosen or optimized statistically. All parameters must be frozen before the final holdout.

## Cost and broker realism
The execution model will include Paytm Money brokerage, statutory/regulatory/exchange charges, bid/ask spread, slippage, multi-leg execution, margin requirements, and any applicable overnight/auto-square-off constraints. Paytm Money states that F&O brokerage is Rs.10 per executed unique order and that statutory/regulatory/exchange charges are levied at actuals; these values will be versioned rather than hard-coded without date attribution.

## No trading conclusion yet
No live-trading recommendation is made at this stage. The strategy must survive the predefined statistical and economic gates before any conclusion about usability.
