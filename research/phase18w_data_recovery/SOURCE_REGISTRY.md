# Phase 18W Source Registry

| ID | Source | Data | Intended use | Access state |
|---|---|---|---|---|
| HF-01 | rissin/nse-options-intraday | NIFTY 1m OHLC/OI | Recent missing cycles | Public; probe pending |
| HF-02 | artist-23/nifty-options-data | NIFTY 1m OHLC/OI/spot | Historical fill | Public; probe pending |
| HF-03 | thetrademarkk/india-index-options-1m | NIFTY 1m OHLC/OI | Cross-fill/validation | Public; probe pending |
| GH-01 | GitHub option-history pipelines | 1m OHLC/OI and retrieval code | Discover lawful archives | Audit |
| API-01 | Upstox expired instruments | 1m OHLC/OI | Direct recovery | Plus/credential required |
| API-02 | ICICI Direct Breeze | historical option OHLC/OI | Direct recovery | Credential required |
| API-03 | Dhan | historical option OHLC/OI | Direct recovery | Credential required |
| API-04 | Angel One SmartAPI | historical option OHLC/OI | Cross-check/recovery | Credential required |
| API-05 | Zerodha/Kite | historical option history | Test expired-instrument limitation | Credential/entitlement |
| NSE-01 | NSE contract-wise historical data | EOD OHLC/OI | Contract validation | Public interface |
| NSE-02 | NSE historical trade/order data | F&O trade/order level | Execution validation | Licensed |
| COM-01 | optionsdata.shop | NIFTY 1m/1s full-chain OHLC/OI | Coverage recovery | Commercial; no purchase yet |
| COM-02 | Global Datafeeds | tick/minute/EOD API | Vendor candidate | Subscription required |
| COM-03 | TrueData | historical L1/BBO candidate | Execution validation | Subscription/custom |
| EX-01 | NSE SPAN/risk files | historical margin parameters | Capital validation | Access probe |

No source is admitted until provenance, contract identity, timestamps, coverage, duplicates and conflicts pass validation.