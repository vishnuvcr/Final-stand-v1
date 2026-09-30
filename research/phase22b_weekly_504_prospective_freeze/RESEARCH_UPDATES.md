# Phase 22B Research Updates

## 2026-09-30 — Prospective computation and validator recovery

- The full 504-variant prospective computation completed successfully.
- The admitted RISSIN-only window contained 7 weekly expiries and 3,528 expected/usable variant-cycle rows.
- E22B-014: validator dependency failure (pandas) corrected.
- E22B-015: validator schema mismatch corrected to use the producer's weekly_expiries field.
- E22B-016: because the frozen validation requires >=8 weekly expiries, the threshold was retained and a gap-only TradeMarkk option-source fallback was added.
- The primary RISSIN option source remains authoritative wherever available; fallback data are used only for missing expiry files.
- No strategy or statistical design parameters were changed.
- Current phase remains ACTIVE pending the multi-source recovery rerun.


## 2026-09-30 — Phase 22B validation completed

- End-to-end run 36759982136 completed successfully.
- 504/504 variants were present; 8 weekly expiries and 4,032/4,032 expected variant-cycle rows passed the coverage gate.
- 376/504 variants had positive total net P&L after the configured cost model.
- Every result row had n=6 completed trades, so the pre-specified >=8-observation bootstrap was not run and Holm-adjusted p-values remained null.
- The correct inference is descriptive prospective evidence only; no configuration is promoted and no capital-promotion conclusion is drawn.
- The next phase must add prospective weekly cycles rather than changing the frozen family or inference threshold.
