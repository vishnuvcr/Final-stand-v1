# Phase 22W — Data Source Audit

## Status
**22.1 complete — execution-aware source landscape mapped; no paid data acquired.**

## Findings

| Source | Data | Bid/Ask / depth | Historical coverage | Admission status |
|---|---|---|---|---|
| NSE Data & Analytics | Official historical EOD/order/trade products | Order/trade; official historical products | Exchange data products | **Primary authoritative route; access/subscription required** |
| NSE real-time products | Level 1/2/3/tick | L1 best bid/ask; L2 top 5; L3 top 20; tick full book | Real-time product, historical availability depends product | **Execution schema confirmed; historical access must be obtained/verified** |
| RISSIN HF | 1-min NIFTY/BANKNIFTY/SENSEX OHLCV/OI | No bid/ask | Oct 2024→2026 | **Already admitted for Phase 21 recovery; OHLC fallback only** |
| TradeMarkk HF | 1-min index/options OHLCV/OI | No bid/ask | ~2021→2026; partial option coverage | **Independent OHLC cross-check candidate** |
| QuantDev-stack TickBytes | Tick/L2/1-sec/1-min | Advertises L1/L2 | Current archive/subscription | **Potential execution-data candidate; sample/public schema only; no purchase without authorization** |
| QuantDev-stack OptionVault | 1-min/tick/Level-2 | Advertises tick/depth | 2018→present depending product | **Potential execution-data candidate; licensed full dataset** |
| optionsdata.shop | 1-min option bars | No bid/ask | Jan 2023→Sep 2026 | **Commercial OHLC fallback; no purchase without authorization** |
| GitHub NIFTY market-data engine | Query layer over Kaggle/other files | No verified bid/ask | 2024 + live 2026 | **Useful engineering/source-discovery route, not execution evidence** |

## Key external evidence

- NSE's official historical-data documentation describes F&O historical order data at tick frequency, including transaction time, buy/sell indicator, order number and instrument fields. citeturn0search44
- NSE's real-time market-data documentation explicitly defines Level 1 as best bid/ask, Level 2 as five levels of depth, Level 3 as twenty levels, and tick-by-tick as full order-book data. citeturn0search12
- NSE provides paid historical EOD and historical order/trade products, with F&O technical specifications and sample files. citeturn0search1
- RISSIN provides 1-minute OHLCV/OI but not executable quote data. citeturn0search0
- TradeMarkk provides an independent 1-minute OHLCV/OI archive but explicitly warns that option coverage can be partial. citeturn0search13
- Public GitHub datasets advertise deeper tick/Level-2 archives, but the complete data are licensed/subscription data and therefore cannot be assumed available. citeturn0search3turn0search9

## Phase 22 admission rule

No execution-aware result will be admitted until the data source demonstrably contains timestamped executable bid/ask/depth observations for the exact NIFTY option contracts and periods used by the new experiment.

No purchase or external credential use is authorized by this phase plan.


## 22.1B — Broker/API route audit (2026-09-30)

- Upstox documents live market-feed bid/ask quantities and prices and D0/D5 depth, plus expired-option contract/candle APIs. Its documented historical expired-instrument endpoint is OHLC, not historical bid/ask/depth. citeturn0search1turn1search4turn1search9
- Upstox option-chain APIs expose current bid/ask price and quantity, but this is a live/current option-chain interface rather than a historical quote archive. citeturn1search3
- Dhan documents historical expired-options data at one-minute resolution with OHLC, IV, OI, volume and spot, but the historical endpoint does not document bid/ask fields. Dhan's 20/200-level depth is documented as real-time websocket data. citeturn1search0turn1search12
- ICICI Breeze's documented historical options API returns minute OHLC/volume and does not expose historical bid/ask in the shown response. citeturn2search5
- A public GitHub NIFTY options analytics repository describes snapshot CSVs containing captured_at, bid_price, ask_price, bid_qty and ask_qty, but its data directory is explicitly not tracked in Git; therefore the repository does not itself provide an admissible reproducible historical quote archive. citeturn2search3
- A separate public NIFTY data-engine repository explicitly states that bid/ask quotes are not available and market_price is substituted from close_price, so it is not execution evidence. citeturn2search0

### Updated admission conclusion

The audit has now covered official NSE historical order/trade products, public OHLC archives, broker APIs with current depth, broker expired-contract historical candles, and public GitHub snapshot schemas. No reproducible, freely accessible historical NIFTY option bid/ask/depth archive has yet been admitted for Phase 22. The official NSE historical order/trade route remains the authoritative candidate, while broker live-depth APIs could support a future prospective collection study but cannot reconstruct past quotes.

No new holdout is opened until an admissible historical execution dataset exists.


## 22.1C — TrueData historical bid/ask route (2026-09-30)

- TrueData states that its Market Data API supports NSE Futures & Options and that historical data are available with or without Bid/Ask history. Its documentation describes Level-1 best bid/ask as part of the feed. citeturn3search8turn3search0
- The TrueData historical client code exposes tick-history retrieval with a bidask flag, supporting historical tick responses containing bid, bid quantity, ask and ask quantity. citeturn3search1
- This makes TrueData the strongest currently identified vendor route for satisfying the Phase 22 execution-data contract, subject to actual access, coverage verification, licensing and reproducible download.
- No TrueData credentials are present in the research protocol, and no paid subscription has been authorized. Therefore no TrueData data are admitted yet.

### Route status

**Strong candidate — access pending.** If an authorized trial/subscription or existing credential becomes available, the first acquisition test should use a small historical NIFTY weekly-expiry sample and verify exact timestamp, expiry, strike, CE/PE, bid/ask, bid/ask quantity, and source provenance before any full acquisition.
