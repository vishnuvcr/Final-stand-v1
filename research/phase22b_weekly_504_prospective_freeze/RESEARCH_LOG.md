# Phase 22B Research Log

## 2026-09-30 — Prospective freeze
- Phase 22A completed the retrospective 504-family expansion.
- A new branch was created for prospective validation.
- The complete 504-family was frozen before opening the new chronological period.
- The new period begins after the Phase-21 last target expiry (2026-05-12).
- Public source audit found the TradeMarkk/Hugging Face NIFTY archive currently reaches 2026-08-04 and documents 1-minute OHLCV(+OI) option bars. citeturn7search2turn8search0
- No bid/ask/depth data are assumed; this phase is explicitly OHLC-based.
- No configuration was selected from Phase 22A before the holdout was opened.


## 2026-10-01 — Frozen robustness-envelope prospective sub-analysis
The retrospective Phase 22A robustness surface identified the 30-member envelope ITM3–ITM7 × NEXT2/NEXT3 × K3 2.5/3/4. This sub-analysis freezes that entire region without selecting an individual member and evaluates it alongside the full 504-family.

Preliminary existing Phase 22B result (8 admitted expiries; n=6 completed observations/configuration): all 30 envelope members have positive cumulative net P&L, win rate >=83.33%, and zero recorded cumulative drawdown. Mean cumulative net P&L is approximately ₹94,845 and median approximately ₹90,885. These figures are **not confirmatory** because n=6 is below the frozen bootstrap minimum and far below the 30-cycle capital gate.

The next qualifying prospective cycles must be appended without changing the envelope. Every member will be reported separately and as an aggregate region. No member will be selected from this preliminary result.
