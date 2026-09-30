# Phase 21W — External Full-Strike Recovery Status

**State:** ACTIVE — the missing-five data gap is being audited against independent broker/API routes and public historical mirrors.

## Frozen gap
- Missing weekly expiries from the combined frozen rerun: 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13, 2026-05-12.
- Admission requires same-source exact CE observations at 10:00 and 14:00 IST plus complete intraday path for every selected strike; no synthetic bars, strike substitution or cross-source leg mixing.

## Current source findings
- Upstox documents an expired-option-contract endpoint and expired historical candles at 1-minute granularity; authenticated access is required.
- ICICI Breeze documents 1-minute NIFTY option history by expiry/right/strike; authenticated API credentials are required.
- Dhan documents minute-level rolling expired options but limits index-option selection to ATM through ATM±10, so exact coverage of the wider frozen strike family must be empirically checked.
- NSE publishes an option-chain CSV interface and sells historical F&O order/trade data; the public option-chain page is not itself a historical 1-minute archive.
- Hugging Face dataset thetrademarkk/india-index-options-1m is a public per-expiry 1-minute NIFTY options dataset with strike/option_type/expiry/OHLCV/OI fields and current files through August 2026. Its license is CC-BY-NC-4.0 and the dataset card says coverage is partial, especially for illiquid/far strikes.
- A separate Hugging Face dataset, rissin/nse-options-intraday, contains Upstox-sourced NIFTY 1-minute data from October 2024 through 2026, with strike/expiry/option_type/OHLCV fields; its license is listed as other and redistribution is subject to source-provider terms.

## Next executable gate
Run the public HF per-expiry probe for the five missing expiries, record file availability, schema, SHA-256, exact 10:00/14:00 coverage, unique CE strike counts and duplicate counts, then attempt exact frozen variant reconstruction only if the data pass source-level validation.