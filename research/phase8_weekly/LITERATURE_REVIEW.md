# Phase 8W — Weekly Options Literature and Evidence Review

## 1. Weekly-option market structure

NSE currently specifies four weekly NIFTY 50 index-option expiry contracts excluding the monthly contracts. Weekly NIFTY options expire every Tuesday, or on the previous trading day when Tuesday is a holiday. NSE also states that a new serial weekly contract is introduced after the respective week's expiry. This makes a one-expiry/one-trade-cycle design a natural unit for the new experiment.

Source:
https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications

Source:
https://www.nseindia.com/static/products-services/equity-derivatives-nifty50

## 2. Very short-dated option risk

Andersen, Fusari and Todorov, "The Pricing of Short-Term Market Risk: Evidence from Weekly Options" (NBER Working Paper 21491), studies weekly S&P 500 index options and emphasizes that weekly contracts provide a direct window into very short-horizon market and jump risk.

Source:
https://www.nber.org/papers/w21491

This supports separating weekly option dynamics from monthly-option evidence rather than assuming the same return-generating mechanism.

## 3. Theta versus gamma in Indian index options

Singhal and Bhattacharyya (2024) study theta decay and delta fluctuations in Indian index options and note that theta accelerates toward expiry, but delta/gamma effects can overwhelm theta, especially near expiry. This is directly relevant to the video strategy because its core claim is based on allowing the far OTM short call to decay over a short weekly horizon.

Source:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4651325

Research implication:
- measure Greek attribution rather than calling all P&L "theta";
- explicitly measure gamma exposure during the final sessions;
- stress large underlying moves during the decay window.

## 4. Weekly option market segmentation

Chatrath, Christie-David, Miao and Ramchander (2015), "Short-term options: Clienteles, market segmentation, and event trading," compares weekly and monthly S&P 500 options and finds materially different trading characteristics, including higher implied volatility and different price-discovery behavior in weekly options.

Source:
https://doi.org/10.1016/j.jbankfin.2015.09.001

This supports treating weekly and monthly strategies as separate empirical objects.

## 5. Weekly options and underlying-market dynamics

Ellahie, Kaplan, Potter and Saha (2026), "Levering Up! Short-Horizon Option Availability and the Gamification of the Stock Market," reports that the introduction of weekly options is associated in its studied U.S. setting with higher trading volume and return volatility and increased gamma-related hedging activity.

Source:
https://ssrn.com/abstract=6703098

This is U.S. evidence, not NIFTY evidence. We use it only to motivate testing weekly-cycle market-state effects, not as proof of an Indian trading edge.

## 6. Expiration-week effects

Stivers and Sun (2013), "Returns and Option Activity over the Option-Expiration Week for S&P 100 Stocks," reports systematic differences in returns and implied-volatility behavior during option-expiration weeks and discusses market-maker hedging as one possible contributor.

Source:
https://doi.org/10.1016/j.jbankfin.2013.07.030

Research implication:
The final 1–2 sessions of the weekly cycle cannot be treated as statistically identical to the first sessions. Regime and day-to-expiry effects must be included.

## 7. Weekly options and short-horizon predictive information

Saba, Bhuyan and Cetin (2025), "Predicting Short-term Stock Returns with Weekly Options Indicators," finds predictive information in weekly option open-interest and volume measures in the studied U.S. setting.

Source:
https://doi.org/10.1142/S2010139225500041

Research implication:
Include weekly option volume/OI and skew as state variables in the regime analysis, while avoiding data leakage.

## 8. India-specific market-structure changes

A 2026 SSRN paper by Rawat and Shreshtha documents major 2024–2025 Indian equity-index-derivatives reforms and reports changes in index-option turnover and composition after reforms. This is relevant because a long weekly history can span materially different contract and participant regimes.

Source:
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7135161

The findings are external research, not a claim about this strategy.

## 9. Research conclusion from the literature

The literature gives four reasons to restart the experiment as a genuinely weekly study:

1. Weekly options are structurally different from monthly options.
2. Very short maturity magnifies the interaction of theta, gamma, jumps and liquidity.
3. Expiration-week market behavior may itself change across the lifecycle.
4. Indian derivatives-market rules and participant composition have changed, so historical weekly results must be segmented by effective market regime.

Therefore the new research will not recycle the monthly backtest with a different expiry filter. It will use a weekly lifecycle model from the ground up.
