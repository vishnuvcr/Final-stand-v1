# Phase 10W Margin Protocol

1. For each admissible weekly cycle, construct the exact pre-lock portfolio:
   +1 K1 call, -1 K2 call, -1 K3 call.
2. Use the dated NSE SPAN risk-parameter file for the trading date.
3. Compute portfolio scenario losses/risk arrays using the exchange contract identifiers and lot size applicable that date.
4. Record SPAN, ELM, premium/net-option-value and other required components separately.
5. Reconstruct the post-lock portfolio:
   +1 K1 call, -1 K3 call.
6. Repeat the dated margin calculation.
7. Compare absolute margin and percentage change.
8. Separately record peak margin requirements if the required intraday files are available.
9. Do not infer broker-specific Paytm Money RMS requirements from exchange SPAN alone; compare against Paytm Money's published RMS policy and document any broker-specific add-ons.
10. Report margin relief only as measured evidence.
