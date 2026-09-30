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
## 2026-09-30 — E21X-004 timezone compatibility correction
- The first public-HF probe downloaded the candidate files but failed before reading schema because Polars rejected fixed-offset +05:30 parquet metadata.
- The fix is limited to the known timezone-parser compatibility setting already used by the Phase-9/13 ingestion path; no source data are transformed or reinterpreted.

## 2026-09-30 — Frozen-split correction and Rissin probe activation
- The external status file had drifted to a 60/20/20 split; this was incorrect for the frozen Phase-21 design. It is restored to the Phase-17/21 chronology of 37/12/14 train/validation/holdout.
- The public Rissin dataset is now the first empirical external probe because it covers all five missing dates in its documented 2026 NIFTY 1-minute archive window and exposes the fields required by the OHLC backtester.
- The probe is pinned to the published revision 78b1c5468255d18cf492984bfe6fe4e3ac874d7c and uses the repository HF_TOKEN secret when available.
