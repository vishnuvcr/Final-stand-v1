# Phase 22W Status

State: **ACTIVE — 22.1 and 22.2 complete; 22.3 configuration freeze complete; weekly-horizon interpretation clarified; broker/API and public-archive audit expanded; execution-data acquisition/admission still pending.**

- 224 configurations frozen.
- Execution-data contract frozen.
- Source audit completed.
- No paid data purchased.
- No new holdout opened.
- No Phase 21W configuration selected post hoc.
- The strategy is explicitly a **weekly-horizon weekly-expiry strategy with intraday execution timestamps**, not an intraday-only strategy.
- Protocol wording was corrected after the 2026-09-30 strategy-horizon clarification; no parameter or holdout data were changed.

Next gate: run the new manual TBT depth-source probe against the separate `market_depth.csv` file, then verify contract identity and weekly-expiry coverage. The file is now a higher-priority public candidate, but remains unadmitted until those checks pass. NSE full-order/full-trade, TrueData extended history and GFDL remain fallback acquisition routes. No new holdout until admission.

### 2026-09-30 execution-data status
- Public TBT candidate: rejected after actual workflow probe (2 dates, 57 invalid quote rows).
- Public/paid-source audit: TrueData and Global Datafeeds technically suitable but access-gated/rolling-window constrained; TickBytes/OptionVault licensed archive candidates.
- Current gate: execution-data acquisition remains the only blocker to Phase 22.4–22.7.
- Holdout remains locked; 224-config registry remains frozen.
