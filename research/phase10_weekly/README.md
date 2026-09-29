# Phase 10W — Mechanics, Margin and Cost Model

## Scope
Formalize executable cash flows, historical statutory charges, Paytm Money brokerage, and the margin measurement required to test the creator's claim that the K2 buyback materially reduces margin.

## Cost schedule
The Phase 11/13 backtest uses dated NSE option transaction charges and STT, plus SEBI/IPFT, stamp duty, GST and Paytm Money brokerage.

## Margin research
NSE Clearing states that SPAN is portfolio-based and uses daily risk arrays; NSE also publishes historical SPAN risk-parameter files and margin reports. The empirical margin study must reconstruct the exact portfolio before lock and the K1/K3 spread after lock for each trade date. citeturn10search3turn10search0turn10search7

## Required margin outputs
- gross SPAN margin before lock;
- net option value / premium component;
- extreme-loss and other applicable margin components;
- margin after K2 buyback;
- absolute and percentage margin change;
- peak margin during the pre-lock interval;
- margin shortfall / square-off exposure proxy;
- sensitivity to adverse underlying and volatility scenarios.

## Important restriction
A lower theoretical risk of the post-lock bull call spread does not by itself prove lower broker margin. The broker/exchange margin engine must be measured using dated risk files.
