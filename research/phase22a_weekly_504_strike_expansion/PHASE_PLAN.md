# Phase 22A — Weekly 504-Configuration Strike-Range Expansion

## Status
ACTIVE — protocol frozen; full 504-configuration weekly backtest queued on the frozen 63-expiry Phase-21 data interface.

## Research question
When the strategy is treated explicitly as a weekly-horizon weekly-expiry trade, what happens when the K1 strike-selection range is extended from OTM/ITM 1–3 to OTM/ITM 1–8 while leaving K2, K3, entry/lock timing, stop, slippage and transaction-cost rules unchanged?

## Aim
Test the complete pre-registered 504-configuration family rather than selecting a single configuration from the earlier 224-configuration surface.

## Objectives
1. Preserve the weekly strategy mechanics already frozen in Phase 22.
2. Expand K1 to OTM1–OTM8 and ITM1–ITM8, retaining ATM_NEAREST and ATM_UP.
3. Test every combination with NEXT1/NEXT2/NEXT3/MIRROR_GAP and K3 = 0.5, 1, 1.5, 2, 2.5, 3, 4.
4. Use the complete 63-expiry Phase-21 recovery data as a retrospective parameter-expansion sample.
5. Keep the previously used 14-expiry holdout interpretation immutable; this phase must not relabel it as a new holdout.
6. Preserve Paytm Money/NSE costs, 0.50-point slippage per leg and 50-point hard stop.
7. Record all coverage failures for the deeper OTM/ITM rules.
8. Produce complete configuration-level results, parameter-surface summaries and reproducibility metadata.

## Frozen configuration family

| Dimension | Values | Count |
|---|---|---:|
| K1 | OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8 | 18 |
| K2 | NEXT1, NEXT2, NEXT3, MIRROR_GAP | 4 |
| K3 | 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0 | 7 |
| Total | | 504 |

No configuration will be added after results are inspected.

## Weekly trade protocol
- Trading horizon: weekly.
- Entry: 10:00 IST on the first trading day after the prior weekly expiry.
- Lock/exit decision: 14:00 IST on the trading day before the target weekly expiry.
- Remaining exposure may continue to target expiry unless the frozen stop/exit rules terminate it.
- Hard stop: 50 NIFTY points.
- Baseline slippage: 0.50 NIFTY points per leg.
- Paytm Money/NSE transaction-cost model: unchanged from the registered engine.

## Data boundary
The primary run uses the immutable Phase-21 recovery dataset revision already admitted for the 63-expiry experiment. This isolates the effect of widening K1 from the effect of changing the historical source.

This phase is a parameter-expansion study, not a fresh unseen-data claim. A future period after the Phase-21 sample remains the appropriate untouched external validation period.

## Statistical analysis
For every configuration:
- valid-cycle count and validity rate across 63 expiries;
- training/validation/holdout P&L under the existing chronological split, reported descriptively;
- win rate, drawdown, expected shortfall, Sharpe and mean cost;
- centered block-bootstrap training p-value;
- Holm correction across the full 504-configuration family.

The existing 224-family promotion result is not retroactively changed.

## Data-quality gates
- exact three-leg OHLC observations at frozen timestamps;
- no synthetic bars;
- no strike substitution;
- no cross-source leg mixing;
- no interpolation;
- complete provenance and SHA-256;
- explicit per-configuration coverage diagnostics.

## Exit criteria
Phase 22A is complete when:
1. all 504 configuration IDs are generated deterministically;
2. all 504 are executed or explicitly fail coverage/contract checks;
3. the 504-family statistical summary and parameter surfaces are written;
4. errors and corrections are logged;
5. a manuscript-style result and README status are updated.

## Interpretation boundary
Positive P&L or a high Sharpe in this historical extension is descriptive evidence only. It does not establish future profitability or executable bid/ask performance.