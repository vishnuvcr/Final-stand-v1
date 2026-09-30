# Phase 22W Execution Workflow

## Manual entry
This workflow will have a manual `workflow_dispatch` entry point.

## Gates
1. Verify phase branch and frozen registry.
2. Audit/verify admitted execution-data cache.
3. Verify exact schema and provenance.
4. Run execution-data contract tests.
5. Run the complete 224 configurations without changing rules.
6. Apply the frozen chronological split.
7. Apply executable bid/ask fills and all registered costs.
8. Run statistical tests and Holm correction.
9. Publish results, coverage, source manifest, error log and manuscript.
10. Refuse promotion when any hard gate fails.

## Data handling
- Cache immutable source artifacts.
- Do not redownload admitted data on every run.
- Record SHA-256 hashes.
- Never synthesize missing quotes.
