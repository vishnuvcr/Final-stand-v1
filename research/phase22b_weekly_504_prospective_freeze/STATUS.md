# Phase 22B Status

State: **VALIDATION COMPLETE — prospective statistical confirmation still pending additional weekly cycles**

## Freeze gate
- 504-configuration family frozen: ✅
- Weekly protocol frozen: ✅
- New-period holdout opened only after freeze: ✅
- Post-hoc configuration selection: ❌ prohibited

## Data and source gate
- Primary option source: RISSIN NIFTY 1-minute archive: ✅
- Primary spot source: pinned independent NIFTY minute archive: ✅
- Gap-only causal spot fallback: used: ✅
- TradeMarkk option fallback: available for eligible files; not used in this run: ⚠️
- Historical bid/ask/depth: unavailable at this validation layer
- Execution-aware evidence: separate downstream gate
- Requested prospective boundary: **2026-09-08**
- Actually admitted weekly expiries: **8**, ending **2026-07-21**
- Data-coverage ceiling is the limiting factor; extending the date input did not create additional admissible option expiries.

## Validation result — extension run
- Authoritative workflow run **36763880416**: SUCCESS
- Commit: **045a2da46307603fe7d0bdf04d12e74285545ee5**
- Frozen family size: **504**
- Expected variant-cycle rows: **4,032**
- Usable variant-cycle rows: **4,032**
- All 504 variants present: **yes**
- Variants with positive total net P&L: **376/504**
- Every variant has **n=6** completed trades.
- Bootstrap p-values: not computed because the pre-specified bootstrap requires at least 8 observations per variant.
- Holm-adjusted p-values: therefore not computed; none can be treated as <0.05.
- Capital-promotion gate: not reached; existing minimum is 30 completed cycles.
- No configuration is selected or promoted.

## Prospective expiry coverage
The run requested 2026-05-19 through 2026-09-08 but admitted only:
- 2026-05-19
- 2026-06-02
- 2026-06-09
- 2026-06-16
- 2026-06-23
- 2026-07-07
- 2026-07-14
- 2026-07-21

Monthly expiries excluded by the protocol included 2026-05-26, 2026-06-30, 2026-07-28 and 2026-08-04. The successful run's source manifest recorded no TradeMarkk option-fallback expiries. Independent public inspection of the TradeMarkk dataset shows its NIFTY option tree currently reaches 2026-08-04, while its dataset documentation explicitly notes partial option coverage. citeturn0search0turn0search1

## Interpretation boundary
The 376/504 positive count is descriptive only. It must not be interpreted as proof of robustness because the prospective sample remains six completed trades per variant and below the statistical and capital-promotion gates. The September 8 date extension was therefore a **data-coverage test**, not additional evidence.

## Errors/recovery
- E22B-014: validator dependency failure — corrected.
- E22B-015: validator registry-field mismatch — corrected.
- E22B-016: initial RISSIN-only expiry coverage below the frozen 8-expiry gate — multi-source discovery added; successful run admitted 8 expiries.
- E22B-017: n=6 per variant prevents the pre-specified bootstrap — remains a coverage limitation, not a strategy redesign.
- E22B-018: extending the prospective end date to 2026-09-08 did not increase admissible weekly option expiries; source coverage remains the bottleneck. No strategy parameters were changed.

## Next research boundary
Do not select a winner from the six-trade sample. Continue only through the pre-planned prospective-validation path when additional qualifying weekly option data become available. Before any further extension, search the approved external sources for additional qualifying NIFTY weekly option archives and record source coverage before rerunning.