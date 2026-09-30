# Phase 21W External Full-Strike Recovery Error Log

## E21X-001 — 2026-09-30
- **Issue:** Earlier external source audit recorded broker/API routes as not tested.
- **Correction:** Expanded the audit with current endpoint/documentation evidence and separated documentary qualification from empirical admission.

## E21X-002 — 2026-09-30
- **Issue:** A public dataset with a matching per-expiry 1-minute option schema could be overlooked if only broker APIs were considered.
- **Correction:** Added thetrademarkk/india-index-options-1m as a candidate route and created a deterministic five-expiry probe.

## E21X-003 — 2026-09-30
- **Issue:** Public dataset presence does not guarantee full-strike coverage or acceptable licensing for later capital use.
- **Correction:** Probe exact missing expiries, record provenance, and carry the dataset's CC-BY-NC-4.0 / educational-use limitation into admission criteria.

## E21X-004 — 2026-09-30
- **Issue:** The first public-HF probe reached the downloaded parquet but Polars rejected the dataset's fixed-offset timestamp metadata (+05:30).
- **Impact:** No source-level probe rows were produced in run 36710896827.
- **Correction:** Reuse the repository's established fixed-offset timezone compatibility setting by setting POLARS_IGNORE_TIMEZONE_PARSE_ERROR=1 before importing Polars; timestamps remain explicitly treated as IST in the probe.
- **Prevention:** Third-party parquet ingestion probes must apply the same timezone-compatibility contract already validated in Phase 13W before reading schemas.

## E21X-006 — 2026-09-30
- **Issue:** The external recovery status had drifted from the frozen 37/12/14 chronological split to 60/20/20.
- **Impact:** This could have contaminated the definition of training, validation and untouched holdout during recovery.
- **Correction:** Restore 37/12/14 everywhere and add an explicit frozen-split check before external backtest integration.
- **Prevention:** Recovery branches may fill missing observations but may not redefine experimental chronology; validate the split before every downstream rerun.
