# Phase 15W — Expanded Free-Source Audit (2026-09-30)

## Purpose
Re-run the free historical execution-data search across public datasets, repositories, research archives and broker/API routes. The qualification target is historical NIFTY weekly option best bid/ask, preferably with bid/ask quantities, at timestamps usable for the frozen 63-cycle strategy.

A source is not admitted merely because its schema contains bid/ask. It must also satisfy historical date coverage, expired-contract coverage, exact-contract addressability, timestamp fidelity, completeness, access/licensing and reproducibility.

## Qualification standard
- A — Quote-qualified: NIFTY index options; expired weekly contracts; study-date coverage; best bid/ask; timestamped intraday observations; exact contract identifiers; reproducible lawful access.
- B — Schema-qualified only: bid/ask/depth fields exist, but complete historical archive or coverage is not established.
- C — OHLC-qualified: useful for independent price/OI/volume cross-checks, but no historical bid/ask.
- D — Rejected: does not provide the required historical data or cannot address expired contracts.

## Findings
| Source | What was verified | Coverage/useful fields | Quote gate |
|---|---|---|---|
| Hugging Face — thetrademarkk/india-index-options-1m | Public 1-min NIFTY option chain by expiry | ~2021–2026; OHLCV/OI; partial strike coverage | C — no bid/ask |
| Hugging Face — rissin/nse-options-intraday | Public 1-min NIFTY/BANKNIFTY/SENSEX archive | NIFTY intraday from Oct 2024; OHLC/V/OI | C — no bid/ask |
| Hugging Face — artist-23/nifty-options-data | Public NIFTY option data | 2020–2025; OHLC, IV, volume, OI, strike/expiry | C — no bid/ask |
| Hugging Face — codepyx23/thetrademarkk/india-index-options-1m | Public 1-min index/options archive | NIFTY options from 2021 onward; OHLCV/OI | C — no bid/ask |
| Kaggle NIFTY option-chain archive | Public 1-min option-chain archive evaluated by an independent research repository | 77 expiries; 72 after Nov 2024 in the audit; OHLC/OI/volume/Greeks | C — later evaluation found no bid/ask |
| Zenodo — Bhat, Nifty spot, futures and options one-minute data | Public 320.9 MB archive | 1-min OHLC/volume, 2017–2020 | C — no bid/ask |
| GitHub — TickBytes | Public samples contain L1/L2 fields | Tick + top-5 depth + 1-sec/1-min; complete archive licensed/subscription | B |
| GitHub — OptionVault | Public market-depth samples contain top-5 bid/ask | Complete dataset 300+ GB; licensed/subscription | B |
| GitHub — ayyararyan/nse-options-pipeline | Repository documents captured_at, bid_price, ask_price, bid_qty, ask_qty | Actual NSEI-Data input is explicitly not tracked in Git | B/C — schema only |
| GitHub — djjain21 NSE F&O archive | README advertises 1-min 2015–2026 and tick market depth 2021–2025 | Free sample only; full data by inquiry | B |
| GitHub — cpbhamu615/NiftyAskBid | Public repository with bid/ask-themed name | README effectively empty; no usable public data found | D |
| ICICI Breeze | Official SDK exposes 1-min historical NFO option OHLC/OI by expiry/strike | Historical candles; documented response has no BBO | C |
| Upstox Expired Instruments API | Official API exposes expired option contracts and expired 1-min OHLC candles | Contract-addressable expired history; expired-instrument API requires Plus | C for quote validation |
| FYERS | Official support says expired option-chain bid, ask, OI, IV and LTP are unavailable | Active contracts only in chain | D |
| Kotak Neo historical API | Official docs say historical API returns OHLCV and excludes expired/delisted instruments | Active-contract historical candles | D/C |
| Angel One SmartAPI | Official docs expose historical NFO candles and OI | 1-min candles/OI; no historical BBO | C |
| Dhan expired-options API | Official support confirms dedicated expired-options endpoint | Potential historical OHLC/OI; not a free public BBO archive | C/B pending empirical test |
| OpenAlgo option-chain API | Public docs show live bid/ask/bid_qty/ask_qty fields | Live chain schema; no qualified historical archive | B/D |
| Options Data | Public vendor pages offer 1-min/1-sec NIFTY OHLC/OI archives | Independent price cross-check; documentation excludes bid/ask | C |

## Important new finding: free broker/API routes
- ICICI Breeze is useful for 1-minute historical NFO option OHLC/OI because the API accepts NIFTY, expiry, strike and right. Its documented historical response does not contain best bid/ask.
- Upstox now has explicit expired-contract APIs and 1-minute expired historical candles, but the expired-instrument endpoints are restricted to the Plus plan. This is not a free quote archive.
- FYERS explicitly states expired option-chain bid, ask, OI, IV and LTP are not available through its option-chain interface.
- Kotak Neo's current historical API documentation explicitly excludes expired/delisted instruments.
- Angel One's historical API provides NFO candles/OI but not historical BBO.

Therefore these APIs can help with OHLC cross-validation and data-interface testing, but none is presently qualified as a free historical BBO source.

## Important new GitHub finding
ayyararyan/nse-options-pipeline uses the desired BBO schema: captured_at, symbol, expiry, strike_price, option_type, bid_price, ask_price, bid_qty, ask_qty, open_interest, total_traded_volume and underlying_value.
However, the repository states that the NSEI-Data input directory is not tracked in Git because it is too large. The repository therefore proves a real-world collection schema, not a freely downloadable historical archive.

## Independent Kaggle finding
A separately audited public research repository reports a free Kaggle 1-minute NIFTY option-chain archive with 77 expiries and 72 expiries after November 2024. Its later evaluation states that the archive was adopted for backtesting but contains no bid/ask, so slippage remained assumed rather than observed.

## Zenodo finding
The Zenodo archive by Aparna Bhat is an openly downloadable historical NIFTY spot/futures/options dataset covering 2017–2020 at 1-minute resolution. Its option files contain trade date/time and OHLC/volume, not BBO. It is useful only as an older independent OHLC source.

## Search conclusion
1. No free historical NIFTY weekly-options BBO archive has been qualified.
2. Multiple free OHLC archives exist and can cross-check the existing Phase 9 price reconstruction.
3. Public repositories prove BBO/L2 collection is technically feasible, but their complete archives are licensed, subscription-only, private, or not tracked.
4. Free broker APIs are useful for OHLC/contract discovery but do not currently provide a verified free historical BBO archive.
5. The most valuable next zero-cost experiment is a direct empirical probe of any user-authorized broker/API account that can legally access expired NIFTY contracts, while preserving the frozen strategy and holdout.

## Research-control decision
No strategy parameter, stop, strike-selection rule, holdout observation, or cost assumption was changed.

**FREE HISTORICAL BBO: NOT QUALIFIED.**

The next Phase 15W work is exact coverage probes for any user-authorized free API credentials, independent OHLC cross-validation, targeted historical BBO extract requests if a free route fails, and capital/margin reconstruction.