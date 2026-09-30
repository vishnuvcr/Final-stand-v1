# Phase 22W — Execution Data Contract

## Status
**22.2 draft/frozen for implementation; execution-data admission remains conditional on source access.**

### Required fields

For every selected NIFTY option leg:

- exchange timestamp in IST with documented precision;
- trade date;
- expiry;
- strike;
- call/put;
- best bid price and quantity;
- best ask price and quantity;
- quote update timestamp;
- market status/session marker where available.

Preferred:
- top-5 or top-20 depth;
- trade price/quantity;
- sequence/order identifiers;
- cumulative volume and OI.

### Quote admissibility

A quote is executable only when:

1. bid and ask are both present;
2. bid <= ask;
3. prices are positive and finite;
4. quote timestamp is at or immediately before the decision timestamp under the predeclared alignment rule;
5. quote is not stale under the frozen stale-quote threshold;
6. required quantity is available at the executable side or the depth model explicitly permits aggregation across levels.

### Entry/exit convention

For a long option leg, executable entry uses the ask side; executable exit uses the bid side.

For a short option leg, executable entry uses the bid side; executable exit uses the ask side.

No midpoint fills are permitted for the primary execution-aware result.

### Costs

The calculation must include:

- Paytm Money brokerage assumptions already registered in the project;
- exchange transaction charges;
- SEBI charges;
- GST;
- stamp duty;
- STT/CTT where applicable;
- slippage beyond displayed liquidity only if explicitly modeled;
- spread crossing through executable bid/ask.

### Missing data

A cycle is invalid when any required leg lacks an admissible executable quote at a required decision point.

No interpolation, synthetic bid/ask, strike substitution, or cross-source leg mixing is permitted.

### Primary robustness variants

The statistical report should separately show:

1. displayed best-quote execution;
2. conservative one-tick/slippage stress;
3. liquidity-constrained execution where size is available.

These are robustness analyses, not alternate post-hoc strategies.
