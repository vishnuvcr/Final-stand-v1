# Phase 21W — External Full-Strike Recovery Status

State: RUNNING — recovering the five missing holdout expiries without altering the frozen 224-variant experiment.

Current missing expiries:
- 2026-01-13
- 2026-02-10
- 2026-03-10
- 2026-04-13
- 2026-05-12

Current data route: Rissin nse-options-intraday. The workflow resolves the current `main` revision at run start, discovers the exact NIFTY 2026 intraday parquet, and records both the resolved commit SHA and file SHA-256 before admission. The dataset card documents NIFTY 1-minute intraday coverage through 2026 with expiry, strike, option type and OHLC/volume fields; intraday OI is unavailable and is not required by the frozen execution engine.

Frozen constraints:
- 63 weekly expiries.
- 224 variants = 8 K1 × 4 K2 × 7 K3.
- Chronological split remains 37/12/14 train/validation/holdout.
- Entry 10:00 IST; lock 14:00 IST.
- 50-point hard stop.
- 0.50 NIFTY-point slippage per leg.
- Existing Paytm Money/NSE transaction-cost model.
- No synthetic interpolation, strike substitution or cross-source leg mixing.
- External bars can fill only the five previously missing expiries; existing 58-cycle data are immutable.

Next gate: source-level probe of the Rissin 2026 NIFTY parquet, followed by exact frozen variant reconstruction for the five dates only.
- The prior `78b1c54` pin produced a 404 because that historical revision did not contain the NIFTY 2026 parquet. The recovery route now validates file existence at the resolved current revision before downloading.
