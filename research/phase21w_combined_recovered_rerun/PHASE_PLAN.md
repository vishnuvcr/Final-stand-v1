# Phase 21W — Combined Recovered Frozen Rerun

## Research question
Does the weekly strategy remain capable of passing the frozen 224-variant promotion gate after restoring the missing executable cycles from an independent source, while keeping source provenance and execution rules fixed?

## Source precedence
1. HF-03 pinned `0f4800e43e6f96cec0794369d78eb4d3c4211ef5` for cycles already executable in Phase 19.
2. HF-02 pinned `45e0a043f34f3f40f9694e52a944297803c2af8b` only for previously missing cycles and only for variant-cycles explicitly marked `USABLE_OHLC`.
3. No cross-source mixing inside a variant-cycle.
4. Missing cells remain missing.

## Frozen controls
224 variants; 63 expiry chronology; 37 training / 12 validation / 14 holdout; 10:00 IST entry; 14:00 IST lock; 50 NIFTY-point stop; 0.50-point slippage per leg; existing Paytm Money/NSE cost model; centered block bootstrap with block length 3 and 3000 reps; Holm correction across 224 tests; unchanged promotion gate.

## Method
- Rebuild the Phase-19 HF-03 input from the pinned source using the frozen baseline manifest.
- Merge only the Phase-20 HF-02 recovered variant cycles/bars for cycles absent from the HF-03 build.
- Verify one-row-per-(variant, expiry, source) and no duplicate timestamp/strike bars.
- Run the exact Phase-17/19 backtester through `strike_alternatives.py --built-input-dir`.
- Persist repository-safe summaries/manifests and full parquet outputs as workflow artifacts.
- Independently verify cycle coverage, trade counts, costs, bootstrap p-values, Holm adjustment, and promotion gate.
## Exit criteria
- Combined cycle manifest covers all 63 chronology entries, with status/provenance recorded.
- Combined option bars pass duplicate/time/strike checks.
- All 224 variants evaluated.
- Gate and holdout results recorded.
- Phase conclusion and limitations written.
