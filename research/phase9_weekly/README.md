# Phase 9W — Hugging Face Weekly Data Gate

Primary source: thetrademarkk/india-index-options-1m.

- 1-minute NIFTY option data partitioned by expiry.
- Separate 1-minute NIFTY index data.
- OHLC, volume and open interest documented for the primary dataset.
- No historical bid/ask field in the documented schema.

Secondary validation source: rissin/nse-options-intraday.

Secondary diagnostics source: artist-23/nifty-options-data, which includes IV and spot fields through December 2025.

The Phase 9 workflow uses the repository secret HF_TOKEN, Hugging Face caching, source revision capture and SHA-256 manifests.

Run:
.github/workflows/phase-9w-hf-data-gate.yml

The workflow produces a pilot cycle manifest and selected option bars. Large third-party source files remain in the HF/Actions cache rather than being redistributed into this public repository.
