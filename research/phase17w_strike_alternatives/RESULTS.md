# Phase 17W — K1/K2/K3 Strike-Definition Alternatives: Results

## Execution
- Workflow run: 36626050986
- Registered family: 224 configurations = 8 K1 rules × 4 K2 rules × 7 K3 multipliers.
- Frozen control: OTM1_NEXT1_K3M2.
- Baseline calendar: 63 usable weekly cycles.
- Chronological split: 60% / 20% / 20% of the fixed calendar (37 / 12 / 14 baseline cycles); variant-level usable trades can be fewer because alternative strike definitions may be incomplete.
- Slippage: 0.50 NIFTY index points per leg.
- Stop: 50 NIFTY points, frozen from prior training-only selection.
- Costs: existing Phase 11 Paytm Money/NSE cost model.
- Execution model: OHLC reconstruction; no historical BBO substitution.
- Holdout: not used for selection.

## Gate outcome

**No variant was promoted to Phase 16W capital/margin validation.**

The implemented promotion gate required:
1. valid rate >= 50/63;
2. training n >= 30 and positive training mean;
3. validation n >= 8 and positive validation mean;
4. training centered block-bootstrap p < 0.05 after Holm adjustment across all 224 variants.

The complete 224-variant run produced **0 promotable variants**. No alternative was therefore used to alter the frozen strategy or the locked Phase 13 holdout.

## Coverage and statistical observations

- All 224 registered variants were evaluated and audited.
- The aggregate contained 8,736 trade records.
- No variant reached the >=50/63 valid-rate gate. The maximum usable count was 39/63.
- 192/224 variants had positive training mean net P&L.
- 136/224 had positive validation mean net P&L.
- 136/224 had positive means in both training and validation.
- 0/224 passed the Holm-adjusted training significance threshold.
- Because the alternative strike rules reduce the number of fully reconstructible cycles for many configurations, the coverage gate is a material part of the preregistered decision rule rather than a post-hoc exclusion.

### Frozen control within Phase 17W

The control OTM1_NEXT1_K3M2 reconstructed:
- training: n=23, mean ₹4,655.83/cycle;
- validation: n=7, mean -₹467.77/cycle;
- holdout: n=9, mean ₹885.995/cycle;
- all three segments together: 39 usable cycles;
- training bootstrap p=0.000333; Holm-adjusted p=0.07464;
- promotion: false.

These Phase 17W control statistics are descriptive and are not a replacement for the locked Phase 13 evidence.

## Interpretation

The experiment does not provide evidence that any of the registered K1/K2/K3 alternatives satisfies the full promotion criteria under the frozen weekly OHLC reconstruction. In particular, the coverage requirement and multiple-testing correction prevent selection based only on favorable point estimates.

The absence of a promoted alternative does **not** prove that every alternative is unprofitable in live trading. It means that none met the preregistered evidence threshold on this dataset and execution model.

## Data provenance

The complete machine-readable result artifact was produced by workflow run 36626050986:
- `variant_summary.json` — all 224 variant summaries and gate flags.
- `variant_registry.json` — registered family.
- `baseline_calendar.json` — frozen 63-cycle calendar.
- `all_variant_trades.csv` — 8,736 reconstructed trade rows.

Workflow artifact ID: 11060372488. The artifact is retained by GitHub Actions for the configured retention period.

## Phase disposition

Phase 17W is closed. No second optimization loop is authorized. The Phase 13 holdout remains locked. Downstream work should focus on the pre-existing capital/margin and execution-data limitations rather than further strike-parameter tuning.
