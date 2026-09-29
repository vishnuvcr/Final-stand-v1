# Phase 15W — Free Historical Bid/Ask Source Audit

| Source | Indian NIFTY options | Bid/ask | Granularity | Historical coverage | Free complete archive? | Qualification |
|---|---|---|---|---|---|---|
| QuantDev-stack/TickBytes | Yes | L1 + top-5 L2 | Tick | Public sample only; subscription archive | No evidence | Sample qualified; archive not qualified |
| QuantDev-stack/OptionVault | Yes | 5 bid/ask levels in public sample | Snapshot | Public sample only; licensed full dataset | No | Sample qualified; archive not qualified |
| Hugging Face sources searched | Yes, OHLC sources | No qualifying L1/L2 source found | Mostly 1-min | Existing candidates are OHLC/derived | No qualifying source | Not qualified |
| Kaggle sources searched | Indian options exist | No qualifying historical L1/L2 archive established | Mixed | No complete qualifying archive established | No qualifying source | Not qualified |
| NSE public historical reports | Yes | EOD/contract data, not historical L1 | EOD/report | Official historical reports | No | Not qualified for execution quotes |
| NSE historical order/trade product | Yes | Order/trade messages | Tick/order-event | Official historical product | Paid/subscription | Potential paid route |

## Direct sample inspection

TickBytes NIFTY option tick sample exposes datetime, exact option symbol, expiry, strike, type, LTP/LTT/LTQ, best bid/ask and quantities, plus bid/ask levels 2 through 5. Its documentation states that the top-five book is updated at each tick.

OptionVault public NIFTY_level2.csv exposes timestamp, option symbol, five bid prices/quantities, five ask prices/quantities, LTP and volume.

## Critical interpretation

A public sample is evidence of schema and provenance only. It is not evidence that the historical archive is freely downloadable. The repositories explicitly distinguish evaluation samples from licensed/subscription historical datasets.

Therefore the samples must not be substituted for the 63-cycle historical sample or used to claim quote-validated backtest performance.

## Sources
- TickBytes: https://github.com/QuantDev-stack/TickBytes
- OptionVault: https://github.com/QuantDev-stack/OptionVault
- NSE historical data subscription: https://www.nseindia.com/static/market-data/eod-historical-data-subscription
- NSE real-time data specification: https://www.nseindia.com/static/market-data/real-time-data-subscription
- NSE historical reports: https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives