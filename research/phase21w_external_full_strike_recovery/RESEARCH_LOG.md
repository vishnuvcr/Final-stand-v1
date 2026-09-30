# Phase 21W External Full-Strike Recovery Research Log

## 2026-09-30 — External-source audit expansion
- The frozen combined rerun identified five completely missing weekly expiries: 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13 and 2026-05-12.
- Independent broker/API documentation was checked for Upstox, ICICI Breeze and Dhan. NSE official historical products were also reviewed.
- A new public Hugging Face candidate was identified: thetrademarkk/india-index-options-1m. The dataset exposes per-expiry NIFTY 1-minute option parquet files with strike, option_type, expiry, OHLCV and OI fields, but its card explicitly warns that option coverage is partial and its license is CC-BY-NC-4.0.
- Because source-level dataset presence is not evidence of exact variant coverage, a deterministic five-expiry probe was added before any strategy backtest integration.

## Probe protocol
- Resolve and record the Hugging Face dataset revision.
- Download only the five missing expiry files; cache them through the workflow cache.
- Record SHA-256 hashes and schema.
- Require exact CE contract rows, zero duplicate timestamp/strike groups and non-null OHLC/volume/strike fields.
- Count distinct CE strikes at exactly 10:00 and 14:00 IST and their intersection.
- Do not admit the source to the frozen backtest solely from strike counts; exact variant construction and intraday stop-path availability remain downstream gates.