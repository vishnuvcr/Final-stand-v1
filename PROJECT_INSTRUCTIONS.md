# Project Instructions

This file preserves the governing research requirements supplied for the Final Stand project.

## Research governance
1. Form research questions before testing.
2. Conduct a broad literature and existing-data review using authoritative sources, published research, open datasets and relevant market documentation.
3. Define aims, objectives, scientific methodology, statistical analyses, results, inferences, discussion, strengths, limitations, conclusions and future research.
4. Maintain a detailed phase plan and keep all research phases separately identifiable.
5. Log every material error and every research step, including failed paths and corrections.
6. Update README and status artifacts after meaningful phase changes.
7. Cache important acquired data or manifests so workflows do not redownload unchanged data unnecessarily.
8. Use Python/Rust as appropriate and support reproducible GitHub Actions workflows with manual run capability for each phase.
9. For market research, consider NSE/BSE, global market relationships, option data, FII/DII, volatility, regime/sentiment, benchmark indices, corporate actions, news and microstructure whenever applicable.
10. Include realistic transaction costs, brokerage, slippage and execution constraints, with Paytm Money as the broker-cost reference where applicable.
11. Do not optimize against the final holdout. Final conclusions require an untouched out-of-sample evaluation.
12. End the research after the predefined phases, with a manuscript and explicit future research directions.

## Conversation continuity
The repository is the canonical research-state record. Chat-derived information should be summarized into durable research artifacts. Private chain-of-thought is not stored; only concise, auditable research decisions, actions, evidence and errors are recorded.

## Strategy-specific rule
The supplied video is a source of a candidate hypothesis. Its claims must be distinguished from independently verified payoff mechanics, broker/exchange rules and empirical backtest results.
