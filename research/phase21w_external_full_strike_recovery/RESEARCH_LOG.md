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

## 2026-09-30 — stale Rissin revision corrected
- Public-HF probe run 36711279624 confirmed the earlier failure was a true source-pin problem: revision `78b1c54` returned HTTP 404 for the 2026 NIFTY intraday parquet.
- The current dataset card documents NIFTY 1-minute intraday coverage through 2026, and a later dataset tree contains `upstox_intraday/NIFTY/NIFTY_2026.parquet`. citeturn769528search1turn627359search0
- The recovery scripts now resolve `main`, discover the exact 2026 NIFTY file, and record the resolved commit SHA plus file SHA-256 before use.
- Workflow push triggers were narrowed so generated output commits do not recursively launch the large recovery jobs.


## 2026-09-30 — first live RISSIN probe

- The corrected workflow successfully downloaded the 371,495,369-byte Phase 21 combined artifact from successful run 36709664677.
- Source audit completed successfully.
- The first live RISSIN probe reached Polars schema inspection and exposed a timezone-metadata compatibility error: the parquet declares +05:30, which the runner's Polars build rejected.
- The recovery script and workflow were corrected with POLARS_IGNORE_TIMEZONE_PARSE_ERROR=1 and explicit timestamp normalization.
- The latest branch head contains that correction. A new workflow run was not created automatically after the GitHub-API commit, so the corrected recovery remains pending execution. The phase therefore remains RUNNING and no 63-cycle conclusion has been published.

## 2026-09-30 — E21X-010 recovery provenance serialization fix
- The Rissin recovery script was audited after the timezone failure and found one remaining stale reference to the old fixed filename constant.
- The source manifest now records the exact dynamically resolved file path used for the download.
- The external workflow was simplified to retain only the valid post-merge Phase-9 restore step; the obsolete pre-merge restore step was removed.

## 2026-09-30 — E21X-011 timezone comparison correction
- The Rissin source parquet loaded successfully after the parser-compatibility fix.
- The next failure was a strict timezone mismatch between Asia/Kolkata Polars timestamps and Python datetime literals normalized as UTC.
- The recovery path now preserves the source timestamps but introduces a temporary UTC comparison column for entry/lock/range filters.
