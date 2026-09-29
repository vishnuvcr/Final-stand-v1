# Phase 17W — K1/K2 Strike-Selection Alternatives

## Purpose
Test a finite, preregistered family of alternative methods for choosing K1 and K2 in the weekly NIFTY call-ladder strategy, while preserving all prior Phase 13W evidence and keeping the untouched holdout out of parameter selection.

This phase is a strategy-definition validation phase. It does not overwrite the frozen Phase 13W strategy or its holdout.

## Trigger for this phase
The current frozen implementation defines:
- K1 = first listed call strike strictly above spot.
- K2 = next listed call strike above K1.

Changing K1 or K2 changes D, K3, entry cash flow, margin path and tail exposure, so alternatives are tested as a separate preregistered family.

## Research questions
1. How sensitive are weekly results to the definition of K1?
2. How sensitive are results to the spacing/rule used for K2 conditional on K1?
3. Do alternative K1/K2 rules materially change trade eligibility, target error, payoff shape, costs and drawdowns?
4. Which alternative rules remain viable on training and validation data without using the untouched holdout for selection?
5. Does the current K1/K2 definition remain within the empirical family rather than being an implicit assumption?

## Fixed components
The following remain frozen for every variant:
- weekly expiry framework and historical expiry calendar;
- 10:00 IST entry decision timestamp;
- 14:00 IST pre-expiry lock timestamp;
- call-only ladder;
- K3 = listed strike above K2 whose entry premium is closest to 2*(P1-P2);
- D <= 0 => no trade;
- 50-point hard stop;
- 0.50 NIFTY-point slippage per leg;
- Paytm Money/cost model from Phase 11W;
- one trade cycle per weekly expiry;
- same OHLC reconstruction and no BBO substitution;
- no change to lot-size rules;
- no capital/margin tuning in this phase.

## K1 alternatives
Eight deterministic definitions are preregistered:
- OTM1: first listed strike strictly above spot.
- OTM2: second listed strike above spot.
- OTM3: third listed strike above spot.
- ATM_NEAREST: listed strike minimizing absolute distance to spot; tie goes to the higher strike.
- ATM_UP: first listed strike at or above spot.
- ITM1: highest listed strike strictly below spot.
- ITM2: second-highest listed strike below spot.
- ITM3: third-highest listed strike below spot.

## K2 alternatives
Four deterministic definitions are preregistered, always requiring K2 > K1:
- NEXT1: first listed strike above K1.
- NEXT2: second listed strike above K1.
- NEXT3: third listed strike above K1.
- MIRROR_GAP: strike above K1 whose distance from K1 is closest to the absolute spot-to-K1 distance; ties go to the lower strike.

This creates 8 x 4 = 32 registered K1/K2 configurations.

## Baseline control
OTM1 + NEXT1 is the current Phase 13W definition and is a control. Previous Phase 12/13 results are not recalculated or replaced by this phase.

## Data and execution
For each expiry, the workflow downloads the same Hugging Face NIFTY option/index data through the existing cached ingestion route. The variant builder reads the full call chain at entry, selects K1/K2 according to the registered rule, recomputes K3 from the frozen premium-difference rule, then creates variant-specific option paths used by the existing Phase 11W backtest engine.

No bid/ask observations are invented.

## Chronological evaluation
Use the same 63-cycle chronology as the Phase 13W study:
- training: first 60% of the baseline usable weekly cycles;
- validation: next 20%;
- untouched holdout: final 20%.

The calendar partitions are fixed by the baseline eligible expiry list, not recomputed by variant, so a variant cannot move a difficult week into or out of the holdout by changing its eligibility.

## Selection rule
The holdout is descriptive only.

A variant is marked PROMOTABLE_TO_CAPITAL_PHASE only if, using training/validation data:
1. it has at least 50 valid cycles out of the 63-cycle calendar;
2. training mean net P&L > 0;
3. validation mean net P&L > 0;
4. training block-bootstrap one-sided p-value is significant after Holm correction across the 32 registered variants.

This is a preregistered gate, not a ranking. No holdout statistic is used in that gate.

## Statistical analysis
For each variant report:
- usable cycle count;
- missing/ineligible cycle count;
- training, validation and holdout n;
- mean/median net P&L;
- win rate;
- maximum drawdown;
- annualized weekly Sharpe;
- expected shortfall;
- total transaction costs;
- target error distribution;
- K1/K2 distance from spot;
- D distribution;
- lock and stop frequencies.

For training:
- moving-block bootstrap of mean net P&L;
- one-sided p-value for mean <= 0 under a centered bootstrap null;
- Holm correction across all 32 p-values.

Holdout outputs are reported for auditability but are never used to choose or promote a variant.

## Multiple-comparison control
All 32 variants are tested in one registered family. The family-level decision uses Holm adjustment across the 32 training p-values.

No hidden sub-selection of variants is allowed after results are observed.

## Stopping rule
Stop this phase after:
1. all 32 registered configurations are evaluated;
2. data-quality and deterministic tests pass;
3. training/validation/holdout reports are generated;
4. the promotion gate is applied without holdout leakage;
5. the strategy-definition implications are documented.

Do not expand the K1/K2 search space after observing results.

## Downstream rule
If one or more variants pass the preregistered promotion gate, Phase 16W capital/margin validation can be resumed for those predeclared variants in a separate phase. The original frozen Phase 13W variant remains the historical control and is never erased.

If no variant passes, retain the frozen control as the documented definition and close the alternatives experiment without further tuning.
