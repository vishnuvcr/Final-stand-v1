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


## E20-004 — 2026-09-30
- **Issue:** Even the PyArrow-backed Polars frame retained the problematic timezone metadata when converting HF-01 timestamps to strings.
- **Impact:** Recovery stopped before evaluating HF-01 observations.
- **Correction:** HF-01 recovery will use predicate-pushed PyArrow reads filtered by expiry/date, then normalize only the small filtered timestamp column to strings before Polars processing. This avoids materializing/reinterpreting the full annual parquet timezone column.


## E20-005 — 2026-09-30
- **Issue:** HF-02 fallback used `is_between(entry, end)` with string arguments interpreted by Polars as column expressions.
- **Impact:** Recovery stopped when reaching the early-period HF-02 source after HF-01 processing succeeded.
- **Correction:** Wrap timestamp bounds in `pl.lit(...)` for the HF-02 fallback. No data or selection rule changes.


## E20-006 — 2026-09-30
- **Issue:** Five missing 2026 target cycles have no frozen Phase-9 entry spot, and HF-02 ends in 2025.
- **Impact:** Those five cycles cannot yet be admitted without an exact 10:00 IST NIFTY spot source.
- **Correction:** For 2024–2025 missing cycles only, recover the exact entry spot from HF-02's contemporaneous `spot` field while keeping option legs single-source. The five 2026 cycles remain explicitly unresolved rather than using daily-close proxies.


## E20-005 — 2026-09-30
- **Issue:** HF-02 final-bar extraction passed timestamp bounds to Polars `is_between` as expressions instead of literals.
- **Impact:** Recovery stopped after source loading and strike-selection, before writing recovered bars.
- **Correction:** Wrap the entry/expiry bounds with `pl.lit(...)`. No source, timestamp, strike-selection, or admission rule changes.


## E20-006 — 2026-09-30
- **Issue:** The restored Phase-9 calendar contains 100 weekly expiries, while the frozen Phase-17 experiment used exactly the first 63 chronological `USABLE_OHLC` cycles.
- **Impact:** Phase-20 initially classified 64 extra expiries as missing and generated 14,336 (64×224) out-of-scope rows.
- **Correction:** Restrict Phase-20 to the exact frozen 63-cycle universe (`sort(target_expiry).head(63)`) before calculating missing cycles. No strategy rule or gate changes.

## E20-007 — 2026-09-30
- **Issue:** Recovery persistence attempted rebase after committing while an intentionally excluded parquet artifact remained unstaged.
- **Impact:** The computation succeeded but repository persistence failed.
- **Correction:** Use `git pull --rebase --autostash` after committing, then push. The recovery artifact remains available through the workflow artifact and the compact manifest is committed to the branch.


## E20-006 — 2026-09-30
- **Issue:** The Phase-9 calendar restored from the artifact contains 100 weekly expiries, while the frozen Phase-17/19 experiment explicitly used the first 63 cycles.
- **Impact:** Phase-20 diagnostic initially treated 64 cycles as missing instead of the frozen 27-cycle gap.
- **Correction:** Restrict recovery to the exact frozen 63-cycle manifest (`expiry_start=0`, `expiry_end=63`). No additional cycles will enter the research sample.
