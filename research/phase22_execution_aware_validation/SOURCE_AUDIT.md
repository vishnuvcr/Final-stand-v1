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
