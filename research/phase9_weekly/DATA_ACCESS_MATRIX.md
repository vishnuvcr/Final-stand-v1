# Phase 9W — Weekly Historical Data Access Matrix

## Admission principle

The primary weekly backtest requires point-in-time option prices around the frozen entry, lock, stop and exit events. No dataset is admitted as equivalent to a historical bid/ask feed unless it contains point-in-time bid/ask or an independently validated executable-price reconstruction.

## Hugging Face candidates

| Source | Coverage | Granularity | Fields relevant to strategy | Primary use | Admission status |
|---|---|---|---|---|---|
| thetrademarkk/india-index-options-1m | NIFTY/BANKNIFTY/SENSEX, ~2021–2026 | 1-minute | OHLC, volume, OI, expiry, strike, option type; separate 1-minute NIFTY spot file | Primary weekly option-chain research source | Admit for 1-minute OHLC research; not true bid/ask |
| rissin/nse-options-intraday | NIFTY/BANKNIFTY/SENSEX, intraday from Oct-2024; daily history earlier | 1-minute | OHLC, volume; OI unavailable on Upstox intraday rows; source metadata | Independent cross-check of overlapping NIFTY weekly prices | Admit for cross-validation; not true bid/ask |
| artist-23/nifty-options-data | NIFTY, 2020-12 to 2025-12 | 1-minute | OHLC, IV, volume, OI, spot, strike price, expiry type, strike type, option type | Secondary IV/spot diagnostics and legacy coverage check | Admit for diagnostics; limited strike coverage must be audited |

## Execution interpretation

The HF primary source reports 1-minute OHLC rather than a historical order book.

1. Strike selection uses the recorded 10:00 OHLC price proxy, not a midpoint.
2. Long entries/long buybacks are stress-tested against the bar high plus explicit slippage.
3. Short sales/short covers are stress-tested against conservative low/high prices plus explicit slippage.
4. Every result carries an execution-quality label.
5. Genuine bid/ask datasets, when found, supersede this OHLC reconstruction for the primary execution result.

The OHLC reconstruction is therefore a research backtest with conservative price bounds, not evidence that historical fills occurred at those prices.

## Cache and licensing rule

The large source Parquet files are not copied into the public Git repository by default. The Phase 9 workflow uses the Hugging Face cache and records source revision, file names, sizes and SHA-256 hashes in the repository. Small derived research metadata/ledgers may be committed.

The primary dataset is published under CC-BY-NC-4.0. Redistribution rights are therefore not assumed.

## Gate criteria

Phase 9 passes only when the pilot demonstrates:

- at least 52 usable weekly expiry cycles;
- at least 95% usable K1/K2/K3 entry observations;
- at least 95% usable K2/K1/K3 lock observations;
- no unresolved contract-date look-ahead;
- no material duplicate-key corruption;
- source checksums recorded;
- an independent overlapping-source comparison for a meaningful subset;
- explicit identification of all cycles where execution is reconstructed from OHLC rather than observed bid/ask.
