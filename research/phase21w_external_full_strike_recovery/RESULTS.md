# Phase 21W Final Results

## Completion

Successful end-to-end workflow: GitHub Actions run 36717226605.

### Data recovery

- Five missing holdout expiries recovered from immutable RISSIN snapshot 8f7739cab3f38abdcbc6332a6d0a83e1341326e3.
- Source file: upstox_intraday/NIFTY/NIFTY_2026.parquet.
- File SHA-256: bae9943b2fa99ee9c1214fb7c695b84f9f661a050a5cd04d9c5c2ffc7bc59f73.
- 224/224 variants admitted on every recovered expiry.
- 1,120 external variant-cycle cells added.
- Final coverage: 63/63 expiries and 12,822 variant-cycle cells.

### Final 224-variant result

| Measure | Result |
|---|---:|
| Variants | 224 |
| Positive training P&L | 193 |
| Positive validation P&L | 136 |
| Positive holdout P&L | 163 |
| Mean training total P&L across variants | ₹83,517.66 |
| Mean validation total P&L across variants | ₹4,960.88 |
| Mean holdout total P&L across variants | ₹33,660.78 |
| Mean holdout annualized weekly Sharpe | 2.357 |
| Minimum validity rate | 41/63 = 0.6508 |
| Mean validity rate | 0.9086 |
| Minimum Holm-adjusted training p | 0.07464 |
| Promotion-gate variants | 0/224 |

Variant-level P&L totals overlap in time and are not additive portfolio results.

### Promotion gate

The frozen promotion gate requires all of:

- validity >= 50/63;
- training n >= 30;
- positive training mean net P&L;
- validation n >= 8;
- positive validation mean net P&L;
- Holm-adjusted training p < 0.05.

No configuration passed all conditions.

### Decision

**Phase 21W is complete. No configuration is promoted to the capital phase under the preregistered frozen protocol.**

The completed evidence resolves the historical-data gap but does not establish a statistically admissible live-trading candidate. Historical OHLC reconstruction, slippage and transaction-cost assumptions remain execution-model limitations.

See [FINAL_MANUSCRIPT.md](FINAL_MANUSCRIPT.md) for the full scientific report.
