# Phase 21W Research Log

## 2026-09-30 — Resume after E21-012 optimization run
- Re-read the phase plan, status, error log, workflow definition, prior workflow runs and the frozen Phase-17/19 interface before modifying the current phase.
- Latest workflow run 36706822914 completed in about 85 seconds and failed only at the deterministic combined-input build; HF-03 artifact retrieval and dependency installation succeeded.
- Exact failure: `Unmapped HF2 schema columns: ['entry_timestamp', 'lock_timestamp', 'k3_multiplier']`.
- Inspection of the frozen Phase-17 build logic confirmed these are repeated metadata fields in the variant-bar interface. The Phase-20 HF-02 bars carry the contract/variant identifiers but omit these repeated fields.
- Correction: map `entry_timestamp` and `lock_timestamp` from the compact recovered-cycle manifest by `target_expiry`; extract `k3_multiplier` from the registered variant id. Null reconstructed metadata is rejected.
- No prices, source timestamps, strike-selection rules, chronology, stop, slippage, transaction-cost assumptions, bootstrap settings or promotion gate changed.
- The memory optimization from E21-012 is retained: no large bar-to-metadata join and duplicate validation is source-local.
