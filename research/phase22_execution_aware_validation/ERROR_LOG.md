# Phase 22W Error Log

## E22-001 — No public executable historical quote archive admitted yet
- **Observed:** publicly discoverable RISSIN and TradeMarkk datasets provide 1-minute OHLCV/OI rather than timestamped bid/ask execution quotes.
- **Impact:** they cannot serve as the primary execution-aware dataset.
- **Correction:** retain them only as fallback/cross-check sources and continue the registered NSE/order-trade/depth source audit.
- **No purchase authorized:** no commercial dataset has been purchased.

## E22-002 — Broker historical APIs do not provide the required execution archive
- **Observed:** Upstox exposes live bid/ask/depth and expired-option historical OHLC; Dhan exposes historical expired-option OHLC and real-time 20/200-level depth; Breeze exposes historical option OHLC. None of the documented historical endpoints inspected provides timestamped historical bid/ask/depth for the required contracts.
- **Impact:** these APIs cannot yet satisfy the Phase 22 execution-data contract.
- **Correction:** keep broker APIs documented as live/prospective collection candidates; do not synthesize historical quotes from candles or current option-chain data.

## E22-003 — Public GitHub bid/ask schema without reproducible data archive
- **Observed:** a public NIFTY options analytics repository documents snapshot files with bid/ask fields, but explicitly says the data directory is not tracked in Git.
- **Impact:** schema evidence is not data evidence; the source cannot be admitted without an accessible immutable dataset.
- **Correction:** treat as source lead only; require actual files, provenance and hash before admission.
