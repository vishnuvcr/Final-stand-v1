# Phase 18W Admission Record for Phase 19W

**Admission status:** AUTHORIZED

Phase 18W recovered the frozen 63-cycle weekly universe from Hugging Face dataset `thetrademarkk/india-index-options-1m`, revision `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`.

- 63 target cycles
- 224 preregistered variants
- 14,112 possible variant-cycle cells
- 13,956 valid cells (98.89%)
- 58 cycles fully covered
- 5 cycles partially covered
- Control OTM1 + NEXT1 + M=2.0 valid on 63/63 cycles
- Recovery workflow: 36635955194
- Coverage artifact digest: `sha256:a1f7265bd26f4c4f5981f7989da7a603ddb7603e7a11d497c4a0a2ab5be436ac`

## Phase 19 requirements
1. Use the exact HF revision above.
2. Preserve the frozen 224-variant registry and original strategy mechanics.
3. Preserve 37/12/14 chronological train/validation/holdout split.
4. Preserve 50-point hard stop, 0.50-point slippage per leg, Paytm Money/NSE cost model, bootstrap, Holm adjustment, and promotion gate.
5. Do not synthesize missing bars or silently drop partial cycles from the validity accounting.
6. Report per-variant valid-cycle counts and identify any variant failing the all-63 validity threshold.
7. Do not use holdout observations for variant selection or parameter tuning.
