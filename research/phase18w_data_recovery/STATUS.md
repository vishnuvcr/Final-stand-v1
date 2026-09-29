# Phase 18W Status — Exhaustive Data Recovery

**Status:** COMPLETED — recovered-data coverage gate passed to Phase 19W with documented partial cells.

## Recovery result
- Source: Hugging Face `thetrademarkk/india-index-options-1m`
- Frozen dataset revision: `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`
- Target weekly cycles: **63**
- Registered variants: **224**
- Variant-cycle cells tested: **14,112**
- Valid variant-cycle cells: **13,956 (98.89%)**
- Fully covered cycles: **58/63**
- Partially covered cycles: **5/63**
- Minimum cycle-level coverage: **182/224 (81.25%)**
- Control configuration (OTM1 + NEXT1 + M=2.0): **valid on 63/63 cycles**
- No synthetic bars, interpolation, or source blending were used.

## Partial-coverage cycles
- 2024-08-22: 182/224
- 2025-05-15: 189/224
- 2025-06-12: 189/224
- 2025-09-09: 196/224
- 2026-03-17: 208/224

The partial cells are carried forward explicitly. Phase 19W must calculate per-variant valid-cycle counts and apply the preregistered all-63 validity gate; it must not silently treat partial cycles as valid.

## Reproducibility
- Recovery script: `research/phase18w_data_recovery/recover_hf03.py`
- Coverage report: `research/phase18w_data_recovery/output/hf03_variant_coverage.json`
- Control cross-check: `research/phase18w_data_recovery/output/hf03_control_crosscheck.csv`
- Successful recovery workflow run: **36635955194**
- Coverage artifact SHA-256: `a1f7265bd26f4c4f5981f7989da7a603ddb7603e7a11d497c4a0a2ab5be436ac`

## Decision
Phase 18W is closed as a **data-recovery success with documented partial contract coverage**, not as a reason to stop the research. Phase 19W is authorized to execute the frozen empirical rerun using the exact HF-03 revision above.
