# Phase 19W Status

**State:** COMPLETE — frozen empirical rerun executed and persisted.

## Execution
- 224/224 variants completed.
- Frozen chronology: 63 cycles; 37 training / 12 validation / 14 holdout.
- Run: GitHub Actions `36642638097` (successful).
- Full derived output retained as workflow artifact `11067705095`.
- Repository-safe summaries and 224 trade files persisted on branch `phase-19w-recovered-rerun`.

## Results
- Promotable variants: **0/224**.
- All variants produced 36/63 usable executable trade cycles (57.14%).
- Therefore every variant failed the frozen minimum coverage requirement of 50/63 and also failed the minimum training/validation sample-size gates.
- 193/224 variants had positive training mean net rupees; 136/224 had positive validation mean; 180/224 had positive holdout mean.
- None had Holm-adjusted training p < 0.05; minimum adjusted p = 0.07464178607130957.
- The positive-return observations are therefore **not admitted to capital testing** under the frozen gate.

## Data-coverage interpretation
Phase 18W's 98.895% figure measured variant-cycle definition/contract-cell coverage (13,956/14,112 cells; 59 fully covered cycles and 4 partial). Phase 19W's stricter executable-bar path requires exact entry/lock marks and a usable expiry settlement spot; that yielded only 36/63 completed trades per variant. This discrepancy is now a research finding, not a reason to silently relax the gate.

## Phase conclusion
Phase 19W establishes the frozen empirical result but does **not** close the overall weekly-strategy research. The next phase is executable-bar recovery from independent sources, with deterministic precedence, provenance, timestamp/strike/side/OHLC validation, and no synthetic bars.

## Frozen controls
Entry 10:00 IST; lock 14:00 IST; 50-point stop; 0.50-point slippage per leg; existing Paytm Money/NSE transaction-cost model; centered block bootstrap (block length 3, 3000 reps); Holm correction across 224 tests; unchanged promotion gate.