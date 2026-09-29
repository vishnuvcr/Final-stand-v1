# Phase 15W — Free/API Probe Protocol

## Decision

The expanded audit found no free historical BBO archive that can be admitted without an actual authenticated historical response.

The next probe is therefore **API capability testing**, not strategy testing.

## Candidates

### ICICI Breeze
Official SDK supports 1-minute historical NFO options addressed by expiry, strike and call/put. Its historical response contains OHLC, volume and OI, but not bid/ask. Therefore it is useful for an independent OHLC cross-check, not BBO validation. citeturn2search1turn2search0

### Dhan
The official Python client exposes expired-options data at 1-minute resolution with OHLC, IV, volume, strike, OI and spot fields. The API does not list historical bid/ask fields in the expired-options response. Therefore Dhan is an OHLC/coverage probe, not a historical-BBO solution. There is also an open report of severe row truncation in the rolling-options endpoint, so completeness must be tested before using it for cross-validation. citeturn1search0turn1search4

### Upstox
Upstox provides explicit expired-option contract discovery and 1-minute expired historical candles, but its expired-instrument endpoints require Upstox Plus. The returned data are OHLCV/OI rather than historical BBO. It is therefore not a free BBO route. citeturn0search0turn0search7turn0search2

### TrueData
Public documentation describes historical tick retrieval with optional bid/ask fields and support for expired symbols. This makes TrueData the first candidate whose documented API actually matches the required BBO data model. Exact date retention, expired weekly coverage and pricing still require authenticated/vendor verification; no purchase has been made. 

## Probe requirements

For any user-authorized API credential:

1. Resolve an expired NIFTY weekly CE and PE for a known study-period expiry.
2. Request a single trading session at 1-minute resolution.
3. Request the exact K1/K2/K3 contracts if the API supports explicit strikes.
4. Count returned observations.
5. Verify timestamps are complete from 09:15 through 15:30 where expected.
6. Verify fields: bid, ask, bid quantity, ask quantity, timestamp, contract identity.
7. Reject a source if it silently substitutes LTP/OHLC for BBO.
8. Repeat for a far-OTM protective leg; missing far-OTM data is a critical failure for the strategy.
9. Save raw API metadata and hashes, but do not publish credentials or private raw data.
10. Only after coverage passes should the frozen 63-cycle manifest be evaluated.

## No-tuning rule

This probe cannot change:
- strike-selection formula;
- weekly cycle dates;
- 10:00 entry;
- 14:00 lock;
- 50-point frozen stop;
- 0.50 index-point per-leg slippage used for selection;
- transaction-cost schedule;
- untouched holdout membership.

A quote dataset may replace execution-price reconstruction, but it may not be used to retune the strategy.

## Current gate

**FREE HISTORICAL BBO: NOT QUALIFIED.**

The next executable gate requires an authenticated API credential or a public downloadable historical BBO archive.