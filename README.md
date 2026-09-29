# Final Stand v1 — Market Inefficiency Research

## Current status
**Active experiment: Phase 13W — Untouched weekly holdout of the NIFTY call-ladder-to-spread strategy.**

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
- Phase 9W — HF weekly data gate: 🟡 active
- Phase 10W — mechanics/margin/costs: 🟡 active
- Phase 11W — weekly backtest: pending
- Phase 12W — robustness: pending
- Phase 13W — untouched holdout: 🟡 re-running after deterministic workflow-path correction
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

## Phase 9W Hugging Face data gate
A primary Hugging Face source has been identified: thetrademarkk/india-index-options-1m, with 1-minute NIFTY option data partitioned by expiry and a separate NIFTY spot file. Its documented schema contains OHLC, volume and open interest, not historical bid/ask. A second HF source, rissin/nse-options-intraday, provides an independent 1-minute NIFTY OHLC series from October 2024 onward. See research/phase9_weekly/DATA_ACCESS_MATRIX.md for the admission rules and execution-quality distinction.

## No trading conclusion yet
No live-trading recommendation or profitability conclusion has been established. Runs 36595701035 and 36596109078 are classified as pipeline failures: each ingested 63 usable cycles but generated zero trades. The second run supplied explicit Phase 9 paths, so the remaining issue is now being diagnosed at the row-level data interface before any empirical conclusion is admitted.
