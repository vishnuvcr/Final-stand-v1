# Phase 18W — Exhaustive Historical Data Recovery

## Purpose
Re-open the historical-data bottleneck that constrained Phase 17W. This phase does not change the frozen weekly strategy, 224 registered configurations, 63-cycle calendar, 37/12/14 chronology, costs, slippage, stop, or holdout rules. Its only purpose is to improve historical data coverage and execution-data quality.

## Research questions
1. Can missing weekly NIFTY option observations be recovered from additional public/free datasets?
2. Can broker APIs with expired-instrument access recover missing 1-minute OHLC/OI observations?
3. Can public GitHub/Kaggle/Hugging Face/Zenodo archives cross-fill missing dates/contracts without leakage or synthetic prices?
4. Can commercial archives provide materially higher coverage, and separately, historical bid/ask/order-book data?
5. What fraction of the 63 cycles and Phase-17 records can be made reproducible from independently sourced data?
6. Does recovered coverage change the Phase-17 promotion decision when the original gate is reapplied unchanged?

## Registered source classes
- Hugging Face public datasets.
- GitHub repositories and lawful public archives.
- Kaggle and Zenodo datasets.
- Broker/API routes: Upstox expired instruments, ICICI Direct Breeze, Dhan, Angel One SmartAPI, Zerodha/Kite where applicable.
- NSE official historical contract, trade/order, report and risk-data infrastructure.
- Commercial OHLC/OI archives.
- Commercial L1/BBO/order-book vendors such as TrueData and Global Datafeeds.

## Frozen downstream protocol
- Weekly expiry definition, 10:00 IST entry, 14:00 IST lock and 50-point stop remain unchanged.
- Slippage remains 0.50 NIFTY points per leg.
- Paytm Money transaction-cost model remains unchanged.
- All 224 Phase-17 configurations remain exactly registered.
- 63-cycle calendar and 37/12/14 chronology remain fixed.
- Untouched holdout remains descriptive and unavailable for selection.
- No new strategy parameters may be selected from recovered results.

## Phase steps
1. Freeze protocol and source registry.
2. Audit newly discovered public/free sources and provenance.
3. Download/cache eligible public datasets using HF_TOKEN where applicable.
4. Probe broker/API sources when credentials and entitlements are available; never commit secrets.
5. Probe official and commercial sources; purchase only with explicit authorization.
6. Build a source-by-date-by-contract coverage matrix against the fixed 63-cycle manifest.
7. Merge sources with deterministic precedence; never silently blend conflicting prices.
8. Rerun the unchanged Phase-17 evaluation if coverage permits.
9. Compare recovered coverage/results with the original Phase-17 audit.
10. Close only after registered source classes are exhausted or demonstrably blocked.

## Stopping rule
Stop after all registered source classes are probed and either sufficient data are recovered to rerun the frozen experiment, or every remaining source is demonstrably inaccessible, incomplete, licensed, or technically incapable of supplying the required observations.

## Promotion rule
The original Phase-17 gate is retained unchanged: at least 50/63 valid cycles, positive training and validation mean net P&L, and Holm-adjusted one-sided training bootstrap p < 0.05. No new threshold may be introduced after observing results.