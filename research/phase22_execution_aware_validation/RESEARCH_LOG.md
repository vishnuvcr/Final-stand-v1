[object Object]

## 2026-09-30 — Strategy-horizon clarification
- Reviewed the frozen Phase 21 implementation and manuscript after a user challenge about the phrase “intraday strategy.”
- Confirmed that 10:00 IST is the entry timestamp and 14:00 IST is the lock timestamp, but these are not same-day open/close boundaries.
- The first trading day after the prior expiry is the entry day; the trading day before the target expiry is the lock day; remaining position may persist to target expiry unless stopped/exited earlier.
- Corrected the conversational characterization: **weekly-horizon strategy using intraday execution timestamps**, not an intraday-only strategy.
