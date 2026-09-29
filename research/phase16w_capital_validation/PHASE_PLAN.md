# Phase 16W Research Plan — Capital and Margin Validation

## Purpose
Validate the capital and margin assumptions of the frozen weekly NIFTY strategy using official NSE historical risk-parameter/report infrastructure where accessible, without changing any strategy parameter or touching the locked holdout for selection.

## Research questions
1. What dated NSE SPAN/risk parameters and margin-report information can be reconstructed for the 63 historical weekly cycles?
2. What is the minimum and peak capital requirement implied by the frozen position path?
3. How do historical margin requirements affect return-on-capital, drawdown-on-capital, and capital efficiency?
4. Which components remain unobservable because client/broker-specific margin reports are not public?

## Scope
- Frozen Phase 13W strategy only.
- Frozen 0.50 index-point per-leg slippage and 50-point hard stop.
- No strike, stop, entry, exit, target, or sizing optimization.
- Untouched 14-cycle holdout remains locked and is never used for parameter selection.
- Historical BBO remains unavailable from a free qualifying archive; no OHLC-to-BBO substitution will be made.

## Method
### A. Data acquisition
- Use official NSE historical F&O report infrastructure and SPAN risk-parameter files where accessible.
- Cache every admitted source with date, source URL, retrieval timestamp, checksum and schema metadata.
- Prefer begin-of-day and intraday/end-of-day SPAN files appropriate to the strategy timestamps.
- Retain raw source files only where redistribution/licensing permits; otherwise cache metadata/checksums and reproducible retrieval instructions.

### B. Contract mapping
- Map each strategy contract to the dated NSE contract/risk record using symbol, expiry, strike and option type.
- Reject ambiguous or missing mappings.
- Record whether the position is long/short and the time at which margin is evaluated.

### C. Capital model
For each cycle and timestamp, estimate:
- premium cash debit/credit;
- SPAN requirement;
- extreme-loss/exposure component where documented;
- net option value / premium margin where applicable;
- total estimated upfront requirement;
- peak intracycle requirement;
- capital utilization and capital-normalized P&L.

Client/broker-specific add-ons are kept as separate assumptions rather than silently embedded.

### D. Sensitivity
Report capital-normalized results under clearly labelled assumptions:
1. exchange-level reconstructed requirement;
2. exchange requirement plus conservative broker buffer;
3. quote-execution gap scenarios already registered in Phase 12.

No scenario is used to retune the strategy.

### E. Statistical analysis
- Distribution of peak capital requirement.
- Median, mean, P95 and maximum capital requirement.
- P&L / peak-capital ratios by cycle.
- Drawdown measured in rupees and as a fraction of required capital.
- Bootstrap confidence intervals for capital-normalized weekly P&L where sample size permits.
- Separate descriptive reporting for training/validation/untouched holdout.

## Acceptance criteria
Phase 16W passes when:
- dated margin/risk inputs are traceable;
- all admitted inputs have contract/date mappings;
- capital requirements are reproducible from cached metadata/source files;
- no holdout leakage occurs;
- capital-normalized results are explicitly distinguished from the earlier rupee-P&L results.

If historical SPAN coverage cannot be reconstructed fully, the phase still closes with a quantified margin-data gap rather than inventing capital requirements.

## Outputs
- STATUS.md
- source/caching manifest
- margin schema and mapping report
- capital reconstruction dataset/results
- statistical summary
- error/research log updates
- manuscript supplement/update
- manual GitHub Actions workflow

## Stopping rule
Stop after the capital/margin reconstruction and documented sensitivity analysis. Do not create another optimization loop.