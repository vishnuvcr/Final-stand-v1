# Phase 21W — External Full-Strike Source Recovery

## Research question
Can the five remaining frozen weekly expiries be reconstructed with full strike-level 1-minute CE observations at the exact frozen entry/lock timestamps using independent external/public/broker/API sources, without synthetic bars or cross-source leg mixing?

The Phase-21 combined rerun has already established 58/63 executable expiries. The five unresolved expiries are the final holdout cycles: 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13 and 2026-05-12.

## Objective
Recover the five missing holdout cycles needed to complete the frozen Phase-17/19 224-variant weekly experiment. No strategy parameter, split, stop, slippage, cost model or statistical gate may be changed.

## Frozen design
- 63 weekly expiries only; 224 variants = 8 K1 × 4 K2 × 7 K3.
- Entry 10:00 IST; lock 14:00 IST; 50-point hard stop.
- 0.50 NIFTY-point slippage per leg and existing Paytm Money/NSE transaction-cost model.
- Original train/validation/holdout chronology and statistical gate remain frozen.

## Source order
1. Public Hugging Face `rissin/nse-options-intraday` NIFTY 1-minute archive, pinned to revision `78b1c5468255d18cf492984bfe6fe4e3ac874d7c`.
2. Upstox expired-option historical candles/API, if credentials/data entitlement permit.
3. ICICI Breeze historical option data.
4. Dhan expired-options data.
5. NSE/BSE historical datasets where full strike-level option OHLC/OI can be obtained.
6. Other public/open-source mirrors as validated fallbacks.

The RISSIN source is a new candidate because its dataset card states that NIFTY 1-minute intraday coverage runs from October 2024 through 2026, with expiry, strike, option type, OHLC and volume fields. Its intraday OI is documented as unavailable; OI is not used by the frozen execution engine for this experiment.

## Admission rules
A cycle is admitted only if all required legs for a variant have exact entry and lock observations from the same source, with expiry/strike/option-type/timestamp/OHLC/volume/OI validated. No synthetic interpolation, strike substitution, or cross-source leg mixing.

## Exit criteria
Every feasible source route is audited; access limitations are documented; an exact five-expiry coverage matrix is produced; recovered bars are provenance-pinned; then the frozen 224-variant rerun proceeds only if all 224 variants have valid executable bars for all five recovered expiries. If no free source satisfies the contract, broker/API access requirements are recorded as a blocking external dependency rather than weakening the frozen design.
