# Research Log

## 2026-09-29 — Major strategy reset to weekly trading
- User instructed that the monthly-expiry strategy research be restarted using weekly expiries and weekly trading.
- Re-read the current repository research-state files before modifying the research design.
- Created new branch `phase-8-weekly-expiry-restart` from main so the monthly research remains auditable but is no longer the active experiment.
- Verified current NSE NIFTY option specifications: four weekly expiry contracts excluding monthly contracts; weekly expiry every Tuesday; prior trading day if Tuesday is a holiday; new serial weekly contract after expiry. citeturn642743search0turn642743search1
- Redefined the experimental unit as one complete weekly expiry cycle.
- Froze a primary operational cycle: entry on the first trading session after expiry at 10:00 IST, lock on the preceding trading day at 14:00 IST, and predefined exit before expiry settlement.
- Replaced the monthly research questions and data requirements with weekly-specific versions.
- Increased the pilot data requirement from monthly expiries to at least 52 weekly expiry cycles, preferably 104+ if quote quality permits.
- Explicitly elevated weekly turnover and transaction costs to primary endpoints.
- Current status: weekly design gate PASSED; historical weekly quote-data gate PENDING.


## 2026-09-29 — Weekly reset completion
- Created the weekly literature review and fresh weekly master research plan.
- Confirmed the monthly research plan is not copied into the active weekly branch.
- Added branch-local status and error logging.
- Weekly branch status remains design gate passed / data gate pending.
