# Phase 16W — Capital and Margin Validation

## State
Active — initialization.

## Starting conditions
- Phase 15W free historical-BBO discovery is closed without a qualifying archive.
- Frozen strategy remains the Phase 13W configuration.
- Untouched 14-cycle holdout remains locked.
- No commercial quote dataset has been purchased.
- Historical BBO limitation is carried forward explicitly.

## Current gate
CAPITAL/MARGIN DATA: STATIC HISTORICAL SPAN ROUTE EXHAUSTED — 0/63 CYCLES

## Planned work
1. Inventory official NSE F&O SPAN/risk-parameter and margin-report routes.
2. Build a date/contract coverage manifest for the 63-cycle study.
3. Acquire/cache legally usable historical files or record reproducible retrieval metadata.
4. Parse and map margin inputs to the frozen position path.
5. Calculate peak capital requirements and capital-normalized diagnostics.
6. Run deterministic validation checks and manual GitHub Actions workflow.
7. Update manuscript/supplement with capital results and remaining execution-data limitations.

## Constraints
- No parameter tuning.
- No holdout selection.
- No OHLC substitution for historical BBO.
- No fabricated or inferred margin observations.
## Final execution
- Run 36627668048 succeeded on the acquisition/probe stage.
- 18 candidate static NSE SPAN URLs (6 patterns × 3 years: 2024–2026) returned HTTP 404.
- 193 unique required trading dates were identified from the frozen cycle interface; 0 dated SPAN members were recovered.
- Result: 0/63 cycles with empirical historical SPAN coverage.
- Phase closed under the preregistered stopping rule; no tuning and no holdout selection.
