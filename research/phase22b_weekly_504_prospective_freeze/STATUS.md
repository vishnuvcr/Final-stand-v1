# Phase 22B Status

State: **VALIDATION COMPLETE — prospective statistical confirmation pending additional qualifying weekly cycles**

## Freeze gate
- 504-configuration family frozen: PASS
- Weekly protocol frozen: PASS
- New-period holdout opened only after freeze: PASS
- Post-hoc configuration selection: prohibited

## Validation result
- Authoritative extension run: **36763880416 — SUCCESS**
- Commit that changed the prospective boundary: **045a2da46307603fe7d0bdf04d12e74285545ee5**
- Frozen family size: **504**
- Requested prospective boundary: **2026-09-08**
- Qualifying weekly expiries admitted: **8**, ending **2026-07-21**
- Expected variant-cycle rows: **4,032**
- Usable variant-cycle rows: **4,032**
- All 504 variants present: **yes**
- Positive total net P&L: **376/504**
- Completed observations per variant: **n=6**
- Bootstrap/Holm inference: **not computed**, because the frozen bootstrap requires at least 8 observations per configuration
- Capital-promotion gate: **not reached**; minimum remains 30 completed cycles
- Configuration promoted/selected: **none**

## Data interpretation
The September 8 date extension did not add qualifying weekly option cycles. The limitation is source coverage, not a strategy or statistical-rule change. The primary RISSIN source supplied the admitted cycles; the successful run recorded no TradeMarkk option-fallback expiries.

## External source review
- The TradeMarkk NIFTY option tree currently lists 2026-08-04 as its latest NIFTY option file; its documentation states that option coverage is partial.
- The codepyx23 Hugging Face dataset/bucket is a duplicate/mirror of TradeMarkk, so it is not independent evidence.
- NSE publishes historical contract-wise derivatives reports and historical order/trade specifications, but the public historical-report pages do not provide a ready free 1-minute expired-option archive equivalent to the required backtest input.
- A commercial archive advertises NIFTY 1-minute full-chain coverage through September 2026, including OHLC, volume and OI. It has no bid/ask/order-book fields and requires purchase; it is therefore recorded as a **candidate source**, not silently substituted into the study.

## Interpretation boundary
The 376/504 positive count is descriptive only. It is not evidence of robustness, statistical significance, or a configuration choice. Historical Phase 22A and prospective Phase 22B remain separate evidence streams.

## Next gate
Before another prospective rerun, continue source-recovery work using approved public/free sources first. If no qualifying free source can provide the missing weekly cycles, record the limitation and separately evaluate whether the paid archive is admissible under the project's data-acquisition rules. Do not change the strategy family or statistical gates to compensate for missing data.
