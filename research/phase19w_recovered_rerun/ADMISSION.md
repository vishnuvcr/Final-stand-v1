# Phase 18W Data Admission for Phase 19W

**Admission state:** ADMITTED FOR FROZEN EMPIRICAL RERUN

**Source:** Hugging Face `thetrademarkk/india-index-options-1m`
**Pinned revision:** `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`
**Recovery run:** `36635955194`
**Coverage report:** `research/phase18w_data_recovery/output/hf03_variant_coverage.json`

## Coverage
- Target weekly expiry cycles: 63
- Registered variants: 224
- Expected variant-cycle cells: 14,112
- Valid variant-cycle cells: 13,956
- Coverage: 98.895%
- Fully covered cycles: 59/63
- Partially covered cycles: 4/63
- Missing cells: 156

Partial cycles are retained as partial observations. Missing contracts are **not** imputed, synthesized, or backfilled from another source in this rerun.

## Frozen rerun controls
- Entry: 10:00 IST
- Lock: 14:00 IST
- Stop: 50 NIFTY points
- Slippage: 0.50 NIFTY points per leg
- Cost model: existing Paytm Money/NSE model
- Chronology: 37 training / 12 validation / 14 holdout
- Variant family: 8 K1 × 4 K2 × 7 K3 multipliers = 224
- Statistical procedure: centered block bootstrap (3-bar blocks, 3000 reps) with Holm adjustment across the 224 training p-values
- Promotion gate remains unchanged.

Phase 19W may now execute. Coverage limitations must remain visible in its results and final manuscript.
