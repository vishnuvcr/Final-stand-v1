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

## 2026-09-29 — Phase 13W holdout protocol
- Created phase-13w-untouched-holdout from the hardened Phase 12 branch.
- Added a mandatory hard-stop selection protocol using training observations only.
- Fixed selection slippage at 0.50 index points per leg; candidate stops are 25/50/75/100/150/200/300 points.
- Holdout observations are not read during parameter selection.
- Added manual and push-triggered GitHub Actions execution.
- No holdout result has been claimed until the workflow output is actually observed.


## 2026-09-29 — Phase 13W execution failure and correction
- Run 36595701035 reached data ingestion successfully: 100 expiry candidates, 63 USABLE_OHLC cycles, 37 incomplete cycles.
- The candidate-generation step nevertheless produced zero trades for all seven stop-loss candidates because the committed workflow omitted the explicit Phase 9 manifest/options/spot paths.
- The holdout selector then failed on missing zero-trade metrics. This is a pipeline defect, not an empirical result.
- Corrective workflow patch: pass all three Phase 9 output paths explicitly to Phase 11 for every candidate run.
- Phase 13 remains pending re-execution; no profitability or holdout conclusion is admitted.


### 2026-09-29 — Phase 13 timestamp investigation
- E-0030/E-0031 fixes did not yet yield trades.
- Added diagnostic output of raw option timestamps, manifest timestamps, and their dtypes before altering the backtest further.
- Strategy rules remain unchanged; no empirical result is accepted until cross-phase timestamp matching is demonstrated.

## 2026-09-29 — Phase 12 robustness closure
- Canonical Phase 12 workflow run 94 completed successfully after optimizing the 30-cell grid to a single-load indexed engine and adding a pre-push rebase.
- All 30 candidate cells produced 63 usable weekly cycles.
- Frozen cell (0.50 slippage per leg, 50-point stop): mean ₹3,503.86/cycle, annualized weekly Sharpe 4.42, bootstrap p=0.0002, Holm-adjusted p=0.006.
- CSCV-style PBO proxy = 0.00 across 20 paths; DSR-style probability = 0.9892. Both are repository-specific approximations and are not exact published-estimator replications.
- Regime and tail-gap diagnostics completed. Historical SPAN/peak-margin integration remains the main capital-normalization blocker.

## 2026-09-29 — Phase 13 holdout closure
- Phase 13 workflow run 36600595100 completed successfully.
- Frozen 50-point stop was selected using training data only at 0.50-point slippage per leg.
- Untouched 14-cycle holdout: mean ₹1,566.04/cycle, win rate 78.57%, annualized weekly Sharpe 2.02, max drawdown -₹12,874.90.
- Holdout remains locked and is not used for subsequent tuning.

## 2026-09-29 — Phase 14 manuscript synthesis
- Created phase-14w-manuscript branch from the completed Phase 13 branch.
- Added final structured manuscript with research questions, aims/objectives, methodology, statistical analysis, results, inference, discussion, strengths, limitations, conclusion, future directions, appendices and supplementary materials.
- Added two SVG figures and a machine-readable supplementary results table.
- Added literature references covering PBO/CSCV, DSR, White's Reality Check, technical-rule bootstrap data-snooping and Holm multiple testing. citeturn0search1turn0search0turn1search0turn1search5turn1search4
## 2026-09-29 — Phase 15W execution-data discovery started
- Created branch phase-15w-execution-data-discovery from completed Phase 14W.
- Audited public TickBytes and OptionVault documentation and sample files.
- Confirmed public NIFTY option samples contain bid/ask and top-5 depth fields.
- Confirmed repository documentation distinguishes evaluation samples from subscription/licensed historical feeds.
- Searched Hugging Face and Kaggle for free Indian/NIFTY option bid/ask archives; no qualifying complete historical archive was identified in this pass.
- Audited official NSE historical-data documentation for historical order/trade and market-data products.
- Gate result: free samples are schema-qualified but no complete free historical quote archive has yet been qualified for the 63-cycle backtest.
## 2026-09-29 — Phase 15W paid-source shortlist
- Current TrueData documentation confirms Level-1 best bid/ask and historical bid/ask history through its Market Data API for NSE F&O; pricing is requirement-dependent and exact long-range/expired-contract coverage must be confirmed.
- Current NSE domestic tariff was checked: Historical Trade Data F&O is ₹1,10,000/year/site; Historical Order & Trade Data F&O is ₹12,50,000/year/site, before applicable taxes/levies.
- TickBytes was retained as a technical alternative because its documented feed contains tick execution data and top-5 bid/ask depth.
- Options Data was rejected for the quote gate because its published historical files explicitly exclude bid/ask.
- Defined the minimum extract required: exact historical dates/contracts, L1 bid/ask and quantities, timestamps, contract identifiers, provenance and research-use licensing.
- No paid purchase has been made; the next gate is verification of exact historical coverage and cost.
## 2026-09-30 — Phase 15W expanded free-source audit
- Re-read Phase 15W plan/status and repository logs before proceeding.
- Expanded the search to public Hugging Face datasets, Kaggle archives, Zenodo, GitHub repositories, broker APIs and open option-chain APIs.
- Qualified several sources for OHLC/schema cross-checking but found no new free historical NIFTY weekly-options BBO archive meeting the Phase 15W execution-data gate.
- Added ICICI Breeze, Upstox expired instruments, FYERS, Kotak Neo, Angel One, Dhan, OpenAlgo, ayyararyan/nse-options-pipeline and djjain21's historical-depth repository to the audit matrix.
- The most important new schema source is ayyararyan/nse-options-pipeline; its BBO fields are documented, but its actual NSEI-Data input is explicitly not tracked in Git.
- No strategy, holdout, cost or parameter state was changed.
- Next action: empirical probe of any user-authorized free API credentials, then exact contract/date coverage validation.

## 2026-09-30 — Phase 15W API capability gate
- Re-checked the phase plan, status and logs before proceeding.
- Verified official/API documentation for ICICI Breeze, Dhan and Upstox; these provide historical OHLC/coverage routes but not historical BBO in the documented response. citeturn2search1turn1search0turn0search0
- TrueData documentation remains the most directly aligned candidate because historical tick retrieval can include bid/ask and expired symbols, but exact old-date coverage must be verified with authenticated access.
- Added an API probe protocol and credential-safe scaffold. No credentials were stored and no strategy/holdout data were accessed.
- Phase 15W remains blocked only at the authenticated historical-BBO access gate; free archive discovery is complete for the current search scope.


## 2026-09-30 — Phase 16W initialization
- Closed Phase 15W's free-BBO discovery gate without qualifying a free historical BBO archive.
- Started Phase 16W on a separate branch for capital/margin validation using official NSE historical SPAN/risk-parameter/report infrastructure.
- Preserved the frozen strategy, locked holdout, and no-tuning rule.
- Added a manual GitHub Actions workflow and source-admission protocol.
