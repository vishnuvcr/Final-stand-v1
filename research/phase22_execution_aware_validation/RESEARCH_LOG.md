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


## 2026-09-30 — Phase 22 TBT source probe actually executed
- Re-established GitHub Actions visibility through the repository Actions REST endpoint.
- Workflow run 36737538413 downloaded `market_depth.csv` successfully and verified SHA-256 `50c92a9c1ab2070224885392a7bd7e4ff94f046eeeef3e9af3289935343c6a05`.
- Exact schema and depth levels 0–4 passed; chronology scan found 681,055 rows across only 2025-10-27 and 2025-10-28, with 57 invalid quote rows.
- Admission failed. The candidate is not sufficient for Phase 22's weekly-horizon multi-expiry execution-aware validation.
- Holdout remains locked.


## 2026-09-30 — Execution-source re-audit after TBT rejection
- Re-checked vendor documentation and public repositories for a genuinely retrievable multi-expiry bid/ask archive.
- TrueData remains the clearest technically documented route: historical NSE F&O bid/ask is supported, including tick history, but credentials/subscription are required.
- Global Datafeeds also exposes historical NFO bid/ask fields, but its published tick backfill window is one calendar week, so it does not solve the multi-year archive problem without additional provisioning.
- TickBytes and OptionVault advertise the required Level-2/tick coverage, but their full archives are licensed/private; only public samples/schema are available.
- No holdout opened; no execution-aware strategy backtest run.


## 2026-09-30 — Additional source leads
- NiftyTrader publicly advertises historical NIFTY option-chain snapshots containing bid/ask and bulk historical downloads; however, the underlying machine-readable archive and provenance/hash are not exposed in the public page, so it remains an unadmitted candidate.
- optionsdata.shop provides broad 1-minute and 1-second expired-option archives, but public documentation establishes OHLC/OI/volume rather than bid/ask, so it does not satisfy the frozen execution contract yet.


## 2026-09-30 — Phase 22A weekly 504-family expansion completed
- Created a separate Phase 22A branch to honor the requested weekly framing and extend K1 through OTM8/ITM8.
- Full 504-family completed successfully over the 63-expiry historical sample.
- All 504 configurations were valid for all 63 weekly cycles.
- Raw bootstrap p<0.05 occurred for 323/504 configurations; Holm-adjusted p<0.05 occurred for 0/504.
- No configuration passed the capital-promotion gate.
- The result is retrospective parameter-surface evidence only; it does not open or consume a new unseen holdout.
- Phase 22 remains open for genuinely new chronological validation and execution-aware evidence.
