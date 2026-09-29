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