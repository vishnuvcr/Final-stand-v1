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


## 2026-09-29 — Weekly data and mechanics gate
- Official NSE sources were audited. NSE provides historical F&O framework, daily contract-wise price/volume data, daily reports, SPAN risk-parameter files and margin-report infrastructure. citeturn0search31turn0search6turn6search0turn6search5
- Public GitHub research repositories demonstrate that 1-minute NIFTY weekly option datasets exist, including a pipeline covering 39 Tuesday-expiry weeks from Sep 2025 to May 2026 and other datasets covering weekly options. These sources are useful for data discovery/prototyping but are not treated as authoritative execution data without source/licence/quote-quality validation. citeturn2search1turn2search2
- The empirical gate remains blocked because the final study requires point-in-time bid/ask or sufficiently conservative executable-price reconstruction for K1/K2/K3 at entry and K2/K1/K3 at lock.
- Implemented deterministic weekly mechanics engine and local unit checks.
- Implemented dated brokerage/statutory/slippage/margin framework.
- Paytm Money currently states ₹10 brokerage per unique executed F&O order. citeturn6search8
- NSE's SPAN documentation confirms portfolio-based scenario margining and daily risk-parameter files; exact historical margin requires the relevant dated files. citeturn6search3turn6search1
- Phase status: 9W blocked pending qualified intraday data; 10W active and mechanics framework implemented.
