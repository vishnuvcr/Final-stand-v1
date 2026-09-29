# Final Stand v1 — Market Inefficiency Research

## Active research reset
**The active strategy research has been reset from monthly to weekly NIFTY expiries.**

Active branch: `phase-9w-hf-data-gate`

Archived/superseded branch: `phase-8-video-call-ladder` — monthly-expiry design, retained for auditability only.

## Weekly research objective
Test the same core video-derived call-ladder-to-spread strategy as a **weekly trading system**, with one complete trade cycle per NIFTY weekly expiry.

NSE currently documents four weekly NIFTY 50 index-option expiry contracts excluding monthly contracts, with weekly expiry on Tuesday or the previous trading day if Tuesday is a holiday, and a new serial weekly contract introduced after expiry.

Research branch:
https://github.com/vishnuvcr/Final-stand-v1/tree/phase-9w-hf-data-gate

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
- 9W — Weekly Hugging Face point-in-time data 🟡 active
- 10W — Mechanics, margin and costs
- 11W — Weekly backtest
- 12W — Robustness / CPCV / PBO / DSR
- 13W — Untouched weekly holdout
- 14W — Final research manuscript

## Research governance
The repository remains the canonical research-state record. Research steps, errors, phase status, methodology changes and final results are committed as auditable artifacts.

## Phase 9W data status
Hugging Face now provides a usable primary research source with expiry-partitioned 1-minute NIFTY options and a separate NIFTY index file. The source is OHLC-based rather than historical bid/ask, so Phase 9 distinguishes conservative OHLC execution reconstruction from true order-book evidence. A second Hugging Face source is wired in for 2025 cross-validation.

The active branch contains a manual GitHub Actions workflow using HF_TOKEN and the Hugging Face cache. Empirical results are not yet admitted because the workflow run itself has not yet been executed/verified.

## No trading conclusion
No profitability conclusion or live-trading recommendation has been established. The weekly strategy must survive realistic execution costs, tail-risk testing, chronological robustness and an untouched holdout.


## Latest research pipeline status — 2026-09-29
- Phase 9W: Hugging Face weekly data gate implemented and push-triggered for execution; no empirical pass/fail result is being fabricated.
- Phase 11W: cost-adjusted weekly backtest pipeline implemented on a separate branch, including Paytm Money brokerage, lot-size changes, slippage, lock mechanics and stop-loss sensitivity.
- Phase 12W: chronological robustness and block-bootstrap stress pipeline implemented on a separate branch, including slippage stress.
- Active branch for the next research phase: phase-12w-robustness.
- Results remain conditional on successful upstream data ingestion and validation.
