# Phase 8 Literature and Evidence Review

## A. Direct strategy mechanics

### Bull call ladder
The video-described pre-lock structure is equivalent to a bull call ladder: long one lower-strike call and short one middle-strike call plus one higher-strike call. Independent strategy references and QuantConnect's formal payoff expression show that the upper short creates theoretically unbounded upside loss above the highest strike and a bounded middle profit zone.

Sources:
- QuantConnect, Bull Call Ladder: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/option-strategies/bull-call-ladder
- ProjectFinance, Bull Call Ladder: https://www.projectfinance.com/bull-call-ladder/
- FYERS School of Stocks, Bull Call Ladder and Bear Call Ladder: https://fyers.in/school-of-stocks/comments/bull-call-ladder-and-bear-call-ladder-1.html

These are technical/educational references rather than peer-reviewed evidence of profitability.

### Lock-in algebra
Buying back the original middle short call cancels that leg. The remaining position is long K1 / short K3, i.e. a conventional bull call spread. This is a mechanical identity, not a claim that the trade is profitable.

## B. Option-return inference and finite-sample risk

Bakshi and Kapadia (2003) examine delta-hedged option returns and document evidence consistent with a negative market volatility risk premium in S&P 500 options, with differences across moneyness and volatility states. This motivates explicit testing of volatility regime effects rather than assuming a universal theta/VRP benefit.

Source:
https://doi.org/10.1093/rfs/hhg002

Broadie, Chernov and Johannes (2009) emphasize that nonlinear option returns have extreme sampling properties and that apparently attractive option-selling returns can be difficult to distinguish from plausible option-pricing models and tail-risk effects. This directly motivates CPCV/DSR/PBO-style robustness checks and tail-sensitive statistics in Phase 12.

Source:
https://business.columbia.edu/faculty/research/understanding-index-option-returns

## C. India / NIFTY-specific evidence

Shaikh and Padhi (2014) study implied-volatility smile/skew, term structure, moneyness and liquidity effects in NSE Nifty options, supporting the use of option-surface state variables and liquidity controls.

Source:
https://doi.org/10.1108/JIBR-12-2013-0103

Sinha and Kamaiah (2017) estimate option-implied risk aversion from a large NIFTY options sample and show that option prices contain information about market expectations and risk preferences.

Source:
https://doi.org/10.1177/2277975216677600

A recent 2026 NIFTY study on volatility risk premium reports positive/regular VRP using NIFTY and India VIX data, but this is a descriptive/VRP finding rather than proof that the specific ladder strategy is tradeable.

Source:
https://economic-sciences.com/index.php/journal/article/view/356

A 2026 SSRN study, "Trading the Volatility Risk Premium on Nifty 50: Strategy Backtest with Realistic Frictions," reports that several VRP strategies turned negative after realistic costs and that tail risk, not merely transaction cost, was a major loss driver. This is particularly relevant because the current strategy has an explicit short-tail component before lock-in.

Source:
https://papers.ssrn.com/sol3/Delivery.cfm/6876580.pdf?abstractid=6876580&mirid=1&type=2

A 2026 paper on conditional dynamics of Nifty-50 volatility-smile asymmetry studies skew/curvature across regimes and links the surface to liquidity, trading activity, maturity structure and volatility states.

Source:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6857939

## D. Current market-rule evidence

NSE's current contract-specification page states that NIFTY 50 index options have three monthly expiries plus quarterly and longer-dated contracts, and that the current expiry day for NIFTY 50 index options is Tuesday of the expiry period, with the previous trading day used when Tuesday is a holiday. The page was updated in August 2026.

Source:
https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications

NSE also maintains current contract information, permitted-lot-size files, quantity-freeze files, margin links and related risk-management resources.

Source:
https://www.nseindia.com/static/products-services/equity-derivatives-contract-information

NSE's India VIX documentation defines India VIX from NIFTY option bid/ask information and as an estimate of expected volatility over the next 30 calendar days. It is therefore a candidate regime variable, not a proof of future realized volatility.

Source:
https://www.nse.in/static/products-services/indices-indiavix-index

## E. Broker and execution evidence

Paytm Money's current F&O FAQ states that brokerage is Rs.10 per unique executed order in futures and options. Its pricing page states statutory/regulatory/exchange charges are levied at actuals and that pricing can change with notice.

Sources:
https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web
https://www.paytmmoney.com/stocks/pricing

Paytm Money's F&O FAQ also states that hedged positions receive margin benefits, while overnight positions require higher margin than intraday positions. Its risk-management policy states that additional margin may be demanded and that insufficient margin can lead to square-off.

Sources:
https://www.paytmmoney.com/stocks/customer/fno-faq/risk-management/rms-policy/what-is-fo-execution-range-and-why-do-some-open-orders-outside-fo-execution-range-get-cancelled
https://www.paytmmoney.com/stocks/customer/fno-faq/trading/general/stocks-allowed-in-futures-options-list
https://www.paytmmoney.com/stocks/static/forms/Download_Center_Forms/Risk-Management-Policy-Equity-Cash-%26-F%26O-v2.pdf

## F. Research implications

1. The strategy's pre-lock tail risk is fundamental, not cosmetic.
2. A high historical win rate alone is insufficient because nonlinear option P&L can contain rare, large losses.
3. "Theta decay" must be decomposed from changes in spot, IV/skew, gamma and execution costs rather than treated as free profit.
4. The lock-in action is economically interesting because it removes the middle short and materially changes the risk topology.
5. Margin reduction must be measured from dated exchange/broker rules, not inferred from a single example.
6. The strategy should be compared against a plain bull call spread because the lock-in state is exactly that structure.
7. India-specific expiry, strike, lot-size and transaction-cost rules must be date-indexed because the derivatives market has undergone structural changes.

## Evidence status
This is an initial Phase 8 literature audit. It is sufficient to finalize the hypotheses and protocol but is not yet the exhaustive final bibliography for the manuscript. Phase 9–14 work will expand the literature/data registry and capture reproducible source snapshots where permitted.
