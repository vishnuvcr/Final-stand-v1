# Research Log

## 2026-09-29 — Major strategy reset to weekly trading
- User instructed that the monthly-expiry strategy research be restarted using weekly expiries and weekly trading.
- Re-read the current repository research-state files before modifying the research design.
- Created new branch `phase-8-weekly-expiry-restart` from main so the monthly research remains auditable but is no longer the active experiment.
- Verified current NSE NIFTY option specifications: four weekly expiry contracts excluding monthly contracts; weekly expiry every Tuesday; prior trading day if Tuesday is a holiday; new serial weekly contract after expiry. citeturn642743search0turn642743search1
- Redefined the experimental unit as one complete weekly expiry cycle.
- Froze a primary operational cycle: entry on the first trading session after expiry at 10:00 IST, lock on the preceding trading day at 14:00 IST, and predefined exit before expiry settlement.
- Replaced the monthly research questions and data requirements with weekly-specific versions.
- Increased the pilot data requirement from monthly expiries to at least 52 weekly expiry cycles, preferably 104+ if quote quality permits.
- Explicitly elevated weekly turnover and transaction costs to primary endpoints.
- Current status: weekly design gate PASSED; historical weekly quote-data gate PENDING.


## 2026-09-29 — Weekly reset completion
- Created the weekly literature review and fresh weekly master research plan.
- Confirmed the monthly research plan is not copied into the active weekly branch.
- Added branch-local status and error logging.
- Weekly branch status remains design gate passed / data gate pending.


## 2026-09-29 — Weekly data and mechanics gate
- Official NSE sources were audited. NSE provides historical F&O framework, daily contract-wise price/volume data, daily reports, SPAN risk-parameter files and margin-report infrastructure. citeturn0search31turn0search6turn6search0turn6search5
- Public GitHub research repositories demonstrate that 1-minute NIFTY weekly option datasets exist, including a pipeline covering 39 Tuesday-expiry weeks from Sep 2025 to May 2026 and other datasets covering weekly options. These sources are useful for data discovery/prototyping but are not treated as authoritative execution data without source/licence/quote-quality validation. citeturn2search1turn2search2
- The empirical gate remains blocked because the final study requires point-in-time bid/ask or sufficiently conservative executable-price reconstruction for K1/K2/K3 at entry and K2/K1/K3 at lock.
- Implemented deterministic weekly mechanics engine and local unit checks.
- Implemented dated brokerage/statutory/slippage/margin framework.
- Paytm Money currently states ₹10 brokerage per unique executed F&O order. citeturn6search8
- NSE's SPAN documentation confirms portfolio-based scenario margining and daily risk-parameter files; exact historical margin requires the relevant dated files. citeturn6search3turn6search1
- Phase status: 9W blocked pending qualified intraday data; 10W active and mechanics framework implemented.


## 2026-09-29 — Phase 9W Hugging Face data gate started
- User supplied an HF_TOKEN repository secret for faster Hugging Face downloads.
- Searched Hugging Face for NIFTY weekly option history suitable for the frozen weekly strategy.
- Identified thetrademarkk/india-index-options-1m as the primary candidate: 1-minute NIFTY option data partitioned by expiry plus a separate 1-minute NIFTY index file. The documented schema provides OHLC, volume and open interest, but no historical bid/ask. https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- Identified rissin/nse-options-intraday as an independent 1-minute OHLC cross-check from October 2024 onward. https://huggingface.co/datasets/rissin/nse-options-intraday
- Identified artist-23/nifty-options-data as a secondary IV/spot/strike diagnostic source through December 2025. https://huggingface.co/datasets/artist-23/nifty-options-data
- Created branch phase-9w-hf-data-gate, preserving phase separation.
- Added a manual GitHub Actions workflow that consumes the HF_TOKEN secret, caches the Hugging Face downloads, records the resolved dataset revision and SHA-256 hashes, and produces a weekly cycle manifest plus selected option bars.
- The raw third-party data are intentionally not copied into the public repository by default because the primary dataset is published under CC-BY-NC-4.0 and the secondary dataset has its own redistribution terms.
- Corrected the ingestion logic so the first selected expiry uses the preceding expiry from the full source catalog rather than incorrectly treating the pilot window as if it began at the first observed cycle.
- Phase status: 9W active; empirical profitability remains untested.

## 2026-09-29 — Phase 10W analytical mechanics result
- A non-empirical Black–Scholes stress illustration was performed to examine weekly target-strike discreteness.
- The key diagnostic added is target error: |actual K3 premium - target premium| / target premium.
- The analysis shows that the exact 2× premium-difference target can be materially unattainable on a discrete weekly strike grid, especially close to expiry.
- This does not establish profitability or unprofitability; it establishes a measurement requirement.
- The weekly pre-lock position remains a bull call ladder with theoretically unbounded upside loss; the K2 lock transforms it into a bounded-risk K1/K3 bull call spread.
- Phase 10W mechanics and cost/margin framework are implemented.
- Phase 9W empirical data remains blocked pending qualified intraday historical quote data.
- No live-trading conclusion has been authorized.


## 2026-09-29 — Phase 9W calendar, execution and cross-check hardening
- Added an expiry-calendar control that excludes the latest expiry in each calendar month from the weekly sample, treating it as the monthly contract.
- Reconciled the historical NIFTY weekly expiry-day regime to NSE circulars: Thursday-era through August 28, 2025 and Tuesday-era after the changeover. The earlier March Monday proposal is treated as superseded by the later June circular.
- Removed intrabar look-ahead from 10:00 strike selection by using the 10:00 bar open rather than its close.
- Added positive-volume filters at entry and lock.
- Added explicit K1/K2/K3 lock-time price fields to the weekly cycle manifest.
- Added an independent 2025 Hugging Face cross-check against rissin/nse-options-intraday for selected entry and lock observations.
- Added data attribution and redistribution notes and kept third-party raw files out of the public repository.
- Hardened the GitHub Actions cache key and download timeout settings for the HF workflow.
- Current result: Phase 9W is ready for execution, but no empirical pass/fail result has been claimed because the workflow has not been executed in the available tool environment.


## 2026-09-29 — Phase 11W backtest pipeline
- Created separate branch phase-11w-weekly-backtest.
- Added a cost-adjusted OHLC-reconstruction backtest consuming the Phase 9 cycle manifest, selected option bars and NIFTY spot path.
- Included explicit slippage, Paytm Money brokerage parameterization, lot-size transition and stop-loss sensitivity.
- Added manual and push-triggered workflow execution.
- No result has been admitted because upstream Phase 9 empirical data execution has not yet been observed.

## 2026-09-29 — Phase 12W robustness pipeline
- Created separate branch phase-12w-robustness.
- Added chronological train/validation/test analysis, weekly block bootstrap, Sharpe, drawdown and expected shortfall.
- Added 30-cell stop/slippage stress grid.
- Added manual and push-triggered workflow execution.
- Robustness conclusions remain blocked until Phase 11 produces admissible trade results.

## 2026-09-29 — Phase 11/12 cost and settlement hardening
- Re-read the active branch status, research log and error log before changes.
- Verified with current NSE documentation that NIFTY index options are cash-settled using the closing value of the underlying index on the last trading day. citeturn9search0turn1search1
- Identified and corrected the Phase 11 expiry-path bug: the selected NIFTY spot file already extended through expiry, but the backtest had been returning the lock timestamp as the expiry exit timestamp.
- Corrected option transaction-cost modelling: NSE option transaction charges are 0.0495% before 01-Oct-2024 and 0.03503% thereafter; STT is 0.0625% before 01-Oct-2024, 0.10% through 31-Mar-2026, and 0.15% from 01-Apr-2026. citeturn5search3turn3search10
- Updated SEBI turnover fee to the currently documented 0.0001% and added the published option IPFT rate proxy of 0.000005% to the cost model. citeturn7search0turn5search5
- Paytm Money currently states ₹10 brokerage per unique executed F&O order; the model retains this broker-specific input. citeturn2search0
- Phase 12 now explicitly states that rupee P&L is not a return-on-capital measure until historical SPAN/peak-margin series are integrated.
- No profitability conclusion was admitted.

## 2026-09-29 — Phase 12 robustness execution resumed and completed
- Re-read the active plan, Phase 12 status, research log and error log before proceeding from the user's resume instruction.
- Observed Phase 12 run 81 complete successfully after the workflow gate simplification. The 30-cell slippage x stop-loss grid produced 30 non-empty candidate ledgers with 63 weekly trades per cell.
- Canonical run 81 artifact: `phase-12w-robustness-81` (GitHub Actions artifact id 11051125242). The stress matrix includes slippage 0, 0.25, 0.50, 1.00 and 2.00 index points per leg and stop-loss none, 50, 100, 150 and 200 and 300 points.
- At the frozen Phase 13 cell (0.50-point slippage per leg, 50-point stop), the 63-cycle full-sample mean net P&L was ₹3,488.06 per weekly cycle, while the chronological 14-cycle test segment mean was ₹1,566.04. These are OHLC-reconstruction results, not return-on-capital metrics.
- The Phase 13 frozen rule was selected on training data only and independently produced 37 training cycles, 12 validation cycles and 14 holdout cycles. The observed holdout was not used to select the stop.
- Identified a protocol gap: the existing Phase 12 implementation covered chronological split, block bootstrap, Sharpe, drawdown, expected shortfall and the 30-cell stress grid, but the written Phase 12 plan also calls for CSCV/PBO, DSR, multiple-testing correction, regime conditioning, tail-gap stress and margin stress. A supplemental audit was therefore added without changing the frozen rule.
- Added `research/phase12_weekly/robustness_supplement.py` and deterministic tests for CSCV-style PBO, Holm multiple-testing adjustment, a DSR-style non-normality/multiple-testing diagnostic, structural regime conditioning, and an additional stop-gap stress overlay.
- Added workflow serialization so duplicate Phase 12 runs do not race on repository pushes.
- Literature check for the supplemental methods used the published PBO/CSCV and DSR papers by Bailey et al. and Bailey & López de Prado. citeturn946365search0turn946365search7
- Phase 12 status after this step: primary stress execution passed; supplemental robustness execution pending.
