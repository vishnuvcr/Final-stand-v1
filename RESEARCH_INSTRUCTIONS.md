# Final Stand v1 — Research Operating Instructions

These instructions govern the research workflow.

1. Maintain a detailed phase/step plan before execution; update it only when the plan changes.
2. Keep every research phase on its own Git branch and provide a manual GitHub Actions entry point.
3. Update phase status, research log, error log and README as the work advances.
4. Preserve mistakes and corrections in the error log so later phases do not repeat them.
5. Cache important external data in GitHub Actions and reuse admitted artifacts rather than redownloading them unnecessarily.
6. For market-data research, exhaust relevant NSE/BSE, public datasets, GitHub, Kaggle, Hugging Face and broker/API routes before declaring a data route unavailable.
7. Never manufacture missing market observations. Do not interpolate, substitute strikes, or mix legs from different sources inside an expiry cycle unless the frozen protocol explicitly permits it.
8. Keep strategy rules, train/validation/holdout splits, transaction costs, brokerages, slippage and stop parameters frozen once preregistered.
9. Use Paytm Money/NSE transaction-cost assumptions already defined by the frozen research code; do not silently remove costs.
10. Every workflow must validate its own coverage and provenance before producing empirical conclusions.
11. Do not stop a research phase because one data source fails; move through the registered fallback sources until the phase exit criteria are met or a serious external dependency blocks further progress.
12. At completion, produce the structured research manuscript with methods, statistical analysis, results, limitations, conclusions, future work, figures, tables and appendices.

Current project repository: https://github.com/vishnuvcr/Final-stand-v1
