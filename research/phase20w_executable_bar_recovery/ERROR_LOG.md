# Phase 20W Error Log

No Phase-20 execution errors yet.


## E20-001 — 2026-09-30
- **Issue:** HF alternate-source inventory hit the same Polars timezone parser panic on `+05:30` parquet metadata.
- **Impact:** Source inventory stopped before comparing any alternate bars.
- **Correction:** Enable `POLARS_IGNORE_TIMEZONE_PARSE_ERROR=1` in the Phase-20 inventory workflow, matching the already validated HF-03 ingestion path. No timestamp values are modified.
