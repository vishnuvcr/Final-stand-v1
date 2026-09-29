# Phase 19W Status

**State:** EXECUTING — recovered-data empirical rerun admitted.

**Execution status:** 224 variants / frozen 63-cycle chronology submitted to GitHub Actions.

**Recovered data:** HF-03 pinned revision `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`; 13,956/14,112 variant-cycle cells available (98.895%); 59 fully covered cycles and 4 partial cycles.

**Frozen inputs:** 224 registered configurations, 63-cycle calendar, 37/12/14 chronology, 50-point stop, 0.50-point slippage per leg, Paytm Money/NSE cost model, holdout locked.

**Statistical plan:** centered block bootstrap (block length 3, 3000 reps), Holm adjustment across 224 training p-values, unchanged promotion gate.

**Missing-data rule:** unavailable contract observations are omitted as missing; no synthetic bars or source blending is introduced in this frozen rerun.

**Next:** complete all 224 empirical backtests, inspect outputs, validate controls, apply promotion gate, then close the phase with manuscript-ready results and limitations.


**Execution trigger correction:** A normal repository commit is being used to trigger the admitted workflow after workflow-file-only push events produced no jobs.


**Workflow activation:** Phase 19 workflow is now installed on the default branch; execution is being triggered from this research branch.
