# Phase 8W — Weekly Research Protocol

## Phase reset rule

The monthly-expiry experiment is archived. All empirical testing from this branch uses weekly contracts only.

## 8W.1 Contract universe
- NIFTY 50 weekly options only.
- One weekly expiry = one potential trade cycle.
- Monthly contracts are excluded from the primary experiment.
- Expiry-day rules are joined to the historical effective date of the exchange contract regime.

## 8W.2 Weekly cycle
Primary:
- expiry Tuesday, or prior trading day if Tuesday is a holiday;
- enter first trading session following that expiry at 10:00 IST;
- construct K1/K2/K3;
- lock previous trading day at 14:00 IST;
- exit before settlement.

The exact timestamp convention is frozen before backtest code is fitted.

## 8W.3 Data requirement
For each cycle, obtain:
- spot;
- K1/K2/K3 quotes at entry;
- K2 quote at lock;
- K1/K3 quotes at lock;
- final exit quotes;
- volume/OI;
- lot size;
- margin information;
- India VIX and regime variables.

## 8W.4 Execution
- Buy at ask plus slippage.
- Sell at bid minus slippage.
- Reject crossed, stale or invalid markets.
- Use midpoint only for strike-selection measurement.
- Use executable quotes for P&L.

## 8W.5 Cost model
Apply date-effective:
- brokerage;
- STT;
- exchange fees;
- SEBI fee;
- stamp duty;
- GST;
- slippage;
- liquidity impact;
- square-off fees if applicable.

## 8W.6 Backtest controls
Run all controls on identical weekly dates and quote-quality rules.

## 8W.7 Statistical design
- chronological split;
- rolling/walk-forward;
- weekly-cycle block bootstrap;
- CPCV/PBO/DSR where sample size supports it;
- multiple-testing control.

## 8W.8 Data and leakage audit
For each trade store:
- data timestamps;
- contract identity;
- strike selection inputs;
- quote quality;
- fill assumptions;
- cost schedule version;
- margin schedule version.

## 8W.9 Final holdout
The final holdout is a contiguous unseen set of weekly expiry cycles. No rule changes are allowed after its results are inspected.

## 8W.10 Reproducible outputs
Produce:
- trade ledger;
- equity curve;
- weekly P&L distribution;
- drawdown chart;
- margin chart;
- cost attribution;
- regime tables;
- robustness tables;
- statistical appendix.

## Stop rule
After the weekly final manuscript/reproducibility package is complete, stop. Do not keep searching for better weekly parameters.
