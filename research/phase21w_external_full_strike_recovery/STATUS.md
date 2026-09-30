# Phase 21W — External Full-Strike Recovery Status

State: **COMPLETE**

Completed end-to-end workflow: GitHub Actions run **36717226605**.

## Final coverage

- 63/63 weekly expiries represented.
- 12,822 admitted variant-cycle cells.
- 58/63 base expiries were preserved unchanged.
- Exactly five previously missing holdout expiries were recovered.
- 1,120 external variant-cycle cells were added.
- 0 cycle overlap and 0 duplicate external bar groups.

## External provenance

- Dataset: RISSIN / Hugging Face nse-options-intraday.
- Immutable revision: 8f7739cab3f38abdcbc6332a6d0a83e1341326e3.
- File: upstox_intraday/NIFTY/NIFTY_2026.parquet.
- File SHA-256: bae9943b2fa99ee9c1214fb7c695b84f9f661a050a5cd04d9c5c2ffc7bc59f73.
- All five targets admitted 224/224 variants using exact entry/lock observations.

## Final 224-variant frozen rerun

- Positive training total P&L: 193/224.
- Positive validation total P&L: 136/224.
- Positive holdout total P&L: 163/224.
- Mean holdout annualized weekly Sharpe across variants: 2.357.
- Minimum 63-cycle validity rate: 0.6508.
- Mean 63-cycle validity rate: 0.9086.
- Minimum Holm-adjusted training p-value: 0.07464.
- Promotion-gate variants: 0/224.

The frozen promotion gate remains unchanged: validity >= 50/63, sufficient training/validation sample sizes, positive training and validation means, and Holm-adjusted training p < 0.05.

## Scientific conclusion

Phase 21W resolves the historical-data availability gap but **does not produce a capital-phase candidate** under the preregistered frozen protocol. Positive holdout outcomes exist for many variants, but no configuration satisfies the complete promotion gate after 224-way Holm adjustment.

No live-trading profitability claim is established. Historical OHLC reconstruction, explicit slippage, and transaction-cost assumptions remain important execution-model limitations.

## Canonical outputs

- [Final manuscript](FINAL_MANUSCRIPT.md)
- [Final results summary](RESULTS.md)
- [Final validation summary](output/final_validation_summary.json)
- [Complete 224-variant summary](output/final_rerun/variant_summary.json)
- [RISSIN source manifest](output/rissin_source_manifest.json)
- [Error log](ERROR_LOG.md)
