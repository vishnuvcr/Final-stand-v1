# Phase 8W — Weekly Expiry Strategy Specification

## 1. Major reset

This branch **supersedes the monthly-expiry version as the active research design**.

The monthly branch `phase-8-video-call-ladder` is retained for auditability but is not part of the new primary experiment.

The new unit of analysis is:

> **one NIFTY weekly expiry = one complete trade cycle**

The strategy is therefore tested as a **weekly trading system**, not as a monthly strategy with weekly observations.

## 2. Current exchange structure

Current NSE documentation states that NIFTY 50 index options have four weekly expiry contracts excluding the monthly contracts, and that weekly contracts expire every Tuesday; if Tuesday is a trading holiday, the previous trading day is the expiry/last trading day. NSE also states that a new serial weekly option is introduced after the respective week's expiry. citeturn642743search0turn642743search1

Historical backtests must still use the contract rules effective on each historical date.

## 3. Weekly trade-cycle definition

Primary cycle:

1. Weekly contract expires on Tuesday or the preceding trading day if Tuesday is a holiday.
2. The next serial weekly contract becomes the target contract.
3. **Entry:** first trading session after the previous weekly expiry, using a fixed 10:00 IST decision timestamp.
4. **Construction:** build the three-call ladder from that weekly expiry.
5. **Decay window:** hold the ladder through the remainder of the week.
6. **Lock:** buy back K2 at a fixed 14:00 IST decision timestamp on the trading day immediately preceding expiry.
7. **Post-lock:** retain long K1 / short K3 bull call spread.
8. **Final exit:** close the remaining spread using executable prices before expiry settlement, or use the final settlement/expiry P&L only in the separate expiry-held control.
9. **One primary trade per weekly expiry.**

If a scheduled timestamp is unavailable because of a holiday, halt/suspension, invalid quote or missing contract data, the cycle is classified according to the preregistered missing-data rule rather than shifted opportunistically.

## 4. Strike construction

At entry:

- K1 = first listed call strike strictly above spot.
- K2 = next listed call strike above K1.
- D = reference premium(K1) - reference premium(K2).
- Target premium = 2D.
- K3 = the listed call strike above K2 whose reference premium is closest to the target premium.
- If D <= 0, the cycle fails the strategy-entry condition and no trade is opened.

Primary quote for strike selection:
- midpoint if valid bid and ask are both positive and contemporaneous;
- otherwise LTP only as a lower-quality sensitivity observation.

Actual fills are never assumed to occur at midpoint.

## 5. Position at entry

+1 C(K1) -1 C(K2) -1 C(K3), same weekly expiry.

The initial entry may be a net credit or debit depending on the observed premiums and execution prices. It is not assumed to be a free-credit trade.

## 6. Lock operation

At the preregistered lock timestamp:

Buy one K2 call to close the original short.

The resulting position is:

+C(K1) - C(K3).

This is a defined-risk bull call spread.

The research will separately measure:
- P&L created before the lock;
- P&L from the K2 buyback;
- post-lock spread P&L;
- total round-trip P&L.

## 7. Weekly stop-loss

Because the video requires a hard stop but provides no exact number, the weekly experiment separates:

### Primary source-faithful framework
A hard stop exists, but no unsupported numeric value is claimed from the video.

### Mechanical validation family
A small preregistered family will be evaluated only on training/validation data:
- total-position loss threshold;
- initial-risk multiple;
- underlying-price stop;
- post-lock spread-value stop.

The final weekly holdout uses exactly one frozen stop rule.

## 8. Weekly timing sensitivities

Primary timing:
- Entry: first eligible trading session after expiry at 10:00 IST.
- Lock: previous trading day at 14:00 IST.
- Exit: predefined close window before weekly settlement.

Secondary, preregistered validation variants:
- entry at 09:30;
- entry at 11:00;
- lock Friday/one or two sessions before expiry when available;
- lock Monday 14:00;
- expiry-day controlled exit.

These are validation alternatives, not parameters to be searched continuously.

## 9. Transaction-cost model

Every leg includes:

- Paytm Money brokerage;
- STT;
- exchange transaction charges;
- SEBI fees;
- stamp duty where applicable;
- GST;
- bid/ask spread;
- slippage;
- liquidity/market-impact allowance;
- any applicable square-off or execution charges.

Weekly trading produces more turnover than monthly trading, so total cost per completed cycle is a first-class endpoint rather than a secondary adjustment.

## 10. Margin and capital model

Track:

- initial margin at three-leg entry;
- peak intracycle margin;
- margin immediately before lock;
- margin immediately after K2 buyback;
- margin of the remaining bull call spread;
- margin during worst simulated weekly move.

Report:

- absolute margin;
- percentage margin reduction;
- return on peak margin;
- return on average margin;
- cost per unit margin;
- capital efficiency versus a plain bull call spread.

The video-reported rupee margin example is not used as empirical evidence.

## 11. Primary hypotheses

### H1 — Weekly profitability
After all transaction costs and realistic slippage, the weekly strategy has positive expected net P&L across the out-of-sample period.

### H2 — Lock benefit
The K2 buyback improves risk-adjusted economics versus holding the original three-leg ladder through expiry.

### H3 — Capital efficiency
The lock materially reduces margin while retaining a meaningful fraction of the trade's expected value.

### H4 — Relative value
The premium-difference rule provides incremental value versus a matched plain bull call spread.

### H5 — Weekly robustness
Results are not concentrated in one small group of weekly expiries, one volatility regime, or one execution assumption.

## 12. Mandatory controls

Every weekly cycle must be paired, where data permits, with:

1. video-derived weekly strategy;
2. same-entry three-leg ladder held without lock;
3. K1/K3 plain bull call spread;
4. matched-risk bull call spread;
5. simple K1 long call control.

## 13. Weekly-specific risk metrics

In addition to standard return statistics:

- losing-week frequency;
- consecutive losing weeks;
- worst single weekly loss;
- worst 4-week rolling loss;
- weekly expected shortfall;
- gap-through-K3 loss;
- margin call/square-off exposure;
- weekly turnover;
- cost/gross-P&L ratio;
- percentage of weeks where the lock is reached;
- percentage of weeks where the hard stop triggers before lock;
- average D and K3 distance from spot.

## 14. Statistical design

Primary evaluation:
- chronological training / validation / final holdout;
- walk-forward weekly evaluation;
- block bootstrap at the weekly-cycle level;
- CPCV where sufficient sample size permits;
- PBO / CSCV-style overfitting diagnostic;
- deflated Sharpe ratio;
- multiple-testing adjustment across preregistered weekly variants.

No final-holdout parameter selection.

## 15. Regime variables

Where available, synchronize:

- NIFTY realized volatility;
- India VIX;
- NIFTY trend;
- weekly opening gap;
- previous-week return;
- FII/FPI and DII activity;
- option skew;
- option term structure;
- NIFTY futures basis;
- USD/INR;
- gold;
- global equity and volatility indices;
- breadth;
- major scheduled-event windows.

The purpose is to determine whether weekly strategy performance depends on identifiable states, not to cherry-pick favorable weeks.

## 16. Weekly falsification gates

Reject the strategy for promotion if:

- net expectancy becomes non-positive under realistic costs;
- returns disappear after conservative slippage;
- losses are dominated by a small number of upside tail events;
- apparent profitability requires illiquid quotes;
- the lock only appears valuable under midpoint fills;
- margin relief is not reproducible;
- performance is unstable across chronological blocks;
- results fail after multiple-testing adjustment;
- there is evidence of look-ahead or post-hoc strike selection.

## 17. Research stop condition

The weekly branch stops after:

Phase 8W → Phase 9W data → Phase 10W mechanics/costs → Phase 11W backtest → Phase 12W robustness → Phase 13W untouched holdout → Phase 14W manuscript.

No endless optimization is allowed.


## 15. Weekly target-error diagnostic

For every empirical cycle calculate:

`target_error = |premium(K3) - 2*(premium(K1)-premium(K2))| / [2*(premium(K1)-premium(K2))]`

This is a mandatory descriptive variable because weekly strikes are discrete and very short-dated OTM premiums can make the requested target unattainable.

Report target error by:
- days to expiry;
- IV;
- liquidity;
- spot/strike distance;
- volatility regime.
