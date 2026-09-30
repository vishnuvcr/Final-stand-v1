# Phase 22W — Data Source Audit

## Status
**22.1 complete — execution-aware source landscape mapped; no paid data acquired.**

## Findings

| Source | Data | Bid/Ask / depth | Historical coverage | Admission status |
|---|---|---|---|---|
| NSE Data & Analytics | Official historical EOD/order/trade products | Order/trade; official historical products | Exchange data products | **Primary authoritative route; access/subscription required** |
| NSE real-time products | Level 1/2/3/tick | L1 best bid/ask; L2 top 5; L3 top 20; tick full book | Real-time product, historical availability depends product | **Execution schema confirmed; historical access must be obtained/verified** |
| RISSIN HF | 1-min NIFTY/BANKNIFTY/SENSEX OHLCV/OI | No bid/ask | Oct 2024→2026 | **Already admitted for Phase 21 recovery; OHLC fallback only** |
| TradeMarkk HF | 1-min index/options OHLCV/OI | No bid/ask | ~2021→2026; partial option coverage | **Independent OHLC cross-check candidate** |
| QuantDev-stack TickBytes | Tick/L2/1-sec/1-min | Advertises L1/L2 | Current archive/subscription | **Potential execution-data candidate; sample/public schema only; no purchase without authorization** |
| QuantDev-stack OptionVault | 1-min/tick/Level-2 | Advertises tick/depth | 2018→present depending product | **Potential execution-data candidate; licensed full dataset** |
| optionsdata.shop | 1-min option bars | No bid/ask | Jan 2023→Sep 2026 | **Commercial OHLC fallback; no purchase without authorization** |
| GitHub NIFTY market-data engine | Query layer over Kaggle/other files | No verified bid/ask | 2024 + live 2026 | **Useful engineering/source-discovery route, not execution evidence** |

## Key external evidence

- NSE's official historical-data documentation describes F&O historical order data at tick frequency, including transaction time, buy/sell indicator, order number and instrument fields. citeturn0search44
- NSE's real-time market-data documentation explicitly defines Level 1 as best bid/ask, Level 2 as five levels of depth, Level 3 as twenty levels, and tick-by-tick as full order-book data. citeturn0search12
- NSE provides paid historical EOD and historical order/trade products, with F&O technical specifications and sample files. citeturn0search1
- RISSIN provides 1-minute OHLCV/OI but not executable quote data. citeturn0search0
- TradeMarkk provides an independent 1-minute OHLCV/OI archive but explicitly warns that option coverage can be partial. citeturn0search13
- Public GitHub datasets advertise deeper tick/Level-2 archives, but the complete data are licensed/subscription data and therefore cannot be assumed available. citeturn0search3turn0search9

## Phase 22 admission rule

No execution-aware result will be admitted until the data source demonstrably contains timestamped executable bid/ask/depth observations for the exact NIFTY option contracts and periods used by the new experiment.

No purchase or external credential use is authorized by this phase plan.


## 22.1B — Broker/API route audit (2026-09-30)

- Upstox documents live market-feed bid/ask quantities and prices and D0/D5 depth, plus expired-option contract/candle APIs. Its documented historical expired-instrument endpoint is OHLC, not historical bid/ask/depth. citeturn0search1turn1search4turn1search9
- Upstox option-chain APIs expose current bid/ask price and quantity, but this is a live/current option-chain interface rather than a historical quote archive. citeturn1search3
- Dhan documents historical expired-options data at one-minute resolution with OHLC, IV, OI, volume and spot, but the historical endpoint does not document bid/ask fields. Dhan's 20/200-level depth is documented as real-time websocket data. citeturn1search0turn1search12
- ICICI Breeze's documented historical options API returns minute OHLC/volume and does not expose historical bid/ask in the shown response. citeturn2search5
- A public GitHub NIFTY options analytics repository describes snapshot CSVs containing captured_at, bid_price, ask_price, bid_qty and ask_qty, but its data directory is explicitly not tracked in Git; therefore the repository does not itself provide an admissible reproducible historical quote archive. citeturn2search3
- A separate public NIFTY data-engine repository explicitly states that bid/ask quotes are not available and market_price is substituted from close_price, so it is not execution evidence. citeturn2search0

### Updated admission conclusion

The audit has now covered official NSE historical order/trade products, public OHLC archives, broker APIs with current depth, broker expired-contract historical candles, and public GitHub snapshot schemas. No reproducible, freely accessible historical NIFTY option bid/ask/depth archive has yet been admitted for Phase 22. The official NSE historical order/trade route remains the authoritative candidate, while broker live-depth APIs could support a future prospective collection study but cannot reconstruct past quotes.

No new holdout is opened until an admissible historical execution dataset exists.


## 22.1C — TrueData historical bid/ask route (2026-09-30)

- TrueData states that its Market Data API supports NSE Futures & Options and that historical data are available with or without Bid/Ask history. Its documentation describes Level-1 best bid/ask as part of the feed. citeturn3search8turn3search0
- The TrueData historical client code exposes tick-history retrieval with a bidask flag, supporting historical tick responses containing bid, bid quantity, ask and ask quantity. citeturn3search1
- This makes TrueData the strongest currently identified vendor route for satisfying the Phase 22 execution-data contract, subject to actual access, coverage verification, licensing and reproducible download.
- No TrueData credentials are present in the research protocol, and no paid subscription has been authorized. Therefore no TrueData data are admitted yet.

### Route status

**Strong candidate — access pending.** If an authorized trial/subscription or existing credential becomes available, the first acquisition test should use a small historical NIFTY weekly-expiry sample and verify exact timestamp, expiry, strike, CE/PE, bid/ask, bid/ask quantity, and source provenance before any full acquisition.

## 22.1D — TrueData retention constraint verified (2026-09-30)

- Current TrueData documentation states default REST history is **5 trading days for tick data**, **6 months for intraday bars**, and **10+ years for daily bars**; extended history is described as an add-on. citeturn0search1turn0search3
- TrueData separately confirms historical data can include Bid/Ask history and real-time tick fields include timestamp, tick sequence, bid, bid quantity, ask and ask quantity. citeturn0search4turn0search6
- Therefore TrueData is technically compatible with the execution contract, but default REST retention is insufficient for the historical weekly-expiry sample required by Phase 22 unless an extended-history entitlement covers the target dates.
- No credentials, subscription, or paid add-on is assumed. No TrueData data are admitted.

### Acquisition gate
A future acquisition attempt must first obtain a small sample covering at least one target historical expiry and verify that the account actually returns timestamped bid/ask/quantity observations for the exact option contracts. If only the default five-day tick window is available, the source cannot satisfy the retrospective Phase 22 experiment.

## 22.1E — Additional historical routes: GFDL and NSE full order/trade

- Global Datafeeds (GFDL) documents historical NFO tick data with BUYPRICE/BUYQTY and SELLPRICE/SELLQTY and says NFO tick backfill is one calendar week. Its option-chain API also exposes bid/ask and sizes, but these are live/current chain endpoints. citeturn3search19turn3search3turn3search6
- GFDL therefore has the required field shape but, like TrueData default tick retention, its documented historical tick window is too short for the retrospective Phase 22 sample unless a separate archival product is licensed.
- NSE's current Historical Order & Trade specification states that full historical Orders and Trades provide complete order-book events and executed trades, with timestamps, prices, volumes and identifiers; full orders are released after 90 calendar days and full trades after 30 calendar days. citeturn4search33
- This makes the **NSE official full-order/full-trade archive** the strongest authoritative reconstruction route. It is an exchange data product requiring subscription/access, and the project currently has no such entitlement.

### Updated route priority
1. **NSE full Orders + Trades** — strongest authoritative historical reconstruction route; access required.
2. **TrueData extended historical Bid/Ask** — technically compatible; extended-history entitlement required for old periods.
3. **GFDL historical tick** — technically compatible; documented default tick retention only one week.
4. Public OHLC/option-chain archives — fallback/cross-check only.

No source is admitted until an actual sample for the required target dates/contracts is obtained and schema/provenance/hash checks pass.


## 22.1D — TrueData availability qualification

- TrueData's current documentation confirms historical Bid/Ask history and the required tick fields, but its standard REST historical availability page says tick history is limited to the **last 5 trading days** by default; extended history is an add-on. citeturn0search0turn0search2
- TrueData also documents historical Bid/Ask through its WebSocket services and says its historical data are available with and without Bid/Ask history. citeturn0search5turn0search12
- Therefore, TrueData is a **technically suitable acquisition route**, but it is not yet evidence that the complete 2024–2026 Phase 22 historical sample is accessible under a free/default account.
- The required next acquisition test is a vendor-authorized sample covering at least one historical NIFTY weekly-expiry session. The sample must demonstrate actual historical bid/ask timestamps and contract identifiers before any bulk acquisition or holdout opening.


## 22.1E — Global Datafeeds historical tick route (2026-09-30)

- Global Datafeeds documents historical NFO data with tick, minute and other periodicities. Its historical tick examples explicitly return **BuyPrice (Bid), BuyQty, SellPrice (Ask), SellQty, LastTradeTime, TradedQty and OpenInterest**. citeturn2search0turn2search15
- Its documentation gives NFO historical-data support and explicitly shows option/futures instrument identifiers; the tick response therefore matches the core executable-quote fields required by Phase 22. citeturn2search1turn2search14
- The remaining unknown is **historical retention for the exact 2024–2026 NIFTY weekly option contracts** and whether the required backfill is available under an authorized trial/subscription. The public documentation does not establish that full multi-year tick retention is freely accessible.
- Global Datafeeds is therefore promoted to **primary acquisition candidate alongside TrueData**, not admitted data.

### Acquisition test
The first authorized sample must contain at least one historical weekly NIFTY expiry session and verify: exact option symbol/expiry/strike/type, timestamp, bid, bid quantity, ask, ask quantity, trade price/quantity and OI. The sample will be hashed and stored as provenance evidence before any bulk acquisition.


## 22.1F — Newly identified public NIFTY TBT/depth dataset (2026-09-30)

- A new Hugging Face dataset, `antony9952/Nifty_option_TBT`, was identified during the expanded source search. Its preview contains timestamped NIFTY option observations with `instrument_key`, five depth levels (`depth_level=0..4`), `bid_price`, `bid_qty`, `ask_price`, and `ask_qty`. This field set directly overlaps the Phase 22 execution-data contract. citeturn2search0
- The dataset is currently **not admissible**. Hugging Face reports a dataset-generation/schema-cast failure because the underlying `market_ticks.csv` mixes depth-schema rows with a different 18-column LTP/OHLC/volume/OI schema. citeturn3view0
- The public preview demonstrates real depth observations (for example, five bid/ask levels at the same timestamp), but the public evidence inspected so far does not establish complete coverage of the required 2024–2026 target weekly expiries. The search did not verify the five Phase 21 recovery dates or the full prospective Phase 22 chronology from this source. citeturn3view0
- Therefore this source is promoted from “unknown” to **execution-data lead requiring direct file-level coverage/schema validation**, not to admitted data.
- No new holdout was opened and no strategy parameter was changed.

### Required validation for this source
1. Obtain the immutable dataset revision and raw file manifest.
2. Determine whether quote/depth rows can be isolated deterministically from the mixed file without imputing or altering observations.
3. Verify exact NIFTY option contract identity: expiry, strike, CE/PE, and instrument mapping.
4. Measure date/session coverage against the preregistered weekly chronology.
5. Hash the admitted raw subset and cache it in the Phase 22 workflow if—and only if—it passes the execution contract.
6. Reject the source if coverage is incomplete or contract identity cannot be reconstructed reproducibly.


## 22.1G — Licensed execution-data sources re-checked (2026-09-30)

### TrueData — technically suitable, access-gated
TrueData documentation explicitly states that its historical Market Data API can provide historical NSE Futures & Options data with Level-1 best bid/ask, and its historical REST interface supports tick history with bid/ask. Its support documentation also states that historical bid/ask data is available through its WebSocket API services. This is the strongest technically documented candidate found in the current audit, but no active TrueData credentials/subscription are available to this research workflow, so no data is admitted.

### Global Datafeeds — technically suitable, access-gated
Global Datafeeds documents NFO historical tick data and fields including BUYPRICE/BUYQTY and SELLPRICE/SELLQTY, and supports contract-specific NIFTY option identifiers. Its published backfill policy currently states only one calendar week of tick history for NFO, while minute history has shorter rolling windows. This makes it unsuitable for directly retrieving a multi-year historical sample unless an extended archive/custom extract is separately provisioned.

### TickBytes / OptionVault — coverage claims strong, archive access-gated
Public GitHub documentation describes daily NIFTY option-chain Level-2/top-5 depth archives and OptionVault describes historical NIFTY index-option tick/1-second and Level-2 data. However, the full datasets are licensed/private; public repositories expose samples/schema rather than the required chronological archive. They remain candidates for a licensed/custom extract, not admitted public sources.

### Public GitHub bid/ask schema projects
ayyararyan/nse-options-pipeline documents per-snapshot NIFTY option rows with bid/ask and quantities, but the underlying NSEI-Data archive is explicitly not tracked in Git. Therefore schema existence is verified, historical coverage is not.


## 22.1H — Additional public/retail historical-data candidates (2026-09-30)

### NiftyTrader historical option-chain page — candidate, not yet admitted
NiftyTrader publicly describes historical NIFTY option-chain snapshots with strike-wise LTP, IV, and bid/ask, and says premium access can export historical data in bulk. The page describes default end-of-day snapshots plus some premium intraday snapshots. This could be useful if the downloadable payload is genuinely historical bid/ask and can be exported reproducibly, but the current public page does not expose a machine-readable archive or immutable file hash. Therefore it is a candidate only and has not entered the Phase 22 data cache.

### optionsdata.shop — broad OHLC archive, execution quotes not established
The service advertises a large NIFTY 1-minute archive and expired-contract 1-minute/1-second archives spanning 2021–2026. The public description confirms OHLC/OI/volume coverage, but does not establish historical bid/ask fields. It therefore cannot replace the execution-data contract without a schema/sample proving quotes.
