# Phase 10W — Execution Cost and Margin Model

## Evidence inputs

Paytm Money currently states ₹10 brokerage per unique executed F&O order. citeturn6search8

NSE publishes daily F&O SPAN risk-parameter files and explains that SPAN evaluates portfolio losses across underlying-price and volatility scenarios; NSE also publishes client-level margin reports. citeturn6search0turn6search3turn6search5

NSE's current contract specification identifies NIFTY 50 as having four weekly expiries excluding monthly contracts and Tuesday weekly expiry. citeturn0search1turn0search4

NSE Circular 176/2025 changed the NIFTY market lot from 75 to 65 for the specified 2026 contract transition. Historical weekly results must therefore use the effective lot size for each contract. citeturn6search37

## Fill model

### Buys
`fill_buy = ask + slippage`

### Sells
`fill_sell = bid - slippage`

### Midpoint
Midpoint is permitted only for strike-selection diagnostics. It is not the primary P&L fill.

## Slippage scenarios

Three frozen scenarios:

1. Base: one half-spread plus a small additional execution allowance.
2. Stressed: one full quoted spread plus additional slippage.
3. Adverse: two-sided adverse execution on every leg.

Exact numerical slippage parameters must be calibrated from the historical quote data once acquired. They must not be tuned to produce a favorable result.

## Brokerage

Each executed unique F&O order is charged according to the date-effective Paytm Money schedule.

The weekly strategy has:
- 3 entry orders;
- 1 K2 lock order;
- 2 post-lock exit orders;

for a minimum of six executed orders when no stop occurs.

A stopped or otherwise early-exited trade can have additional orders and therefore higher brokerage.

## Statutory and exchange charges

The engine keeps the following as separate fields rather than one blended percentage:

- STT;
- exchange transaction charge;
- SEBI fee;
- stamp duty;
- GST;
- brokerage;
- slippage.

The date-effective schedule is stored with every trade.

## Margin model

Primary target:
- reproduce portfolio margin using dated NSE SPAN risk-parameter files where available.

Required fields:
- trade date;
- contract;
- strike;
- expiry;
- option type;
- quantity;
- SPAN scenario values;
- exposure/ELM components;
- net option value;
- applicable client margin.

NSE describes SPAN as a portfolio-based system and provides risk arrays that represent potential one-day gains/losses under specified price/volatility scenarios. citeturn6search3turn6search1

### Fallback margin model

If exact historical SPAN files cannot be obtained, the research may report:
- conservative short-option notional/risk proxy;
- broker-observed margin where documented;
- post-lock defined-risk spread capital requirement.

The fallback must be clearly labeled **proxy**, never presented as exact historical margin.

## Primary capital metrics

- peak margin;
- mean margin;
- median margin;
- margin immediately before lock;
- margin immediately after K2 buyback;
- percentage margin reduction;
- net P&L / peak margin;
- net P&L / average margin;
- maximum adverse excursion / peak margin.

## Cost sensitivity

The final report must show net P&L under:
- base execution;
- stressed execution;
- adverse execution.

A strategy that is profitable only under midpoint fills or zero slippage fails the economic robustness gate.

## Weekly turnover warning

Because the experiment generates one potential trade every week, even small per-cycle costs compound materially. Therefore:
- annual turnover;
- annual brokerage;
- annual statutory charges;
- annual spread/slippage;
- cost as percentage of gross P&L

are primary results.
