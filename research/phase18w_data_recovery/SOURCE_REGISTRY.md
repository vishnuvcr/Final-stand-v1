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

## Additional source discoveries — 2026-09-30
- Upstox officially exposes expired option contracts and expired historical candles at 1-minute resolution; access requires Upstox Plus. citeturn1search0turn1search1
- ICICI Breeze public GitHub pipelines demonstrate a practical route for downloading years of NIFTY weekly options at 1-minute OHLCV + OI, subject to the user's own Breeze credentials/API access. citeturn1search5turn1search10
- TickBytes advertises Level-1/Level-2 tick, 1-second and 1-minute NIFTY option-chain archives, but its full archive is subscriber/private rather than freely downloadable. citeturn1search9
- HF-03 explicitly warns that illiquid/far strikes can be sparse or absent; therefore 63/63 expiry-file presence does not establish complete strategy coverage. citeturn0search0turn0search4
