# Final Stand v1 — Market Inefficiency Research

## Current status
**Active experiment: Phase 8W — Weekly NIFTY call-ladder-to-spread strategy.**

The previous monthly-expiry version is retained only for auditability. It is not the active research design.

## New weekly objective
Test the video-derived strategy as a **weekly trading system**, where each NIFTY weekly expiry is one complete trade cycle.

Primary operationalization:
- target contract: the new weekly expiry after the prior weekly expiry;
- entry: first trading session after expiry at 10:00 IST;
- K1: first call strike above spot;
- K2: next call strike;
- K3: call strike above K2 whose premium is closest to 2 × (K1 premium − K2 premium);
- lock: buy K2 on the trading day immediately before expiry at 14:00 IST;
- post-lock position: long K1 / short K3 bull call spread;
- one primary trade per weekly expiry.

The hypothesis is exploratory. No profitability is assumed.

## Current NSE structure
NSE currently documents four weekly NIFTY 50 option expiries excluding the monthly contracts; weekly expiry is Tuesday, or the previous trading day when Tuesday is a holiday. NSE also specifies introduction of a new serial weekly contract after expiry. citeturn642743search0turn642743search1

## Weekly research status
- Phase 8W — weekly strategy definition: ✅
- Phase 9W — PIT weekly data: 🟡 pending
- Phase 10W — mechanics/margin/costs: pending
- Phase 11W — weekly backtest: pending
- Phase 12W — robustness: pending
- Phase 13W — untouched holdout: pending
- Phase 14W — final manuscript: pending

## Canonical weekly files
- [Weekly master research plan](RESEARCH_PLAN.md)
- [Weekly strategy specification](research/phase8_weekly/STRATEGY_SPEC.md)
- [Weekly research questions](research/phase8_weekly/RESEARCH_QUESTIONS.md)
- [Weekly research protocol](research/phase8_weekly/RESEARCH_PROTOCOL.md)
- [Weekly literature review](research/phase8_weekly/LITERATURE_REVIEW.md)
- [Weekly data-source manifest](research/phase8_weekly/DATA_SOURCE_MANIFEST.md)
- [Weekly cost/margin model](research/phase8_weekly/COST_MARGIN_MODEL.md)
- [Analytical weekly stress test](research/phase8_weekly/ANALYTICAL_WEEKLY_STRESS.md)
- [Weekly phase status](research/phase8_weekly/STATUS.md)
- [Research log](research/logs/RESEARCH_LOG.md)
- [Error log](research/logs/ERROR_LOG.md)

## Cost and broker realism
Weekly turnover makes friction more important. The model includes Paytm Money brokerage, statutory/regulatory/exchange charges, bid/ask spread, slippage, multi-leg execution, margin requirements and applicable square-off constraints.

## No trading conclusion yet
No live-trading recommendation or profitability conclusion has been established.
