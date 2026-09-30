# Phase 22B Error Log

## E22B-001 — Execution-aware data still unavailable
- The available public NIFTY source provides OHLCV(+OI), not historical bid/ask/depth.
- Correction: Phase 22B labels the result as OHLC validation and retains execution-aware validation as a separate gate.

## E22B-002 — Short new-period sample
- The public archive currently reaches 2026-08-04, yielding only a limited number of weekly expiries after the Phase-21 sample.
- Impact: the new period cannot satisfy the existing 30-cycle capital-promotion minimum.
- Correction: evaluate the full frozen 504-family anyway for prospective evidence, but do not promote capital from this phase.

## E22B-003 — Push-triggered workflow inputs were empty
- Observed: GitHub Actions exposes `inputs.*` only for workflow_dispatch. The controlled push run therefore passed empty environment variables.
- Impact: the run stopped before data acquisition with an integer-conversion error.
- Correction: workflow environment variables now use explicit defaults when dispatch inputs are absent. The manual workflow_dispatch interface remains available.

## E22B-004 — TradeMarkk post-Phase-21 NIFTY file coverage was insufficient
- Observed: the source-catalog discovery over 2026-05-19..2026-08-04 admitted only one weekly expiry from TradeMarkk's NIFTY expiry-file tree.
- Impact: it could not provide a meaningful new weekly validation window.
- Correction: the prospective phase switched acquisition to RISSIN's current 2026 NIFTY 1-minute archive, which documents year-level intraday coverage and expiry/strike/CE/PE/OHLC/volume fields. The 504 family and trading protocol were not changed.

## E22B-005 — Source gaps must not redefine the trading calendar
- Observed: RISSIN contains only 7 of the weekly expiries in the requested post-Phase-21 window.
- Risk: deriving the prior expiry from available source files would incorrectly move entry dates backward whenever an expiry file is missing.
- Correction: the prospective builder now derives the prior weekly expiry from the frozen Tuesday weekly calendar relation (target expiry minus 7 days) for this period. Missing source files cause a missing cycle, not a calendar shift.

## E22B-006 — RISSIN timestamp timezone mismatch in lazy filtering
- Observed: the annual RISSIN file reports timestamps with a +05:30 timezone representation that Polars would not directly compare with an Asia/Kolkata literal inside the lazy scan.
- Impact: prospective data extraction stopped before cycle construction.
- Correction: the annual file is now date-filtered using its canonical date field before collection; timestamps are normalized only after materialization.

## E22B-007 — Polars nested timezone literals in coverage check
- Observed: using `Expr.is_in([timezone-literal, timezone-literal])` produced a nested-object construction error.
- Impact: the run stopped after loading the weekly option data, before completing cycle admission.
- Correction: the exact entry/lock coverage check now uses two explicit equality predicates joined with OR.

## E22B-008 — Spot coverage gap
- The TradeMarkk NIFTY minute index source lacked an exact 10:00 IST spot row for a later prospective week.
- K1 selection cannot proceed without an underlying spot observation.
- Correction: the prospective run now uses a separately pinned NIFTY minute spot archive; option legs remain exclusively sourced from RISSIN.

## E22B-009 — NIFTY minute spot schema uses date rather than timestamp
- The pinned spot archive contains `date, open, high, low, close, volume` without a separate symbol or timestamp column.
- Correction: the adapter treats the `date` field as the minute timestamp and applies the existing IST normalization. The file itself is pinned by revision and SHA-256.

## E22B-010 — NIFTY minute spot timestamps are strings
- The spot archive stores minute timestamps as strings such as `2026-05-15 10:39:00`.
- Correction: the adapter now parses string timestamps explicitly in IST before exact 10:00 selection.

## E22B-011 — Exact 10:00 spot timestamp unavailable
- A prospective week had no exact 10:00 IST underlying observation in the pinned minute archive.
- Correction: the entry-strike spot rule now uses the latest observation at or before 10:00 within a fixed five-minute causal window. No future observation is used, and the rule is frozen before rerun.


## E22B-012 — Primary spot archive gap on 2026-07-08
- Observed: the pinned independent NIFTY minute archive has no causal observation within five minutes before the frozen 10:00 IST entry for the 2026-07-14 target expiry.
- Impact: the prospective builder aborted before any 504-family results were generated.
- Correction: added a separately pinned public NIFTY 1-minute archive as a **gap-only causal fallback**. It is consulted only when the primary archive lacks the required observation; the same ≤5-minute causal rule is retained. Fallback source: `technovusin/nifty50-historical-data`, revision `cd169a991ccfc8979e718ae5ebeb1891a788107d`.
- No option source, strike rule, weekly protocol, stop, slippage, cost model, or holdout boundary was changed.


## E22B-013 — Null Holm column in summary coverage check
- Observed: the full prospective data/backtest computation completed, but the workflow failed while evaluating `summary["holm_adjusted_p"] < 0.05` because Polars inferred the column as Null when no adjusted p-values were populated.
- Impact: this was a reporting/serialization failure after the 504-family computation; no trades or strategy parameters were altered.
- Correction: the coverage check now explicitly casts `holm_adjusted_p` to Float64 with null-safe handling before counting significant adjusted p-values.
- Research interpretation: null adjusted p-values remain null; they are not converted into significant results. The next run will determine whether the holdout produced enough observations per variant for the pre-specified bootstrap test.


## E22B-014 — Validator missing pandas dependency
- Observed: the full 504-family computation completed successfully, producing 7 admitted weekly expiries, 3,528/3,528 expected usable variant-cycle rows, and all 504 variants. The subsequent validation step failed with `ModuleNotFoundError: No module named 'pandas'`.
- Impact: validation/publish/artifact steps were skipped; this was a workflow dependency failure, not a research-computation failure.
- Correction: add `pandas` to the workflow's installed Python dependencies. No research data, variant definition, weekly protocol, or statistical rule is changed.


## E22B-015 — Validator used obsolete registry field
- Observed: the producer writes `weekly_expiries`, but the validator attempted to read obsolete key `selected_weekly_expiries`, causing `KeyError` after the complete 504-family computation.
- Impact: validation/publish/artifact steps were skipped; the research computation itself completed successfully.
- Correction: validator now reads the producer's canonical `weekly_expiries` field. The pre-specified minimum of 8 weekly expiries remains unchanged.


## E22B-016 — RISSIN weekly expiry coverage insufficient for the frozen 8-expiry gate
- Observed: corrected validation showed only 7 weekly expiries from RISSIN in 2026-05-19..2026-08-04, while the frozen validation requires at least 8.
- External source review found the current TradeMarkk Hugging Face NIFTY 1-minute options dataset has per-expiry Parquet files and currently advertises coverage through 2026-08-04. citeturn1search0turn0search2
- Correction: add TradeMarkk as a **gap-only option-data fallback** for expiry files absent from RISSIN. RISSIN remains primary; no strategy, strike grid, entry/lock times, causal spot rule, cost model, or 8-expiry validation threshold is changed.
