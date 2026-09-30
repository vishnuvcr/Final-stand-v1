# Phase 21W External Source Audit — 2026-09-30

| Route | Documented capability | Access / limitation | Current admission state |
|---|---|---|---|
| Upstox expired option contracts + expired candles | Expired NIFTY option contracts plus 1-minute OHLC history | OAuth/access token; expired-candle entitlement is broker/account dependent | Documentary qualification; empirical admission pending credentials |
| ICICI Breeze | Historical NIFTY options by expiry, right and strike at 1-minute interval | Breeze API key/session required; max 1,000 candles per historical V2 request | Documentary qualification; empirical admission pending credentials |
| Dhan rolling expired options | Minute-level expired index options, OHLC/IV/volume/OI/spot | Index selection documented as ATM through ATM±10; credentials required | Candidate; exact frozen strike coverage pending probe |
| NSE official | Current option-chain CSV plus paid historical order/trade/F&O data | Public option-chain is not a historical intraday archive; historical products are controlled/paid | Supplementary source, not yet an admitted 1-minute source |
| thetrademarkk/india-index-options-1m | Per-expiry NIFTY 1-minute OHLCV(+OI), strike/option_type/expiry | CC-BY-NC-4.0; educational use; partial/far-strike coverage caveat | **Probe queued** for the five missing expiries |
| rissin/nse-options-intraday | NIFTY 1-minute intraday track from Oct 2024 through 2026, plus daily history | License listed as other; intraday source is Upstox and redistribution follows source terms | Candidate secondary mirror; probe later if needed |

## External evidence
- Upstox expired option contracts: https://upstox.com/developer/api-documentation/get-expired-option-contracts/
- Upstox expired historical candles: https://upstox.com/developer/api-documentation/get-expired-historical-candle-data/
- Dhan expired options: https://dhanhq.co/docs/v2/expired-options-data/
- NSE option chain: https://www.nseindia.com/option-chain
- NSE paid EOD/historical data: https://www.nseindia.com/static/market-data/eod-historical-data-subscription
- Breeze historical options example: https://github.com/nocturnalknight/Breeze
- Breeze downloader project: https://github.com/mukhilj/breeze_options_pipeline
- Public HF NIFTY 1-minute options dataset: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- Public HF NIFTY intraday mirror: https://huggingface.co/datasets/rissin/nse-options-intraday

## Admission rule
Documented endpoint capability is not sufficient for admission. A source must provide the actual missing expiry, exact contract/strike fields, valid 1-minute OHLC observations, exact entry and lock timestamps, intraday stop-path bars, deterministic provenance and acceptable redistribution/usage rights for the intended research stage.