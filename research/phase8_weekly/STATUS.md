# Research Status

## Active research branch
**phase-9w-hf-data-gate**

The prior monthly-expiry Phase 8 is retained for auditability but has been superseded as the active experimental design.

| Phase | Status | Gate |
|---|---|---|
| 0 — Governance | ✅ Complete | Repository governance exists |
| 1–7 — Prior research | 🟡 Preserved | Historical project artifacts |
| 8M — Monthly strategy | ⚪ Archived | Superseded by weekly reset |
| 8W — Weekly strategy definition | ✅ Complete | Weekly objective, cycle and controls frozen |
| 9W — Weekly PIT data | 🟡 Active | Hugging Face 1-minute option/spot sources available; OHLC execution reconstruction is being validated and true bid/ask remains a separate quality tier |
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

## Phase 9W current data finding
Hugging Face now provides a feasible primary research source with expiry-partitioned 1-minute NIFTY options and a separate 1-minute NIFTY spot file. The dataset documentation explicitly describes OHLC rather than bid/ask, so the empirical phase will not silently treat OHLC as observed order-book execution.

The active Phase 9 branch now:
- excludes monthly expiries from the weekly experimental universe;
- preserves the prior weekly expiry across the pilot-window boundary;
- removes 10:00 intrabar look-ahead by using bar-open prices;
- records K1/K2/K3 at entry and lock;
- cross-checks 2025 prices against a second Hugging Face source;
- captures source revisions and SHA-256 metadata;
- uses HF_TOKEN plus the Hugging Face cache in a manual GitHub Actions workflow.

The next gate is a 52–104 weekly-expiry pilot with source checksums, strike completeness, entry/lock coverage, target-error diagnostics and an independent cross-source comparison.

No weekly profitability result has been established.
