# Phase 21W External Recovery Research Log

## 2026-09-30 — resumed from Phase 21 combined rerun

- Re-read the frozen Phase 21 combined rerun coverage contract.
- Confirmed the combined input has 58/63 executable expiries, 11,702 combined variant-cycle cells, zero HF-03/HF-02 overlap, and exactly five missing expiries.
- Confirmed the five missing expiries are all in the holdout segment: 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13 and 2026-05-12.
- Confirmed the current 224-variant summary is therefore not a final 63-cycle holdout result.

## 2026-09-30 — external-source audit expanded

- Reviewed public/external options-data routes and existing source-audit workflow.
- Added RISSIN/Hugging Face as the first new automated recovery candidate.
- Pinned RISSIN dataset revision 78b1c5468255d18cf492984bfe6fe4e3ac874d7c.
- The RISSIN dataset card documents NIFTY 1-minute intraday coverage from October 2024 through 2026 with expiry, strike, option type, OHLC and volume fields.
- Documented that RISSIN intraday OI is unavailable; OI is not part of the frozen execution-price path.
- Kept Upstox, ICICI Breeze, Dhan, NSE/BSE and MoneyTicks as fallback/audit routes. No paid data access was initiated.

## 2026-09-30 — implementation

- Added a pinned five-expiry recovery script.
- Added deterministic merge/coverage validation that rejects overlap and requires exactly 224 x 63 variant-cycle coverage before the final rerun.
- Extended the source-audit workflow with manual dispatch and push execution.
- The workflow reuses the latest successful Phase 21 and Phase 9 artifacts and the existing HF cache instead of downloading the already-admitted data again.
- The final rerun uses the exact Phase 17 frozen engine revision and unchanged cost/slippage/stop parameters.

## Next step

Run the external recovery workflow. If all five dates pass the 224-variant admission gate, complete the 63-cycle rerun and update the final statistical report. If any target fails, record the exact missing variant/date cells and continue only with another external source route.
