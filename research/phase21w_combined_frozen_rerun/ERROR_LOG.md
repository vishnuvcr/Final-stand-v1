# Phase 21W Error Log

## E21-001 — 2026-09-30
- **Issue:** HF-02 recovered cycle manifest lacks Phase-9 `prior_expiry` and `status` columns required by the frozen backtester interface.
- **Impact:** Combined-input construction stopped before backtesting.
- **Correction:** Join those fields from the frozen 63-cycle Phase-9 calendar by `target_expiry`. No strategy/data values changed.
