# Phase 15W Research Plan — Execution and Capital Validation Data

## Research question
Can the frozen weekly NIFTY strategy be evaluated with historically observed option quotes and historically appropriate capital constraints without changing any strategy parameters or contaminating the untouched holdout?

## Phase gates
1. Source discovery — identify public and paid candidates.
2. Schema qualification — verify timestamps, contract identifiers, bid/ask and quantities.
3. Coverage qualification — map candidate dates/contracts to all eligible weekly cycles.
4. Licensing/access qualification — distinguish public samples from usable historical archives.
5. Execution model — construct quote-based fills and conservative fallback rules.
6. Capital model — reconstruct dated SPAN/peak-margin requirements where possible.
7. Frozen rerun — run the exact Phase 13 strategy without parameter tuning.
8. Holdout integrity audit — verify the holdout remains untouched and unselected.
9. Statistical comparison — compare OHLC reconstruction versus quote-based execution.
10. Manuscript update — document results, limitations and whether the evidence supports executable-performance claims.

## Stopping rule
Stop after these gates. Do not open a new parameter-optimization loop. If no free qualifying archive is found, document that outcome and quantify the minimum legitimate paid dataset required.

## Required outputs
- Source qualification matrix
- Data-access and licensing record
- Quote schema validation report
- Coverage report against the 63-cycle manifest
- Quote-based execution dataset or documented data-gap result
- Historical margin dataset or documented margin-gap result
- Frozen rerun results
- Updated manuscript and supplementary material
- Error and research logs