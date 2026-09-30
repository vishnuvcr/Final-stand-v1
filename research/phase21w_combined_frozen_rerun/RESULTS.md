# Phase 21W — Combined Frozen Rerun Results

## Research scope
The frozen 224-configuration weekly NIFTY experiment was rerun after deterministic source recovery. Source precedence was HF-03 first and admitted HF-02 recovery second. No cross-source blending within a variant-cycle was allowed.

### Coverage
| Measure | Result |
|---|---:|
| Frozen variant-cycle cells | 14,112 |
| Admitted combined cells | 11,702 |
| Coverage | 82.93% |
| Covered expiries | 58 / 63 |
| Completely missing expiries | 5 |
| Source overlap | 0 |
| Source-local duplicate groups | 0 |

Missing expiries: 2026-01-13, 2026-02-10, 2026-03-10, 2026-04-13, 2026-05-12.

## Gate counts across 224 variants
| Criterion | Count |
|---|---:|
| Coverage >= 50/63 | 168 |
| Training n >= 30 | 168 |
| Positive training mean | 193 |
| Validation n >= 8 | 168 |
| Positive validation mean | 136 |
| Positive holdout mean | 185 |
| Positive train + validation + holdout and coverage >= 50/63 | 106 |
| All non-Holm promotion components | 107 |
| Holm-adjusted training p < 0.05 | 0 |
| Promoted to capital phase | 0 |

## Distribution across tested variants
Mean of the per-variant mean net P&L values:
- Training: ₹2,687.73/cycle.
- Validation: ₹458.86/cycle.
- Holdout: ₹2,610.84/cycle.

Observed range of per-variant mean net P&L:
- Training: -₹9,235.88 to ₹12,059.05/cycle.
- Validation: -₹7,136.81 to ₹7,882.21/cycle.
- Holdout: -₹5,049.02 to ₹13,182.05/cycle.

These are descriptive grid statistics over an incomplete sample; they are not a claim that the highest observed configuration is intrinsically superior.

## K3 sensitivity (descriptive)
| K3 multiplier | Training | Validation | Holdout | All 3 positive |
|---:|---:|---:|---:|---:|
| 0.5 | -₹2,682.76 | -₹2,706.02 | -₹1,364.90 | 0 |
| 1.0 | ₹1,215.64 | -₹1,435.03 | ₹454.22 | 6 |
| 1.5 | ₹2,538.47 | -₹194.60 | ₹1,465.50 | 15 |
| 2.0 | ₹3,518.08 | ₹729.07 | ₹2,736.50 | 21 |
| 2.5 | ₹4,120.91 | ₹1,580.82 | ₹3,797.21 | 31 |
| 3.0 | ₹4,658.91 | ₹2,197.01 | ₹4,919.80 | 31 |
| 4.0 | ₹5,444.88 | ₹3,040.76 | ₹6,267.52 | 31 |

The K3 table is descriptive and should not be interpreted as causal because the sample is incomplete and multiple configurations were tested.

## Interpretation
Under the preregistered gate, no configuration qualified for capital promotion. The statistical blocker is multiplicity-adjusted training evidence: every variant's Holm-adjusted training p-value was at least 0.0746418.

The incomplete historical executable sample is also material: five weekly expiries have no admitted full-strike observations in the current combined source set.

The data are OHLC-based rather than historical bid/ask, so this is a historical price-reconstruction study rather than verified executable-fill research.

## Reproducibility
- Machine-readable per-variant output: output/variant_summary.json.
- Compact combined-cycle manifest: combined_input/variant_cycle_manifest.csv.
- Coverage record: combined_input/coverage.json.
- Full combined option parquet: successful workflow artifact phase21w-combined-frozen-results.