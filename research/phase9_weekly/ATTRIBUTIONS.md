# Phase 9W — Data Attribution and Redistribution Notes

## Primary data source

**thetrademarkk/india-index-options-1m**

Hugging Face dataset:
https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

The dataset is marked CC-BY-NC-4.0 and describes 1-minute OHLCV(+OI) bars for NIFTY, BANKNIFTY and SENSEX index/option data. The data card states that option coverage is partial and recommends verification against official exchange data.

The repository does not redistribute the large raw source Parquet files. The research workflow downloads them into the GitHub Actions/Hugging Face cache and commits only derived metadata such as source revision, file paths, file sizes, checksums and research manifests.

## Secondary source

**rissin/nse-options-intraday**

Hugging Face dataset:
https://huggingface.co/datasets/rissin/nse-options-intraday

The dataset is marked with license value "other". Its card states that intraday data were collected via the Upstox historical API and should be redistributed in line with source-provider terms. Raw source files therefore remain outside the public repository; they are used only through the workflow cache for cross-validation.

## Secondary diagnostic source

**artist-23/nifty-options-data**

Hugging Face dataset:
https://huggingface.co/datasets/artist-23/nifty-options-data

This source is used only for independent diagnostics such as IV/spot/strike/expiry-field comparisons. Raw data are not copied into the repository.

## Research-use rule

Dataset-specific attribution and licensing statements are descriptive. They do not constitute legal advice. The project avoids raw-data redistribution where source terms are not clearly permissive.
