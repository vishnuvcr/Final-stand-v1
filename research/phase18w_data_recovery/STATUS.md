# Phase 18W Status — Exhaustive Data Recovery

**Status:** INITIALIZED — source audit and recovery in progress.

**Reason for reopening:** Phase 17W maximum usable coverage was 39/63 cycles. This is a data-availability limitation that should be investigated before interpreting the absence of promotion as a strategy-definition conclusion.

**Newly identified sources:**
- Hugging Face rissin/nse-options-intraday: NIFTY 1-minute intraday Oct 2024–2026. [Source](https://huggingface.co/datasets/rissin/nse-options-intraday)
- Hugging Face artist-23/nifty-options-data: about 34M rows, 2020-12-29 to 2025-12-26, 1-minute OHLC/OI/spot. [Source](https://huggingface.co/datasets/artist-23/nifty-options-data)
- Hugging Face thetrademarkk/india-index-options-1m: about 377M rows, roughly 2021–2026, NIFTY/BANKNIFTY/SENSEX 1-minute OHLC/OI. [Source](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m)
- Upstox expired-instrument API: documented 1-minute expired-contract OHLC/OI, with Plus entitlement. [Source](https://upstox.com/developer/api-documentation/get-expired-historical-candle-data/)
- NSE official historical contract and order/trade infrastructure. [Source](https://www.nseindia.com/static/market-data/eod-historical-data-subscription)
- Commercial NIFTY 1-minute/full-chain archive and 1-second archive. [Source](https://optionsdata.shop/data/nifty-options-historical-data)

These sources are discovered but not yet admitted. Empirical coverage and schema validation are required.

**Next action:** run the source inventory and then build the fixed 63-cycle coverage matrix.