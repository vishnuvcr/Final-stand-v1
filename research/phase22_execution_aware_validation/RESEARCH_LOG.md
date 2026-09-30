[object Object]

## 2026-09-30 — Strategy-horizon clarification
- Reviewed the frozen Phase 21 implementation and manuscript after a user challenge about the phrase “intraday strategy.”
- Confirmed that 10:00 IST is the entry timestamp and 14:00 IST is the lock timestamp, but these are not same-day open/close boundaries.
- The first trading day after the prior expiry is the entry day; the trading day before the target expiry is the lock day; remaining position may persist to target expiry unless stopped/exited earlier.
- Corrected the conversational characterization: **weekly-horizon strategy using intraday execution timestamps**, not an intraday-only strategy.


## 2026-09-30 — New execution-data lead identified
- Expanded the public-source search and identified `antony9952/Nifty_option_TBT` on Hugging Face.
- The public preview contains actual NIFTY option five-level bid/ask depth observations with quantities and timestamps, making it materially closer to the frozen execution contract than the previously admitted OHLC-only archives. citeturn2search0turn3view0
- The source is not yet admitted because its underlying CSV mixes incompatible schemas and the required historical coverage has not yet been demonstrated.
- Phase 22 remains holdout-locked. No configuration selection, parameter change, or execution assumption was introduced.
- Next step: file-level/immutable-revision coverage validation and deterministic extraction of quote/depth rows.


## 2026-09-30 — TBT source decomposition
- The Hugging Face repository contains a separate `market_depth.csv` file (48.5 MB) in addition to the mixed-schema `market_ticks.csv`. The depth file has an immutable Xet SHA-256 of `50c92a9c1ab2070224885392a7bd7e4ff94f046eeeef3e9af3289935343c6a05` and the repository commit history shows the file was uploaded on 2025-10-31. citeturn3view0turn5view0
- Its published preview demonstrates a clean nine-column five-level depth schema: id, tick_id, instrument_key, timestamp, depth_level, bid_price, bid_qty, ask_price, ask_qty. The preview shows timestamped levels 0–4 with positive bid/ask quantities. citeturn3view0
- This resolves the earlier concern that the **entire repository** was unusable because of the mixed `market_ticks.csv`; the separate depth file is a materially better candidate. However, the public evidence currently exposes a sample beginning 2025-10-27 and does not establish the complete weekly-expiry coverage required by Phase 22. The source therefore remains **candidate, not admitted**.
- Added manual GitHub Actions workflow `.github/workflows/phase-22-tbt-source-probe.yml` to download the depth file, verify the exact schema, scan timestamps/date coverage, validate bid<=ask and positive prices/quantities, verify all five depth levels, and preserve the immutable file/hash as an artifact.
