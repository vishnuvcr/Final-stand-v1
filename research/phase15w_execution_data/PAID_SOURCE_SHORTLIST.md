# Phase 15W — Paid Source Shortlist and Minimum Extract Specification

## Decision objective
Identify the smallest legitimate dataset capable of replacing OHLC-reconstructed execution with observed historical best bid/ask for the already-frozen 63 weekly cycles.

## Candidate A — TrueData Market Data API
- TrueData states that NSE F&O historical data are available through its API and that historical data can include best bid/ask history.
- Its documentation states Level 1 contains best bid/ask and that historical bid/ask is available through its Market Data API.
- The API pricing is requirement-dependent; TrueData states pricing depends on exchange segments, number of symbols, and whether real-time and/or historical data are required, with a free trial available.
- A separate TrueData page states the standard API historical tick retention is limited, so the exact historical archive available for the 63-cycle period must be confirmed with the vendor rather than inferred from the live API limits.
- Qualification: **highest-priority quote-data inquiry**, because the required output is directly best bid/ask rather than reconstructed order-book events.

## Candidate B — NSE historical data
- NSE documents historical order/trade data for F&O and provides timestamped historical order-book events and executed trades.
- NSE's April 2026 domestic tariff lists Historical Trade Data for F&O at ₹1,10,000 per annum per site and Historical Order & Trade Data for F&O at ₹12,50,000 per annum per single site, excluding applicable taxes/levies.
- This is substantially more expensive than a targeted vendor extract and is not the first choice for this research unless a direct quote feed cannot be obtained.
- Qualification: **official fallback**, particularly if order-level reconstruction becomes necessary.

## Candidate C — TickBytes
- TickBytes documents tick-by-tick execution ticks plus top-5 bid/ask depth and 1-second/1-minute aggregates.
- Public samples establish the desired schema, but the complete archive is a subscription/licensed product.
- Qualification: **high-priority targeted historical-file inquiry** if they can sell only the required NIFTY option dates/contracts rather than a broad archive.

## Candidate D — Options Data
- Options Data offers NIFTY 1-minute and 1-second historical chains at published one-time prices, including all strikes/expiries and OI.
- Its own documentation explicitly states the files do not contain bid/ask.
- It is therefore not a solution to the primary bid/ask gate, but can serve as an independent OHLC/1-second cross-check if needed.
- Qualification: **not suitable for quote validation**.

## Minimum data request
Request only:
1. NIFTY index options, NFO-OPT.
2. Exact dates contained in the Phase 9/13 weekly-cycle manifest.
3. Exact contracts K1, K2 and K3 used by the frozen strategy, plus the underlying NIFTY spot/index series needed for timestamp alignment.
4. Intraday timestamps at the finest available quote resolution.
5. best_bid, best_ask, bid_qty, ask_qty.
6. LTP/LTT/LTQ and cumulative volume/OI where available.
7. contract symbol, expiry, strike and CE/PE.
8. timezone explicitly documented as IST or exchange-local time.
9. data revision/version identifier and provenance statement.
10. permission for private research/backtesting; redistribution is not required.

## Exact execution-validation requirement
For each strategy leg we need the nearest valid quote at or immediately before the model decision timestamp, with a documented staleness tolerance. Market buys will be evaluated against ask and market sells against bid. If a quote is stale or missing, the observation will be classified as unavailable rather than silently filled from OHLC.

## Vendor inquiry text
Subject: Historical NIFTY weekly options L1 bid/ask data for research

Request: Please quote the minimum-cost historical dataset/API access containing NIFTY option best bid/ask history for a specified list of historical dates and exact option contracts. We require bid price, ask price, bid quantity, ask quantity and timestamp, plus contract identifiers. We do not require the full market universe, Level-2 depth, or real-time access. The intended use is academic/private backtesting of a fixed weekly options strategy. Please state available date range, quote resolution, whether expired contracts are included, data licensing terms, and one-time versus recurring price.

## Purchase gate
Do not purchase yet. First obtain/verify the exact date coverage and expired-contract availability. A paid source is admissible only if it can cover the historical weekly cycles without changing the frozen strategy or holdout.