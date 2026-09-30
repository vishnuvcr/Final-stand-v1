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
