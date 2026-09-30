# Phase 22A Appendices and Supplementary Material

## Appendix A — Configuration registry

The complete configuration family is:

- K1: OTM1–OTM8, ATM_NEAREST, ATM_UP, ITM1–ITM8
- K2: NEXT1, NEXT2, NEXT3, MIRROR_GAP
- K3: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0

Total = 18 × 4 × 7 = 504.

The machine-readable registry is:
output/variant_registry.json

## Appendix B — Weekly protocol

Entry:
10:00 IST on the first trading day after the prior weekly expiry.

Lock/exit decision:
14:00 IST on the trading day before the target weekly expiry.

Residual exposure:
May continue to target expiry unless terminated by the frozen stop/exit rules.

Hard stop:
50 NIFTY points.

Slippage:
0.50 NIFTY index points per leg.

Transaction costs:
Registered Paytm Money/NSE model used by the frozen research engine.

## Appendix C — Statistical procedure

Per configuration:

- training/validation/historical-holdout net P&L;
- win rate;
- maximum drawdown;
- 95% expected shortfall;
- annualized weekly Sharpe;
- mean cost;
- valid-cycle rate;
- centered training bootstrap p-value.

Multiplicity:
One Holm correction across all 504 configuration-level training tests.

Capital-promotion gate:
Unchanged from the registered engine. No configuration passed.

## Appendix D — Data provenance

Historical base:
Frozen Phase-21 63-expiry recovery interface.

Original-source expiries:
58 weekly expiries from the original historical option source, with SHA-256 values inherited from the frozen Phase-21 manifest.

Recovered expiries:
2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13 and 2026-05-12.

Recovered source:
RISSIN, revision 8f7739cab3f38abdcbc6332a6d0a83e1341326e3.

Recovered file:
upstox_intraday/NIFTY/NIFTY_2026.parquet.

Recovered-file SHA-256:
bae9943b2fa99ee9c1214fb7c695b84f9f661a050a5cd04d9c5c2ffc7bc59f73.

The option source does not provide historical bid/ask/depth, so fills remain OHLC reconstructions.

## Appendix E — Workflow reproducibility

Workflow:
.github/workflows/phase-22a-weekly-504-strike-expansion.yml

Run:
36741881293

Artifact:
phase22a-weekly-504-results

Artifact ID:
11111230842

Artifact digest:
sha256:1a250f5ca0a39aaefb3b293758eedc41293387e720cf65491e720a5cdb243964

The final workflow verified:

- exactly 504 variant IDs;
- exactly 63 baseline weekly cycles;
- 100% configuration-level validity;
- zero capital-promotion passes.

## Appendix F — Error corrections applied before interpretation

E22A-001:
504-family multiple-testing correction required.

E22A-002:
Weekly-horizon wording standardized.

E22A-003:
Historical holdout not relabeled as new unseen evidence.

E22A-004:
K1 selection generalized from ranks 1–3 to ranks 1–8.

E22A-005:
Phase-9 interface sourced from the frozen combined branch rather than an incomplete workflow artifact.

E22A-006:
TheTrademarkk and RISSIN revisions separated and pinned by source.

E22A-007:
Per-variant OHLC bar replication removed.

E22A-008:
RISSIN duplicate identity expanded to include expiry.

E22A-009 to E22A-011:
IST timestamp comparisons made explicit across source filters and entry selection.

Full descriptions are in ERROR_LOG.md.

## Supplement S1 — Complete row-level results

output/ALL_504_CONFIG_RESULTS.csv

## Supplement S2 — Compact row-level results

output/ALL_504_CONFIG_RESULTS_COMPACT.csv

## Supplement S3 — Parameter surfaces

output/K1_SURFACE_MEAN_HOLDOUT.csv
output/K2_SURFACE_MEAN_HOLDOUT.csv
output/K3_SURFACE_MEAN_HOLDOUT.csv

## Supplement S4 — Static figures

charts/K1_MEAN_HOLDOUT_PNL.svg
charts/K2_MEAN_HOLDOUT_PNL.svg
charts/K3_MEAN_HOLDOUT_PNL.svg
charts/HOLDOUT_PNL_QUANTILES.svg

## Supplement S5 — Audit and manuscript files

RESULTS.md
PARAMETER_SURFACE_ANALYSIS.md
FINAL_MANUSCRIPT.md
RESEARCH_LOG.md
ERROR_LOG.md
