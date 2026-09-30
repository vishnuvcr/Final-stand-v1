# Phase 20W Error Log

No Phase-20 execution errors yet.


## E20-001 — 2026-09-30
- **Issue:** HF alternate-source inventory hit the same Polars timezone parser panic on `+05:30` parquet metadata.
- **Impact:** Source inventory stopped before comparing any alternate bars.
- **Correction:** Enable `POLARS_IGNORE_TIMEZONE_PARSE_ERROR=1` in the Phase-20 inventory workflow, matching the already validated HF-03 ingestion path. No timestamp values are modified.


## E20-002 — 2026-09-30
- **Issue:** The missing-cycle inventory filtered a Polars `Date` column against string expiry values, producing an empty required-variant inventory.
- **Impact:** Recovery stopped before downloading or admitting any alternate bars.
- **Correction:** Normalize `target_expiry` to ISO strings before filtering. No source precedence or bar-admission rule changed.


## E20-003 — 2026-09-30
- **Issue:** HF-01 NIFTY parquet encodes timestamps with `+0530`, which the current Polars reader rejects while casting the timestamp column.
- **Impact:** Alternate-source recovery stopped before evaluating any HF-01 rows.
- **Correction:** Use Polars' PyArrow parquet reader for HF-01 source files. This is a reader compatibility change only; timestamps and OHLC observations are not transformed.
