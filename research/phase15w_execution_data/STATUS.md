# Phase 15W — Execution Data Discovery Status

## State
Active — free historical bid/ask discovery and schema qualification.

## Objective
Determine whether a legally usable, sufficiently granular historical NIFTY options Level-1/Level-2 quote source is available without purchasing a commercial dataset, and whether it can support execution-price validation of the frozen weekly strategy.

## Frozen constraints
- Strategy parameters remain frozen from Phase 13W.
- The untouched 14-cycle holdout remains locked.
- This phase may improve execution-data fidelity but must not select a new stop, strike rule, entry rule or exit rule.
- Vendor claims and public sample files cannot be treated as evidence of complete historical coverage.

## Work completed
1. Audited public TickBytes documentation and NIFTY option samples.
2. Audited public OptionVault documentation and Level-2 sample.
3. Searched Hugging Face and Kaggle for Indian/NIFTY option bid/ask datasets.
4. Audited official NSE historical-data documentation.

## Evidence
- TickBytes exposes a NIFTY option sample with timestamped Level-1 best bid/ask plus top-5 depth.
- OptionVault exposes a Level-2 sample with five bid/ask levels and quantities.
- Both repositories distinguish public evaluation samples from subscription/licensed historical feeds.
- The inspected free samples are dated 2026 and are not a complete historical archive covering the 63-cycle study.
- The current OptionVault 1-minute options schema contains OHLC/OI/Greeks, not historical bid/ask.
- NSE documents historical order/trade and Level-1/Level-2/tick data products, but the relevant historical products are not identified as free archives.

## Gate decision
FREE HISTORICAL BID/ASK DATASET: NOT YET QUALIFIED.

The free samples prove that the desired schema exists, but do not establish free access to the historical quote history required for the backtest.

## Next actions
- Continue searching public GitHub, Hugging Face and Kaggle sources.
- Check exact coverage against the Phase 9W weekly-cycle dates and option contracts.
- If no qualifying free archive is found, quantify the minimum paid extract required.
- Preserve the frozen strategy and holdout throughout.
## Additional search result
- SauMStats NIFTY market-data engine was checked as an independent candidate; its documentation explicitly says bid/ask quotes are not available and market price is proxied by close.
- This candidate is therefore rejected for quote-based execution validation.

## Current conclusion
After the first public-source audit, no complete free historical NIFTY options L1/L2 quote archive has been qualified. The strongest free evidence is limited to evaluation samples. The next step is to determine whether a small legitimate paid historical extract, rather than a broad commercial archive, can cover the exact weekly cycles required.
## Paid-source research update
- TrueData is now the highest-priority targeted inquiry: its current documentation states NSE F&O historical data can include Level-1 best bid/ask history, but pricing is customized and historical retention/expired-contract coverage must be confirmed for the exact study dates.
- NSE is the official fallback. Current domestic pricing lists ₹1,10,000/year/site for historical F&O trade data and ₹12,50,000/year/site for historical F&O order-and-trade data, excluding taxes/levies.
- TickBytes is a strong technical alternative because its feed contains top-5 bid/ask depth, but the complete historical archive is subscription/licensed.
- Options Data is not suitable for the bid/ask gate because its published files explicitly exclude bid/ask.
- A minimum-extract specification and vendor inquiry have been written; no purchase has been made.