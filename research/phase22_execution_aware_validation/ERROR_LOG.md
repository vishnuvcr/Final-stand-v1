# Phase 22W Error Log

## E22-001 — No public executable historical quote archive admitted yet
- **Observed:** publicly discoverable RISSIN and TradeMarkk datasets provide 1-minute OHLCV/OI rather than timestamped bid/ask execution quotes.
- **Impact:** they cannot serve as the primary execution-aware dataset.
- **Correction:** retain them only as fallback/cross-check sources and continue the registered NSE/order-trade/depth source audit.
- **No purchase authorized:** no commercial dataset has been purchased.

## E22-002 — Broker historical APIs do not provide the required execution archive
- **Observed:** Upstox exposes live bid/ask/depth and expired-option historical OHLC; Dhan exposes historical expired-option OHLC and real-time 20/200-level depth; Breeze exposes historical option OHLC. None of the documented historical endpoints inspected provides timestamped historical bid/ask/depth for the required contracts.
- **Impact:** these APIs cannot yet satisfy the Phase 22 execution-data contract.
- **Correction:** keep broker APIs documented as live/prospective collection candidates; do not synthesize historical quotes from candles or current option-chain data.

## E22-003 — Public GitHub bid/ask schema without reproducible data archive
- **Observed:** a public NIFTY options analytics repository documents snapshot files with bid/ask fields, but explicitly says the data directory is not tracked in Git.
- **Impact:** schema evidence is not data evidence; the source cannot be admitted without an accessible immutable dataset.
- **Correction:** treat as source lead only; require actual files, provenance and hash before admission.


## E22-004 — Strong execution-data vendor identified but access is not provisioned
- **Observed:** TrueData documents historical NSE F&O data with optional Bid/Ask history and a historical tick API supporting bid/ask fields.
- **Impact:** the technical data contract may be satisfiable, but no authorized credential/subscription is available to the research workflow at present.
- **Correction:** record TrueData as the primary vendor acquisition candidate; do not claim data admission until a real sample is obtained, hashed and schema-validated. No paid purchase or credential fabrication.

## E22-005 — Default TrueData tick retention is too short for retrospective Phase 22
- **Observed:** current TrueData documentation says default REST tick history is limited to the last five trading days; extended history is an add-on.
- **Impact:** default access cannot supply the historical weekly-expiry periods needed for the planned retrospective train/validation/holdout experiment.
- **Correction:** require verified extended-history entitlement covering the target dates before admission. Do not substitute current ticks for historical periods or alter the experiment dates to fit the data.

## E22-006 — GFDL default tick retention is too short
- **Observed:** GFDL documents NFO historical tick data with bid/ask fields, but its documented backfill is one calendar week.
- **Impact:** default history cannot cover the retrospective Phase 22 target periods.
- **Correction:** treat GFDL as a prospective/short-window execution-data route unless an archival entitlement is verified.

## E22-007 — NSE full-order reconstruction requires exchange-data access
- **Observed:** NSE documents complete historical order-book events and trades with timestamps, prices, volumes and identifiers, but access is provided as a subscribed historical data product.
- **Impact:** the strongest authoritative reconstruction route is not currently accessible to the workflow.
- **Correction:** do not infer access or fabricate downloads; keep the route first priority for authorized acquisition.


## E22-005 — TrueData historical-depth availability is access-dependent
- **Observed:** TrueData documents historical Bid/Ask support, but its default REST tick-history window is only the last 5 trading days; extended history is an add-on. Historical Bid/Ask is also documented through its WebSocket service.
- **Impact:** TrueData cannot yet be treated as an automatically available multi-year source for the Phase 22 holdout.
- **Correction:** require an authorized historical sample and explicit coverage confirmation before admission; no assumption of multi-year access.


## E22-006 — Global Datafeeds historical retention/access not yet verified
- **Observed:** Global Datafeeds documents historical NFO tick responses containing bid/ask prices and quantities, but public documentation does not establish that the complete 2024–2026 weekly-option history required by Phase 22 is freely accessible.
- **Impact:** technically suitable schema is confirmed, but data admission and retention are unverified.
- **Correction:** require an authorized historical sample and coverage verification before treating the source as admitted.


## E22-008 — Intraday-only characterization was incorrect
- **Observed:** the strategy was described in conversation as an intraday strategy with no overnight holding.
- **Correct interpretation:** the frozen weekly protocol uses **intraday timestamps for entry and lock decisions**, but the trade has a **weekly horizon**. Entry occurs at 10:00 IST on the first trading day after the prior expiry; the lock occurs at 14:00 IST on the trading day before the target expiry; remaining exposure can continue to expiry unless the stop/exit rules terminate it earlier.
- **Impact:** the prior conversational description incorrectly implied same-day closure and no overnight holding.
- **Correction:** all future descriptions must call this a **weekly-expiry/weekly-horizon strategy with intraday execution timestamps**, not an intraday-only strategy. No research code or frozen parameters are changed by this clarification.


## E22-009 — Public NIFTY TBT dataset has mixed incompatible schemas
- **Observed:** `antony9952/Nifty_option_TBT` exposes genuine timestamped five-level bid/ask/depth fields in its preview, but Hugging Face reports that `market_ticks.csv` contains mixed row schemas: depth rows with 7 quote/depth fields and other rows with 18 LTP/OHLC/volume/OI fields. The dataset viewer therefore fails schema casting. citeturn3view0
- **Impact:** the source cannot yet be treated as a clean reproducible execution archive. Blindly loading it could drop or misinterpret quote observations.
- **Correction:** retain the source as a high-priority acquisition lead. Require immutable revision/file manifest, deterministic quote-row isolation, exact contract mapping, chronological coverage validation and SHA-256 hashing before admission. No holdout opened.
- **Additional environment issue:** direct container HTTP access to Hugging Face failed because DNS/network resolution is unavailable in the current execution environment; web-source evidence was used instead. This does not establish that the dataset itself is inaccessible to GitHub Actions, so it is not a rejection criterion.


## E22-010 — Probe execution unavailable in current GitHub connector session
- **Observed:** the Phase 22 manual probe workflow was created correctly, but the available GitHub connector exposes workflow inspection/rerun operations and does not expose a workflow-dispatch operation. Direct container download of the Hugging Face file also failed in this session.
- **Impact:** the source cannot be admitted merely from the public preview; no claim of a completed Actions probe is made.
- **Correction:** preserve the manual workflow as the reproducible next execution step. Continue source assessment only from independently verifiable public metadata/preview until a workflow run or authorized file download is available.


## E22-011 — TBT probe executed: only two dates and 57 invalid quote rows
- Date: 2026-09-30
- Workflow run: 36737538413
- Source: `antony9952/Nifty_option_TBT/market_depth.csv`
- SHA-256: `50c92a9c1ab2070224885392a7bd7e4ff94f046eeeef3e9af3289935343c6a05`
- Download succeeded (46.2 MiB); exact 9-column schema and depth levels 0–4 were present.
- Scan found 681,055 rows, 4 instruments, but only 2 dates: 2025-10-27 through 2025-10-28.
- 57 rows violated the basic quote contract. The workflow therefore failed admission.
- This source cannot currently support the Phase 22 weekly-horizon new-data validation because its observed coverage is far short of the required multi-expiry chronological sample.
- No holdout was opened and no strategy result was produced.
