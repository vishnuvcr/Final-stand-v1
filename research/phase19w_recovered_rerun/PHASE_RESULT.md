# Phase 19W — Recovered-Data Empirical Result

**Date:** 2026-09-30  
**Branch:** `phase-19w-recovered-rerun`  
**Authoritative workflow run:** 36642638097  
**Workflow conclusion:** success  
**Artifact:** `phase19w-recovered-results-issue-bridge` (358,825,217 bytes; SHA-256 `c7f774352e8ed74f64dfc4a200c7532cd41be63c1edbbce360df47764b7ecfa7`)

## Research question

Does the preregistered weekly NIFTY option strategy family remain viable when the Phase-17W strike-selection alternatives are rerun on the recovered historical dataset, using the original chronology, execution assumptions, transaction-cost model, and multiple-testing correction?

## Frozen experiment

- 224 configurations = 8 K1 × 4 K2 × 7 K3.
- K1: OTM1, OTM2, OTM3, ATM_NEAREST, ATM_UP, ITM1, ITM2, ITM3.
- K2: NEXT1, NEXT2, NEXT3, MIRROR_GAP.
- K3: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0.
- 63 frozen weekly expiry cycles.
- Chronology: 37 training / 12 validation / 14 holdout by the preregistered calendar; actual usable trade observations are lower when required contracts are unavailable.
- Entry 10:00 IST; lock 14:00 IST.
- Hard stop: 50 NIFTY points.
- Slippage: 0.50 NIFTY points per leg.
- Paytm Money/NSE transaction-cost model.
- Centered block bootstrap: block length 3, 3000 resamples.
- Holm correction across all 224 training p-values.
- No post-observation parameter expansion and no holdout selection.

## Data recovery

The rerun used the pinned HF-03 dataset revision `0f4800e43e6f96cec0794369d78eb4d3c4211ef5` and the exact frozen Phase-9 interface artifact for the 63-cycle calendar and NIFTY spot bars.

Recovered variant-cycle availability was 13,956 / 14,112 cells = **98.895%**. The strategy's usable trade observations were **36 / 63 cycles = 57.143%** for every variant. This is the binding evidence limitation for the frozen promotion gate.

## Results

All 224 registered variants completed computationally.

| Measure | Result |
|---|---:|
| Variants evaluated | 224 / 224 |
| Variants promoted | 0 |
| Variants with positive training mean | 193 |
| Variants with positive validation mean | 136 |
| Variants with positive holdout mean | 180 |
| Holm-adjusted training p < 0.05 | 0 |
| Holm-adjusted training p < 0.10 | 107 |
| Usable-cycle rate, min/max across variants | 57.143% / 57.143% |
| Training observations per variant | 21 |
| Validation observations per variant | 7 |
| Holdout observations per variant | 8 |

The frozen promotion gate requires, among other conditions, at least 50/63 valid cycles, at least 30 training observations, at least 8 validation observations, positive training and validation means, and Holm-adjusted training p < 0.05. Because every variant has only 36 usable cycles, 21 training observations, and 7 validation observations, **no configuration can satisfy the gate**. This is a coverage/eligibility result, not evidence that all 224 economic return profiles are negative.

Some configurations have positive validation and holdout means and some have low unadjusted/adjusted training p-values, but those observations are descriptive only under the preregistered gate. They must not be converted into a capital recommendation.

## Interpretation

The data-recovery effort succeeded in moving from the earlier 39/63 maximum-usable-cycle limitation to a much larger recovered dataset, and the full 224-configuration calculation now runs reproducibly. However, the recovered contract-level interface still leaves only 36 usable strategy cycles. The main unresolved scientific issue is therefore **contract-level completeness**, not computational feasibility.

The absence of promoted configurations should not be interpreted as proof that the strategy family has no predictive or economic signal. It means that the current evidence does not satisfy the predefined evidence threshold required for capital-phase promotion.

## Strengths

1. Full preregistered 224-configuration family was evaluated rather than selectively narrowing the search.
2. The original weekly chronology and holdout structure were preserved.
3. Slippage and transaction costs were included.
4. Multiple testing was controlled with one Holm family.
5. Data recovery used a pinned HF revision and preserved a reproducible artifact.
6. Large derived option-bar data are retained as a workflow artifact rather than silently discarded.

## Limitations

1. Only 36/63 cycles were usable at the strategy-trade level.
2. Training and validation sample sizes are therefore only 21 and 7 observations.
3. Historical OHLC reconstruction is not equivalent to historical executable bid/ask fills.
4. The recovered dataset is not yet sufficient for the capital-promotion gate.
5. Positive holdout rows within a broad 224-cell search are exploratory and should not be treated as independently validated discoveries.

## Phase decision

**Phase 19W is complete. No variant is promoted to capital execution.**

The appropriate next phase is targeted data-completeness and execution validation, not further parameter tuning. The next phase should seek to raise contract-level weekly coverage toward the preregistered 50/63 threshold using deterministic source precedence and, separately, validate executable bid/ask assumptions where historical quote data are available.

## Audit artifacts

- `variant_summary.json`
- `variant_registry.json`
- `variant_cycle_manifest.csv`
- `variant_option_bars.parquet` (workflow artifact)
- `ERROR_LOG.md`
- `STATUS.md`
