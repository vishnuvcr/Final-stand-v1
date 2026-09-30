# Phase 21W Error Log

## E21-001 — 2026-09-30
- HF-02 recovered cycle manifest lacked Phase-9 prior_expiry/status columns; mapped from the frozen 63-cycle calendar.
## E21-002
- HF-02 used oi rather than open_interest; renamed at the adapter boundary.
## E21-003
- A redundant HF-03 rebuild run was cancelled; reused the prepared artifact.
## E21-004
- Phase-19 persisted option-bar input was absent; rebuilt the frozen interface from the pinned source.
## E21-005 to E21-011
- Adapter schema mismatches (trading_day, symbol, option_type, expiry and ordering) were corrected without changing source price/timestamp values.
## E21-012
- Full metadata join/global duplicate grouping was too expensive; replaced by compact metadata reconstruction and source-local duplicate checks.
## E21-013
- Missing entry_timestamp, lock_timestamp and k3_multiplier fields were reconstructed from the admitted manifest/variant ID.
## E21-014
- GitHub runner shutdown occurred during combined-input construction; builder was changed to lazy/streaming parquet processing.
## E21-015
- Coverage validation incorrectly required all 63 expiries to be executable; corrected to 63 baseline + 58 covered + 5 missing.
## E21-016
- Phase-9 artifact path was restored under the wrong directory; corrected to the research/ interface path.
## E21-017
- Builder still used the old Phase-9 manifest path; corrected to research/phase9_weekly/output.
## E21-018
- 346.32 MB combined parquet exceeded GitHub's 100 MB single-file limit; switched repository persistence to compact outputs plus workflow artifact.
## E21-019
- No new execution error. The exact frozen 224-variant run completed successfully and produced the phase-closure result.