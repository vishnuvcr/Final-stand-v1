# Phase 22B Status

State: **ACTIVE — multi-source recovery rerun**

## Freeze gate
- 504-configuration family frozen: ✅
- Weekly protocol frozen: ✅
- New-period holdout opened only after freeze: ✅
- Post-hoc configuration selection: ❌ prohibited

## Data and source gate
- Primary option source: RISSIN NIFTY 1-minute archive: ✅
- Primary spot source: pinned independent NIFTY minute archive: ✅
- Gap-only causal spot fallback: ✅
- Gap-only option fallback: TradeMarkk Hugging Face expiry files: 🔄
- Historical bid/ask/depth: unavailable at this validation layer
- Execution-aware evidence: separate downstream gate

## Validation state
- Full 504-family computation completed successfully on prior corrected runs: ✅
- Latest completed computation admitted 7 weekly expiries, 3,528/3,528 expected variant-cycle rows, and all 504 variants.
- E22B-014 and E22B-015 were workflow-only validator defects and are corrected.
- The frozen >=8 weekly-expiry validation threshold remains unchanged.
- Multi-source recovery is now attempting to recover missing weekly expiry files rather than weakening the threshold.
- Statistical inference and publication remain pending successful validation.

## Promotion boundary
This is an external prospective validation layer. Even after recovery, it remains subject to the existing 30-cycle capital-promotion minimum and the separate execution-aware gate. No capital deployment conclusion is drawn from the current short OHLC-only sample.

## Latest execution state
- E22B-014: validator lacked pandas — corrected.
- E22B-015: validator used obsolete registry key — corrected.
- E22B-016: RISSIN supplied only 7 weekly expiries for the current window — gap-only TradeMarkk recovery added.
- No strategy parameter, holdout boundary, entry/lock timestamp, causal spot rule, stop-loss, slippage/cost model, or 504-family definition was changed.
