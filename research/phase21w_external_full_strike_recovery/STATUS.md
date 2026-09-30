# Phase 21W — External Full-Strike Recovery Status

State: RUNNING — recovering the five missing holdout expiries without altering the frozen 224-variant experiment.

Current missing expiries:
- 2026-01-13
- 2026-02-10
- 2026-03-10
- 2026-04-13
- 2026-05-12

Current data route: Rissin nse-options-intraday, pinned to revision 78b1c5468255d18cf492984bfe6fe4e3ac874d7c. Its dataset card documents NIFTY 1-minute intraday coverage from October 2024 through 2026, with expiry, strike, option type, OHLC and volume fields; intraday OI is unavailable and is not required by the frozen execution engine.

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