# Phase 22B Research Updates

## 2026-10-01 — Prospective extension and source-coverage review
- Extended the prospective input boundary from 2026-08-04 to 2026-09-08 without changing strategy mechanics.
- Workflow 36763880416 completed successfully.
- Revalidated all 504 frozen configurations.
- 4,032/4,032 variant-cycle rows remained usable.
- 376/504 variants had positive total net P&L.
- All variants still had n=6; the pre-specified bootstrap/Holm inference therefore remained unavailable.
- The extension did not add qualifying weekly option expiries beyond 2026-07-21.
- Reviewed independent/public source coverage:
  - RISSIN remains the primary free intraday source used by the run.
  - TradeMarkk reaches 2026-08-04 for NIFTY and documents partial option coverage.
  - codepyx23 is a duplicate/mirror of TradeMarkk, not an independent source.
  - NSE provides official contract-wise historical derivatives reports and historical order/trade specifications, but not a directly downloadable free 1-minute expired-option archive matching the required input.
  - A commercial 1-minute NIFTY full-chain archive advertises coverage through September 2026; it is a paid candidate and lacks bid/ask/order-book data.
- No strategy parameter, sample-size gate, cost model, or configuration-selection rule was changed.
- Next action: continue source recovery before another prospective rerun.
