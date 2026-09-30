# Phase 21W Error Log

## E21-001 — 2026-09-30
- **Issue:** HF-02 recovered cycle manifest lacks Phase-9 `prior_expiry` and `status` columns required by the frozen backtester interface.
- **Impact:** Combined-input construction stopped before backtesting.
- **Correction:** Join those fields from the frozen 63-cycle Phase-9 calendar by `target_expiry`. No strategy/data values changed.

## E21-002 — 2026-09-30
- **Issue:** HF-02 recovered bars use `oi` while the HF-03 frozen bar interface uses `open_interest`.
- **Impact:** Combined-input construction stopped before coverage validation.
- **Correction:** Rename `oi` to the frozen interface field `open_interest` at the adapter boundary; values are unchanged.

## E21-003 — 2026-09-30
- **Issue:** The third Phase-21 run was cancelled during a redundant HF-03 interface rebuild.
- **Impact:** No empirical result was produced.
- **Correction:** Phase 21 will use the already-persisted Phase-19 HF-03 interface/results as its primary source and the admitted Phase-20 HF-02 recovery overlay, avoiding unnecessary redownload/rebuild. The frozen 63-cycle calendar and strategy parameters remain unchanged.

## E21-004 — 2026-09-30
- **Issue:** Phase-19 persisted outputs do not include the intermediate `variant_option_bars.parquet` required for exact re-execution.
- **Impact:** A direct persisted-input overlay cannot reproduce the original OHLC backtest interface.
- **Correction:** Rebuild the frozen HF-03 interface once from its pinned revision, then overlay admitted HF-02 cycles. The rebuild is data-interface reconstruction, not parameter retuning.

## E21-005 — 2026-09-30
- **Issue:** HF-02 recovered bars lack the derived `trading_day` field required by the HF-03 interface.
- **Impact:** Overlay construction stopped before coverage validation.
- **Correction:** Derive `trading_day` from the recovered bar timestamp at the adapter boundary; no timestamp or price values are modified.
