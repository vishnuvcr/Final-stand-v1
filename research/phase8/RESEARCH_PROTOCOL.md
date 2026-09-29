# Phase 8 Research Protocol

## Phase objective
Convert the video-described setup into a falsifiable experiment without assuming the video claim is true.

## Sequence

### 8.1 Source and literature audit
- Preserve the user-supplied video rule as source material.
- Verify payoff algebra independently.
- Review bull call ladders, ratio spreads, theta/gamma, margin and transaction-cost literature.
- Record ambiguities and disagreements.

### 8.2 Market-rule validation
- Verify NIFTY contract schedule, strikes, tick sizes, lot sizes and settlement.
- Verify current and historical expiry conventions.
- Verify Paytm Money brokerage, margin and order constraints.
- Acquire dated cost schedules.

### 8.3 Data acquisition
Acquire point-in-time:
- NIFTY spot/index;
- NIFTY option quote/trade data;
- volume and OI;
- implied volatility where available;
- India VIX;
- FII/FPI/DII data;
- global risk indicators;
- margin reports where available.

Cache immutable raw snapshots and checksums.

### 8.4 Data-quality gate
Reject duplicates, stale quotes, crossed markets, impossible premiums, missing contract mappings, inconsistent lot sizes and invalid option bounds.

### 8.5 Backtest engine
Implement a state machine:
ENTRY -> WAIT/DECAY -> LOCK -> POST-LOCK MANAGEMENT -> EXIT/EXPIRY.

Every transition is time-stamped.

### 8.6 Baseline controls
Run locked strategy, unmodified ladder, plain bull call spread and matched-risk benchmark under the same dates and execution assumptions.

### 8.7 Parameter governance
Validation may choose only among a predefined candidate family. Final holdout parameters are frozen.

### 8.8 Statistical testing
Use chronological splits, walk-forward analysis, bootstrap intervals, CPCV/PBO/DSR diagnostics and multiple-testing control.

### 8.9 Economic stress testing
Stress spread width, slippage, brokerage, fill probability, lock timing, margin, overnight gap and large upside gaps through K3.

### 8.10 Final holdout
Reserve one untouched period for the final verdict. Do not modify methodology after reading it.

### 8.11 Final manuscript
Produce abstract, introduction, literature review, methods, hypotheses, results, figures, tables, appendices, limitations, conclusion, future research and reproducibility manifest.

## Stop condition
Stop after the predefined manuscript/reproducibility gate. Do not turn the work into an open-ended parameter search.
