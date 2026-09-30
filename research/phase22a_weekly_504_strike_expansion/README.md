# Phase 22A — Weekly 504-Configuration Strike Expansion

## Status: COMPLETE

Phase 22A tested all 504 weekly-horizon configurations after extending K1 through OTM8 and ITM8.

**504 = 18 K1 × 4 K2 × 7 K3.**

### Final results

- 504/504 configurations executed.
- 63/63 valid weekly cycles for every configuration.
- 414/504 positive training P&L.
- 239/504 positive validation P&L.
- 308/504 positive historical-holdout P&L.
- Mean historical-holdout P&L: **₹33,113.91** per configuration total.
- Mean historical-holdout annualized weekly Sharpe: **1.6885**.
- 323/504 raw bootstrap p-values <0.05.
- **0/504 Holm-adjusted p-values <0.05.**
- **0/504 capital-promotion passes.**

The descriptive surface was strongest around deeper ITM K1 rules, NEXT2/NEXT3 and larger K3 values, while the deeper OTM side weakened materially beyond OTM3. These are retrospective surface characteristics, not a prospective trading-rule selection.

### Evidence boundary

This is a **retrospective expansion of the completed Phase-21 63-expiry sample**, not a new unseen validation. The results remain OHLC-reconstructed because the historical source does not provide verified bid/ask/depth.

### Core files

- Phase 22A plan
- Variant registry
- Results
- Parameter-surface analysis
- Final manuscript
- Status
- Research log
- Error log
- Complete 504 results
- Compact 504 results
- K1/K2/K3 surface CSVs
- Static charts

### Workflow evidence

Run: 36741881293
Artifact: phase22a-weekly-504-results
Artifact ID: 11111230842
Artifact digest: sha256:1a250f5ca0a39aaefb3b293758eedc41293387e720cf65491e720a5cdb243964

### Next phase boundary

No configuration is promoted from Phase 22A. A genuinely new chronological period and execution-aware evidence remain required before any deployment interpretation.
