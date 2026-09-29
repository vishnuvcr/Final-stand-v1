# Final Stand v1 — Market Inefficiency Research

## Active research reset
**The active strategy research has been reset from monthly to weekly NIFTY expiries.**

Active branch: `phase-8-weekly-expiry-restart`

Archived/superseded branch: `phase-8-video-call-ladder` — monthly-expiry design, retained for auditability only.

## Weekly research objective
Test the same core video-derived call-ladder-to-spread strategy as a **weekly trading system**, with one complete trade cycle per NIFTY weekly expiry.

NSE currently documents four weekly NIFTY 50 index-option expiry contracts excluding monthly contracts, with weekly expiry on Tuesday or the previous trading day if Tuesday is a holiday, and a new serial weekly contract introduced after expiry.

Research branch:
https://github.com/vishnuvcr/Final-stand-v1/tree/phase-8-weekly-expiry-restart

## Reset decision
The monthly experiment is not being mechanically converted into weekly data. The weekly branch has a new:
- weekly lifecycle;
- entry/lock/exit timing;
- weekly data-quality gate;
- weekly cost/turnover model;
- weekly-specific hypotheses;
- weekly literature review;
- weekly robustness framework.

## Active weekly phase map
- 8W — Weekly strategy definition ✅
- 9W — Weekly point-in-time data 🟡 pending
- 10W — Mechanics, margin and costs
- 11W — Weekly backtest
- 12W — Robustness / CPCV / PBO / DSR
- 13W — Untouched weekly holdout
- 14W — Final research manuscript

## Research governance
The repository remains the canonical research-state record. Research steps, errors, phase status, methodology changes and final results are committed as auditable artifacts.

## No trading conclusion
No profitability conclusion or live-trading recommendation has been established. The weekly strategy must survive realistic execution costs, tail-risk testing, chronological robustness and an untouched holdout.
