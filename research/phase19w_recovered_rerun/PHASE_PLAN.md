# Phase 19W — Recovered-Data Empirical Rerun

## Purpose
Re-run the pre-registered Phase 17W 224-configuration experiment after Phase 18W data recovery, using the recovered historical data without changing the strategy family, chronology, costs, slippage, stop, or promotion gate.

## Entry condition
This phase must not be evaluated until Phase 18W has:
1. completed the registered recovery workflow(s);
2. produced a machine-readable source-by-cycle-by-contract coverage record;
3. recorded all recovery errors and source exclusions;
4. established deterministic provenance and duplicate/conflict checks.

## Frozen protocol
- 224 configurations: 8 K1 × 4 K2 × 7 K3 multipliers.
- Fixed 63-cycle calendar and 37/12/14 chronology.
- Entry 10:00 IST; lock 14:00 IST.
- 50-point hard stop.
- 0.50 NIFTY points slippage per leg.
- Existing Paytm Money/NSE transaction-cost model.
- Same lot-size rules.
- OHLC reconstruction only unless separately labelled execution-validation analysis is available.
- Untouched holdout remains descriptive and locked from selection.

## Research questions
1. How much of the Phase 17 data-availability deficit is removed by the recovered source set?
2. Does the unchanged 224-variant family achieve the original coverage gate when the recovered data are used?
3. Does the original promotion gate change its disposition under improved coverage?
4. Are any differences attributable to data recovery/provenance rather than strategy-parameter changes?
5. Are recovered control results internally reproducible against the original Phase 17 control where both sources overlap?

## Methods
- Build a source-by-cycle-by-strike coverage matrix.
- Validate timestamps, expiry identity, strike identity, option side, OHLC consistency, OI/volume fields, duplicates and conflicting records.
- Use deterministic source precedence declared by Phase 18; do not silently blend conflicting bars.
- Reconstruct all 224 variants with the existing Phase 17 engine.
- Run the same training/validation/holdout split.
- Compute the same metrics and centered moving-block bootstrap.
- Apply Holm correction across all 224 training p-values.
- Apply the unchanged preregistered promotion gate exactly once.

## Non-negotiable leakage controls
- No parameter additions after recovered results are observed.
- No holdout-based selection.
- No changing the 50-point stop or 0.50-point slippage after looking at recovered results.
- No changing the 63-cycle chronology.
- No source blending that creates synthetic bars.

## Exit criteria
Close this phase after:
1. all 224 variants are evaluated or a documented coverage limitation prevents a complete rerun;
2. deterministic data-quality checks pass;
3. recovered-vs-original control comparison is reported;
4. promotion gate is applied without holdout leakage;
5. results, implications, strengths, limitations and next phase are documented.

## Downstream rule
Only variants that satisfy the unchanged Phase 17 promotion gate may proceed to a separate capital/margin phase. Otherwise, retain the historical control and do not open another strike-search loop.
