# Phase 9W — Hugging Face Weekly Data Gate Status

## Branch
phase-9w-hf-data-gate

## State
Ready for workflow execution; empirical gate not yet run in this session.

## Implemented

- Primary source: thetrademarkk/india-index-options-1m.
- Secondary 2025 cross-check: rissin/nse-options-intraday.
- Diagnostic source retained: artist-23/nifty-options-data.
- HF_TOKEN wired through GitHub Actions secrets.
- Hugging Face cache enabled with a stable cache key.
- Source revision, file size and SHA-256 captured.
- Monthly expiries excluded from the weekly experimental universe.
- Prior weekly expiry is resolved from the full weekly catalog, not from the selected window boundary.
- 10:00 entry price proxy uses bar open rather than close to avoid intrabar look-ahead.
- Selected entry and lock bars require positive traded volume.
- K1/K2/K3 entry prices and K1/K2/K3 lock prices are written to the cycle manifest.
- Historical expiry regime is recorded as Thursday-era through August 28, 2025 and Tuesday-era after that boundary.
- Independent 2025 source cross-check compares selected strike prices at entry and lock where available.
- Raw third-party Parquet is kept in the HF/Actions cache rather than copied into the public repository.

## Data-quality gate

Pass criteria remain:
- >=52 weekly expiry cycles;
- >=95% entry K1/K2/K3 coverage;
- >=95% lock K1/K2/K3 coverage;
- no duplicate target expiries;
- prior weekly expiry strictly precedes target;
- independent source cross-check match rate >=80%;
- no unresolved calendar or leakage issue.

## Important limitation

The primary HF source is 1-minute OHLC, not a historical order-book bid/ask feed. Therefore a Phase 9 pass is a validated OHLC reconstruction gate, not a claim of historical bid/ask execution fidelity.

## Blocking point

The available GitHub toolset does not expose workflow-dispatch execution, so this session has created and verified the manual workflow but has not fabricated a Phase 9 run result.