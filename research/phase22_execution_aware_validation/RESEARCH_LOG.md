# Phase 22W Research Log

## 2026-09-30 — Initiation
- Created Phase 22 branch from main.
- Completed source audit across official NSE documentation and public OHLC/tick/depth candidates.
- Frozen execution-data contract.
- Frozen complete 224-configuration prospective registry.
- Defined manual workflow gates and reproducibility requirements.
- No new holdout has been inspected or opened.
## 2026-09-30 — Expanded execution-data audit
- Audited Upstox live depth/bid-ask and expired-instrument historical endpoints.
- Audited Dhan historical expired-option data and real-time 20/200-level depth.
- Audited ICICI Breeze historical option candles.
- Audited public GitHub repositories advertising bid/ask snapshot schemas.
- Result: no freely accessible, immutable historical bid/ask/depth archive has yet been admitted.
- Added a manual GitHub Actions workflow with a hard refusal gate when the execution-data cache is absent.
- Phase remains blocked at execution-data admission; no new holdout opened and no Phase 21W configuration selected post hoc.

## 2026-09-30 — Strongest vendor route identified
- TrueData documentation confirms historical NSE F&O data with optional Bid/Ask history and a historical tick interface with bid/ask quantities.
- TrueData is now the primary acquisition candidate for Phase 22 execution data.
- No credentials or paid subscription are assumed; no vendor data have been admitted.
- Admission remains gated on a real sample, exact schema validation, provenance and SHA-256 hashing.

## 2026-09-30 — TrueData retention check
- Verified current TrueData documentation: default REST tick history is 5 trading days; intraday bars are 6 months; extended history is an add-on.
- TrueData remains technically suitable for bid/ask schema, but default access is insufficient for the retrospective Phase 22 target periods.
- No data admission or holdout opening occurred.

## 2026-09-30 — TrueData coverage qualification
- Confirmed TrueData supports historical Bid/Ask fields suitable for the execution contract.
- Confirmed default REST tick history is limited to the last 5 trading days; extended history is an add-on.
- Corrected the earlier assumption that TrueData automatically supplies the required multi-year historical archive.
- No data admitted and no holdout opened; authorized historical sample remains the next gate.
