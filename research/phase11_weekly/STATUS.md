# Phase 11W Status

## Branch
phase-11w-weekly-backtest

## State
Implementation complete; waiting for Phase 9 data-gate output.

## Controls implemented
- 1-minute OHLC reconstruction.
- Explicit slippage.
- Paytm Money brokerage parameter.
- Lot-size transition: 75 through 23-Dec-2025 and 65 from 06-Jan-2026.
- K2 lock buyback.
- Pre-lock and post-lock stop handling.
- Expiry intrinsic settlement after lock.
- No-stop baseline plus seven stop-loss values.
- Unit tests.
- Manual workflow and push-triggered autonomous execution.

## Scientific restriction
The stop-loss numeric threshold is not stated in the source representation, so Phase 11 treats stop levels as a sensitivity family. A final holdout value must be frozen only after training-period selection.

No profitability conclusion is currently admitted.
