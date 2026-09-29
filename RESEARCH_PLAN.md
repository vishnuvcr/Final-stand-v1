# Final Stand Research Plan — Weekly Reset

## Research reset
The prior monthly-expiry call-ladder experiment is archived for auditability. The active research program now evaluates the same core strategy on **NIFTY weekly expiries with one complete trade cycle per week**.

## Phase map

### Phase 8W — Weekly hypothesis formalization ✅
- Weekly strike-selection rule.
- Weekly lifecycle.
- Weekly lock rule.
- Weekly stop-loss family.
- Weekly controls.
- Weekly literature review.
- Weekly data requirements.

### Phase 9W — Point-in-time weekly data 🟡 Active
Primary ingestion source is now Hugging Face, using thetrademarkk/india-index-options-1m 1-minute NIFTY option-chain files plus the NIFTY spot file. A secondary Hugging Face source is reserved for overlapping cross-validation. Because the primary public source documents OHLC rather than bid/ask, the phase has two execution-quality tiers: conservative 1-minute OHLC reconstruction and any later true bid/ask source.

Acquire and validate:
- weekly NIFTY spot;
- weekly option quotes/trades;
- K1/K2/K3 at entry and lock;
- volume/OI/IV;
- lot-size and contract mapping;
- margin;
- India VIX;
- FII/FPI/DII;
- global volatility and cross-asset variables;
- event/regime indicators.

Pilot target: >=52 weekly expiries; preferred >=104.

### Phase 10W — Mechanics, margin and full cost model
Build:
- payoff engine;
- Greek/lifecycle attribution;
- margin state engine;
- Paytm Money dated fee schedule;
- bid/ask/slippage model;
- weekly turnover model.

### Phase 11W — Weekly backtest
Run:
- training;
- validation;
- walk-forward;
- weekly trade ledger;
- matched controls.

### Phase 12W — Robustness
Run:
- CPCV;
- PBO/CSCV-style diagnostics;
- DSR;
- block bootstrap;
- multiple-testing correction;
- regime conditioning;
- spread/slippage stress;
- tail-gap stress;
- margin stress.

### Phase 13W — Untouched weekly holdout
Run one frozen weekly strategy version on a contiguous unseen expiry sample.

Primary outputs:
- net weekly expectancy;
- Sharpe;
- drawdown;
- loss frequency;
- 4-week rolling loss;
- expected shortfall;
- peak margin;
- transaction-cost attribution.

### Phase 14W — Final weekly manuscript
Produce:
- abstract;
- introduction;
- literature review;
- methods;
- hypotheses;
- data;
- results;
- figures;
- tables;
- statistical appendix;
- cost/margin appendix;
- limitations;
- conclusion;
- future research;
- reproducibility package.

## Decision gates

### Promotion
Only if the weekly edge survives costs, tail-risk, chronological robustness and untouched holdout tests.

### Research-only
Mechanics are valid but economic edge is inconclusive, fragile or regime-dependent.

### Rejection
Edge disappears with realistic execution, statistical correction or unseen weekly data.

## Non-goals
- No monthly/weekly blending in the primary test.
- No final-holdout optimization.
- No midpoint-only profitability claims.
- No endless parameter search.
