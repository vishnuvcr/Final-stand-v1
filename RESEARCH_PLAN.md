# Final Stand Research Plan — Phase 8 Strategy Extension

## Overall scientific objective
Determine whether the video-derived call-ladder-to-spread structure contains a repeatable, economically meaningful edge in NIFTY index options after realistic execution, margin and tail-risk constraints.

## Phase 8–14 work packages

### Phase 8 — Hypothesis formalization ✅ ACTIVE
Deliverables:
- source specification;
- payoff algebra;
- hypotheses;
- falsification criteria;
- literature review;
- manual GitHub Actions workflow.

Gate:
- strategy unambiguously defined;
- no empirical parameter optimization yet.

### Phase 9 — Point-in-time data reconstruction
Collect and validate:
- NIFTY spot/index;
- full option-chain quote/trade observations;
- strike, expiry, lot-size and contract mapping;
- OI, volume and IV;
- India VIX;
- FII/FPI/DII;
- global risk indicators;
- corporate/event calendar;
- exchange margin and risk-parameter files where available.

Gate:
- no missing contract mappings;
- no look-ahead;
- data snapshots reproducible;
- quote quality sufficient for multi-leg execution modelling.

### Phase 10 — Mechanics, Greeks, margin and costs
Build:
- exact payoff engine;
- lifecycle Greeks;
- margin state engine;
- Paytm Money fee model;
- spread/slippage model;
- stress scenarios.

Controls:
- pre-lock ladder;
- post-lock bull call spread;
- ordinary bull call spread;
- comparable long call.

Gate:
- numerical payoff matches independent algebra;
- margin reductions reproduced from exchange/broker inputs;
- cost schedule versioned by effective date.

### Phase 11 — Backtesting
Implement chronological:
- training;
- validation;
- walk-forward;
- execution simulation.

Variants limited to preregistered candidates:
- lock timing;
- target-premium tolerance;
- hard-stop family;
- expiry exit policy.

Gate:
- all candidate parameters frozen before final holdout;
- no manual trade selection.

### Phase 12 — Robustness and multiple testing
Perform:
- CPCV;
- PBO/CSCV-style diagnostics;
- deflated Sharpe ratio;
- block bootstrap;
- multiple-testing adjustment;
- liquidity/slippage stress;
- regime conditioning;
- tail-gap stress;
- margin stress.

Gate:
- edge not dependent on one narrow parameter combination or one market regime.

### Phase 13 — Untouched holdout
Run exactly one frozen strategy version on an unseen historical period.

Primary output:
- net return;
- Sharpe;
- drawdown;
- expected shortfall;
- return on peak margin;
- transaction-cost attribution.

Gate:
- independent holdout evidence is required for any promotion.

### Phase 14 — Final manuscript
Produce:
- abstract;
- introduction;
- literature review;
- methods;
- hypotheses;
- data;
- statistical methodology;
- results;
- figures;
- tables;
- discussion;
- strengths/limitations;
- conclusion;
- future research;
- supplementary methods;
- data dictionary;
- code/reproducibility manifest.

## Decision framework

### Promote for further research
Only if net performance, risk and margin efficiency survive the statistical and economic gates.

### Retain as research signal
If payoff/mechanics are sound but profitability evidence is inconclusive or regime-dependent.

### Reject
If the apparent edge disappears under realistic costs, tail stress, out-of-sample testing or data-quality controls.

## Explicit non-goals
- No guarantee of profitability.
- No use of final holdout for parameter tuning.
- No conversion of a source-video claim into a live trading recommendation without empirical validation.
- No endless optimization after Phase 14.
