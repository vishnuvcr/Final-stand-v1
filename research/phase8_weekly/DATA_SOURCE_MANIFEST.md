# Phase 8W — Weekly Data Source Manifest

## New data objective

The prior pilot requirement of 20 monthly expiries is discarded.

The weekly experiment requires enough weekly cycles to estimate distributions, regimes and tail events. The pilot target is:

**At least 52 weekly NIFTY expiries**, with a preferred research sample of 104+ weekly expiries if historical quote quality permits.

The sample must include:
- low, medium and high volatility states;
- major market drawdowns and rallies;
- pre- and post-contract-rule changes;
- ordinary and event-heavy weeks;
- both favorable and adverse upside moves through far OTM calls.

## Minimum weekly fields

For each weekly expiry cycle:
- prior expiry date;
- target weekly expiry date;
- entry timestamp;
- lock timestamp;
- exit timestamp;
- NIFTY spot;
- K1/K2/K3;
- bid/ask and quantities for all active legs;
- LTP;
- volume;
- OI;
- IV if available;
- lot size effective for the contract;
- margin requirement;
- source and checksum;
- quote-age indicator;
- data-quality flag.

## Weekly data-quality gate

Pass only if pilot data can demonstrate:
- >=95% usable K1/K2/K3 entry quote pairs;
- >=95% usable K2 lock quotes;
- >=95% usable K1/K3 lock marks;
- <0.1% contract-mapping errors;
- no look-ahead;
- reproducible transformation and source manifests.

## Historical-rule rule

NIFTY weekly expiry specifications are date-dependent. Current NSE documentation says weekly contracts expire every Tuesday, or the previous trading day if Tuesday is a holiday, and currently provides four weekly contracts excluding monthly contracts. Historical periods must be joined to the effective exchange rules for that period. citeturn642743search0turn642743search1

## Hugging Face data admission
Primary source: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

Secondary cross-check: https://huggingface.co/datasets/rissin/nse-options-intraday

Secondary IV/spot diagnostics: https://huggingface.co/datasets/artist-23/nifty-options-data

The primary source has expiry-partitioned 1-minute NIFTY option data and a separate NIFTY index file. The documented option schema contains OHLC, volume and open interest, but not historical bid/ask. Therefore the pilot must label all P&L as OHLC-reconstruction research until a true quote source is admitted.

Large third-party source files remain in Hugging Face/Actions cache rather than being redistributed into the public repository. Source revisions and SHA-256 hashes are committed in the Phase 9 output metadata.

## Critical weekly execution issue

Because the strategy is now repeated every week, turnover and friction become structurally larger. The study therefore reports:
- gross P&L;
- brokerage;
- taxes/fees;
- spread cost;
- slippage;
- total cost;
- net P&L;
- net P&L per week;
- net P&L / peak margin.

No midpoint-only profitability statistic is acceptable as the primary result.
