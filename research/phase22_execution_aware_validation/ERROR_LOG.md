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
