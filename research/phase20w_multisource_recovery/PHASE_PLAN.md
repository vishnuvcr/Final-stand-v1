# Phase 20W — Multi-Source Contract Recovery

## Purpose
Recover the 27 target weekly cycles that remain absent from the Phase 19 strategy-level executable set, using independent public sources without changing the frozen strategy.

## Research questions
1. Are the 27 missing target cycles present in an independent 1-minute weekly-expiry archive?
2. Do the alternate bars contain exact 10:00 IST entry and 14:00 IST lock observations for every required strike?
3. Can recovered contracts be mapped without synthetic prices or look-ahead leakage?
4. Does deterministic source precedence materially increase the 63-cycle executable coverage?
5. If coverage becomes sufficient, does the unchanged 224-variant experiment remain directionally consistent?

## Registered sources
- Primary: HF-03 `thetrademarkk/india-index-options-1m`, pinned revision `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`.
- Recovery-1: HF public `johnwick3690/stocks`, pinned commit `f90f7ac`, explicit weekly-expiry parquet archive.
- Recovery-2: HF-02 `artist-23/nifty-options-data`, pinned revision `45e0a043f34f3f40f9694e52a944297803c2af8b`.
- Recovery-3: HF-01 `rissin/nse-options-intraday`, pinned revision `8f7739cab3f38abdcbc6332a6d0a83e1341326e3`.
- Broker/official routes remain registered for later use if public sources cannot recover sufficient observations.

## Frozen protocol
- 224 variants unchanged.
- 63-cycle calendar unchanged.
- 37/12/14 chronological split unchanged.
- 10:00 IST entry, 14:00 IST lock.
- 50 NIFTY-point stop.
- 0.50 NIFTY-point slippage per leg.
- Existing Paytm Money/NSE transaction-cost model.
- Holdout remains locked for selection.
- No source blending at the same observation unless exact duplicate values agree; conflicts are logged and excluded from synthetic reconstruction.

## Deterministic precedence
1. HF-03 for observations already admitted in Phase 19.
2. Recovery-1 only for missing observations/contracts.
3. Recovery-2 only if Recovery-1 is unavailable/incomplete.
4. Recovery-3 only as the next public fallback.
A source may fill a missing observation, but it may not overwrite a primary observation.

## Steps
1. Freeze source revisions and target missing-cycle list.
2. Inventory exact weekly-expiry files in Recovery-1.
3. Download/cache only target files and validate schema/timestamps/expiry/strike/side.
4. Measure contract-level coverage at entry and lock for all 224 variants.
5. Cross-check duplicate observations against HF-03 where overlap exists.
6. Add deterministic fallback bars only where primary data are absent.
7. Produce a recovered option-bar interface and provenance manifest.
8. Re-run the unchanged Phase-19 backtest if coverage improves materially.
9. Reapply the original promotion gate unchanged.
10. Close only after registered public sources are exhausted or demonstrably insufficient.

## Exit criteria
- Exact source hashes recorded.
- Missing-cycle coverage matrix complete.
- Duplicate/conflict audit complete.
- No synthetic bars.
- Coverage improvement quantified.
- If >=50/63 valid cycles become available, rerun the frozen 224-variant family.
- If coverage remains below the frozen gate, document the remaining missing contracts and proceed only to execution-data validation for the covered set.
