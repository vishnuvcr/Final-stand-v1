# Phase 21W Final Recovery Targets

The combined frozen rerun has executable coverage for 58 of the frozen 63 weekly expiries. The following five holdout expiries are the only remaining target dates.

| target expiry | split | current status | external candidate |
|---|---|---|---|
| 2026-01-13 | holdout | missing | RISSIN HF NIFTY 1-minute |
| 2026-02-10 | holdout | missing | RISSIN HF NIFTY 1-minute |
| 2026-03-10 | holdout | missing | RISSIN HF NIFTY 1-minute |
| 2026-04-13 | holdout | missing | RISSIN HF NIFTY 1-minute |
| 2026-05-12 | holdout | missing | RISSIN HF NIFTY 1-minute |

## Admission contract

A recovered expiry is admitted only when the same external source supplies, for every one of the 224 registered variants:

1. the exact frozen 10:00 IST entry bar for all three selected CE strikes;
2. every required 1-minute OHLC bar from entry through the frozen 14:00 IST lock and the subsequent stop/expiry path;
3. the exact 14:00 IST lock bar for the required strikes;
4. valid expiry/strike/option-type identity;
5. positive-volume entry observations where the frozen strike-selection algorithm requires them.

No synthetic bars, interpolation, cross-source leg mixing, strike substitution or manual prices are allowed.

## Provenance

Candidate source: rissin/nse-options-intraday on Hugging Face.

Pinned dataset revision: 78b1c5468255d18cf492984bfe6fe4e3ac874d7c.

The dataset card states that its upstox_intraday track contains NIFTY 1-minute data from October 2024 through 2026, with expiry, strike, option type, OHLC and volume fields. It also states that intraday OI is unavailable from the upstream Upstox API. OI is therefore not an admission requirement for this price-path backtest.

The large source parquet must remain a workflow/cache artifact and must not be committed to Git. Compact provenance, coverage and validation summaries belong in this phase directory.
