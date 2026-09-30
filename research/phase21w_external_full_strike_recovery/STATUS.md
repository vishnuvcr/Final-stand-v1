# Phase 21W Status

**State:** RUNNING — external recovery of the final five holdout expiries.

## Current gate

The exact frozen 224-variant combined rerun completed for **58/63** weekly expiries, with **11,702** combined variant-cycle cells and zero HF-03/HF-02 overlap. Five baseline expiries remain completely unrecovered:

- 2026-01-13
- 2026-02-10
- 2026-03-10
- 2026-04-13
- 2026-05-12

These five are all in the untouched holdout portion, so the current empirical results are **not yet the final 63-cycle holdout result**.

## New external-source route

A public Hugging Face dataset, `rissin/nse-options-intraday`, was identified as a candidate source. Its dataset card documents NIFTY 1-minute intraday coverage from October 2024 through 2026, with expiry, strike, option type, OHLC and volume fields. The source was pinned to revision `78b1c5468255d18cf492984bfe6fe4e3ac874d7c`.

The next executable step is to download only the NIFTY 2026 parquet through the existing HF_TOKEN-enabled workflow, isolate the five missing expiries, reconstruct the frozen 224-variant strike selections, and validate exact 10:00/14:00 timestamp coverage plus stop-path bars.

## Frozen constraints

- 63 weekly expiries; 224 variants.
- 60/20/20 chronological train/validation/holdout split remains frozen.
- Entry 10:00 IST; lock 14:00 IST.
- 50-point hard stop.
- 0.50 NIFTY-point slippage per leg.
- Existing Paytm Money/NSE transaction-cost model.
- No synthetic interpolation, strike substitution or cross-source leg mixing.
- External bars may fill only the five previously missing expiry cycles; existing 58-cycle HF-03/HF-02 observations are not replaced.

## Phase completion condition

Complete the five-cycle recovery and rerun only if all 224 variants are executable on all five dates. Otherwise record the exact missing cells and source limitation and do not manufacture a 63-cycle conclusion.
