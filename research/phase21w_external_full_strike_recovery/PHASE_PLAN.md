# Phase 21W — External Full-Strike Source Recovery

## Research question
Can the remaining 40 frozen weekly expiries be reconstructed with full strike-level 1-minute CE observations at exact 10:00 entry and 14:00 lock timestamps using independent external/public/broker/API sources, without synthetic bars or cross-source leg mixing?

## Objective
Recover the missing executable cycles needed for the frozen Phase-17/19 224-variant weekly experiment.

## Frozen design
- 63 weekly expiries only; 224 variants = 8 K1 × 4 K2 × 7 K3.
- Entry 10:00 IST; lock 14:00 IST; 50-point hard stop.
- 0.50 NIFTY-point slippage per leg and existing Paytm Money/NSE transaction-cost model.
- Original train/validation/holdout chronology and statistical gate remain frozen.

## Source order
1. Upstox expired-option historical candles/API, if credentials/data entitlement permit.
2. ICICI Breeze historical option data.
3. Dhan expired-options data.
4. NSE/BSE historical datasets where full strike-level option OHLC/OI can be obtained.
5. Public/open-source mirrors as validated fallbacks.

## Admission rules
A cycle is admitted only if all required legs for a variant have exact entry and lock observations from the same source, with expiry/strike/option-type/timestamp/OHLC/volume/OI validated. No synthetic interpolation, strike substitution, or cross-source leg mixing.

## Exit criteria
Every feasible source route is audited; access limitations are documented; an exact coverage matrix is produced; recovered bars are provenance-pinned; then the frozen 224-variant rerun proceeds if coverage permits.
