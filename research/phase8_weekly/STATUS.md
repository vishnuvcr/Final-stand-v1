# Research Status

## Active research branch
**phase-8-weekly-expiry-restart**

The prior monthly-expiry Phase 8 is retained for auditability but has been superseded as the active experimental design.

| Phase | Status | Gate |
|---|---|---|
| 0 — Governance | ✅ Complete | Repository governance exists |
| 1–7 — Prior research | 🟡 Preserved | Historical project artifacts |
| 8M — Monthly strategy | ⚪ Archived | Superseded by weekly reset |
| 8W — Weekly strategy definition | ✅ Complete | Weekly objective, cycle and controls frozen |
| 9W — Weekly PIT data | 🟡 Blocked/Pending | Official data sources identified; historical intraday quote access still required |
| 10W — Mechanics/margin/costs | 🟡 Active | Mechanics engine and cost/margin framework implemented; exact historical margin pending |
| 11W — Weekly backtest | ⏳ Pending | Depends on 10W |
| 12W — Robustness | ⏳ Pending | Depends on 11W |
| 13W — Final holdout | ⏳ Pending | Depends on frozen methodology |
| 14W — Manuscript | ⏳ Pending | Depends on completed empirical results |

## Phase 10W findings
- Deterministic mechanics engine implemented and locally checked.
- K2 buyback is confirmed to cancel the middle short exactly.
- Pre-lock payoff remains a bull call ladder with unbounded upside loss.
- Weekly discrete strikes introduce a mandatory target-error diagnostic.
- Exact historical margin remains dependent on dated SPAN inputs.

## Current weekly finding
NSE currently documents four weekly NIFTY 50 option expiries excluding monthly contracts, with Tuesday weekly expiry and a new weekly series introduced after expiry. citeturn642743search0turn642743search1

No weekly profitability result has been established.
