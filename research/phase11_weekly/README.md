# Phase 11W - Weekly Backtest

This phase consumes the Phase 9W cycle manifest and selected 1-minute option and NIFTY spot bars.

## Execution model

The empirical series is conservative OHLC reconstruction:

- entry long uses open plus configured slippage;
- entry shorts use open minus configured slippage;
- K2 lock buyback uses open plus configured slippage;
- stop exits use the next available 1-minute bar after the stop condition is observed;
- expiry settlement uses the final available NIFTY spot bar and intrinsic K1/K3 spread payoff;
- Paytm Money brokerage is parameterized at INR 10 per executed F&O order;
- exchange, regulator and tax parameters are explicit configuration values and remain assumptions until their historical schedules are verified.

Paytm Money currently states INR 10 brokerage per unique executed F&O order.

NSE Circular 176/2025 changed the NIFTY lot size from 75 to 65; the first weekly expiry using the revised lot size was 06-Jan-2026.

## Stop-loss methodology

The video specifies a hard stop but does not provide a reproducible numerical threshold in the available source representation. Phase 11 therefore runs a stop-loss sensitivity grid. No grid value is silently promoted to the primary strategy. A value can only be frozen for the final holdout after training-period selection.

## Output

- trade_results.csv
- summary.json

No profitability conclusion is valid until the Phase 9 data-quality gate passes and the results survive chronological validation and realistic-cost stress.
