# Phase 21W Status

State: COMPLETE — exact frozen 224-variant rerun executed on the admitted 82.93% executable-cell sample; no configuration passed the preregistered promotion gate. External full-strike recovery remains the next data-recovery phase.

Frozen design:
- 224 variants = 8 K1 × 4 K2 × 7 K3 multipliers.
- 63 chronological weekly expiries; train/validation/holdout = 37/12/14.
- 10:00 IST entry; 14:00 IST lock.
- 50-point hard stop; 0.50-point slippage per leg.
- Existing Paytm Money/NSE transaction-cost model.
- Block bootstrap length 3,000 reps with Holm multiple-testing adjustment.
- No synthetic bars, strike substitution, or cross-source leg mixing.

Data coverage:
- Combined admitted variant-cycle cells: 11,702 / 14,112 (82.93%).
- HF-03 cells: 8,064.
- HF-02 recovered cells: 3,638.
- Covered expiries: 58/63.
- Completely missing expiries: 5 — 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13, 2026-05-12.
- Source overlap: 0.
- Source-local duplicate groups: 0.
- Full combined option parquet is 346.32 MB and is retained in the successful workflow artifact rather than Git.

Empirical result:
- Variants evaluated: 224.
- Variants satisfying coverage >= 50/63: 168.
- Positive training mean: 193.
- Positive validation mean: 136.
- Positive holdout mean: 185.
- Positive means in training + validation + holdout with coverage >= 50/63: 106.
- Variants meeting all non-Holm promotion components: 107.
- Holm-adjusted training p < 0.05: 0.
- Variants promoted to capital phase: 0.

The exact backtest is reproducible and auditable for the current admitted sample, but the five missing expiries and lack of historical bid/ask execution data remain material limitations.

Next phase: Phase 21W External Full-Strike Source Recovery.