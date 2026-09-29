# Phase 8 Data-Source Manifest and Feasibility Audit

## Decision
**Data feasibility: PARTIALLY PASS / execution-history gap remains.**

A rigorous backtest is feasible in principle, but the quality of the conclusion depends on the historical quote granularity available. Official NSE sources document historical F&O snapshots, trades and order/trade data, while current NSE feeds explicitly distinguish best bid/ask, market depth and tick/order-book levels. Some of the richest historical data is subscription-based. Therefore a long-history strategy study can be done, but exact historical bid/ask reconstruction may require licensed NSE data or an explicitly conservative execution model.

## Source registry

| Source | Coverage / content | Use | Limitation | Status |
|---|---|---|---|---|
| NSE historical F&O framework | Monthly directories from 2003; bhavcopy, masters, snapshots, trades, circulars | Contract mapping, historical option prices, PIT validation, market-design changes | Rich order/trade/snapshot history may require access/subscription | ✅ primary |
| NSE EOD / historical data subscription | F&O EOD and historical order/trade data | Authoritative execution and contract history | Paid/entitlement-dependent | ✅ primary |
| NSE real-time/snapshot specification | Level 1 bid/ask, Level 2 depth, Level 3 depth, tick-by-tick; 1/5-min snapshots | Defines what executable quote data should look like | Current feed description, not itself the historical dataset | ✅ methodology |
| NSE option chain | Bid, ask, quantities, LTP, IV, volume, OI | Current schema validation and spot checks | Not a substitute for a complete historical PIT archive | ✅ validation |
| NSE contract information | Permitted lot size, quantity freeze, margin links and related files | Contract mapping and margin | Current portal, historical files must be versioned | ✅ primary |
| NSE circular 176/2025 | NIFTY lot revised 75 -> 65; effective schedule by expiry | Historical lot-size transition | Must join to contract introduction/expiry date | ✅ primary |
| India VIX | NIFTY-option bid/ask-derived expected-volatility index | Regime variable | Not a direct strategy P&L input | ✅ primary |
| Public/open-source datasets (Hugging Face etc.) | Some 1-min/EOD NIFTY options datasets | Prototyping, validation, sensitivity | Often OHLC-only, sparse far strikes, licensing/coverage differences, no true historical bid/ask | 🟡 secondary |
| Broker records / Paytm Money documentation | Brokerage, margin, RMS constraints | Cost and execution model | Current rules do not automatically describe historical rules | ✅ primary for current |

## Key historical contract rule

NSE Circular 176/2025 revised the NIFTY market lot from 75 to 65. It states that the revised lot applies to the first weekly expiry on 06-Jan-2026 and first monthly expiry on 27-Jan-2026, while existing lot size remained applicable to weekly/monthly contracts through the 30-Dec-2025 expiry. Historical backtests must therefore be date/contract aware rather than applying one lot size across the sample.

## Quote-quality hierarchy

For the strategy's entry and lock legs:

1. Historical order-book Level 1 bid/ask at or immediately before the decision timestamp.
2. Historical snapshot bid/ask at the decision timestamp.
3. Trade prints with reconstructed effective spread only as a lower-quality fallback.
4. OHLC/LTP-only data for exploratory backtests only, never as the sole evidence for final execution claims.

## Minimum fields per option observation

- decision timestamp;
- trading date;
- underlying;
- expiry;
- strike;
- CE/PE;
- bid;
- ask;
- bid quantity;
- ask quantity;
- LTP;
- traded volume;
- OI;
- IV if available;
- source;
- quote age / freshness;
- contract lot size effective on that date;
- data quality flag.

## Entry reconstruction requirement

At every candidate entry timestamp we need all of:
- spot/index reference;
- K1, K2 and candidate K3 calls;
- valid premiums for the premium-difference rule;
- bid/ask for actual simulated fills;
- sufficient quote freshness;
- valid contract and expiry mapping.

If any essential field is unavailable, the candidate trade must be rejected or assigned to a separate lower-quality sensitivity sample.

## Lock reconstruction requirement

At the lock timestamp we need:
- the K2 executable ask to close the original short;
- current K1 and K3 marks for post-lock valuation;
- contemporaneous underlying;
- same-expiry contract identity;
- quote quality sufficient to model a realistic buyback.

## Margin data requirement

Exact historical margin should use dated NSE/clearing risk-parameter files or broker historical margin evidence. A fixed video example such as ₹65,000 -> ₹15,000 is not admissible as empirical margin evidence.

## Data-splitting rule

Any source downloaded or transformed for research must carry:
- source URL;
- retrieval timestamp;
- source modification/effective date where available;
- checksum;
- transformation version;
- license/usage note.

Important immutable source files should be cached so repeated GitHub Actions runs do not depend on live web availability.

## Current audit conclusion

The project should not jump directly from public EOD OHLC data to a final profitability claim. The first data gate is to obtain and validate a pilot sample containing actual bid/ask or sufficiently granular historical snapshots for all three legs and the lock leg. A later full-history run can use the same schema.

## Next concrete data gate

Acquire a small, representative pilot covering:
- at least 20 monthly NIFTY expiries;
- multiple volatility regimes;
- both pre- and post-lot-size revision periods;
- enough intraday observations to reconstruct entry and lock timing.

Pass criteria:
- >=95% of sampled candidate trades have usable quote pairs for K1/K2/K3 at entry;
- >=95% have usable K2 quote at lock;
- contract mapping error rate <0.1%;
- no look-ahead detected;
- reproducible source checksum and transformation manifest.
