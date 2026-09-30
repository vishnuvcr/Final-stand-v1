# Phase 22W — Prospective Configuration Registry

## Frozen before the new holdout

The Phase 22 primary analysis will **not select a single Phase 21W winner**. The complete 224-configuration family is carried forward as the preregistered candidate family:

- K1: OTM1, OTM2, OTM3, ATM_NEAREST, ATM_UP, ITM1, ITM2, ITM3
- K2: NEXT1, NEXT2, NEXT3, MIRROR_GAP
- K3: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0

Total: **224 configurations**.

## Rationale

Phase 21W showed a descriptive K3/ITM/NEXT surface, but using the Phase 21W holdout to select one winner would contaminate the next holdout. Carrying the complete family forward preserves the ability to test the hypothesis without post-hoc winner selection.

## Frozen strategy rules

- Entry: 10:00 IST.
- Lock/exit: 14:00 IST.
- Hard stop: 50 NIFTY points.
- Slippage baseline: 0.50 NIFTY points per leg.
- Paytm Money/NSE transaction-cost model remains the registered baseline.
- No strategy rule may be changed after the new holdout is opened.

## Statistical family

The 224 configurations form one multiplicity family. The primary inferential screen will use the preregistered bootstrap procedure and Holm correction across all 224 configurations.

## Phase 22 distinction

The primary improvement is **execution evidence**, not a new parameter search. The experiment asks whether the Phase 21W configuration surface survives with executable quote prices and realistic liquidity constraints.
