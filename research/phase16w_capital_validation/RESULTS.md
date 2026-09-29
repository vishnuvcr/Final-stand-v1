# Phase 16W — Capital and Margin Validation: Final Status

## Result
**Phase closed with a quantified historical-margin data gap. No capital-normalized performance claim is admitted.**

The phase successfully froze the 63-cycle cycle-date/strike interface and verified the deterministic research gate. A historical NSE SPAN acquisition probe was then run against the required 2024–2026 dates.

### Acquisition audit
- Required years: 2024, 2025, 2026.
- Required unique dates: 193.
- Static archive candidates tested per year: 6.
- Total candidate URL attempts: 18.
- Successful historical SPAN downloads: 0.
- Dated SPAN members recovered: 0.
- Therefore: empirical SPAN margin reconstruction coverage = 0/63 cycles.

NSE's official derivatives reports page confirms that historical F&O SPAN BOD, 1st–4th intraday and EOD reports are offered. The blocker is reproducible access to those historical report files through the available static archive routes, not an assumption that the reports do not exist.

## What can and cannot be concluded

### Can be concluded
1. The frozen strategy remains the Phase 13/14 strategy; no capital-data failure changed its parameters.
2. The historical rupee P&L results remain valid as the previously reported OHLC-reconstructed results, subject to their documented execution-data limitations.
3. A defensible historical peak-capital series cannot be produced from zero admitted SPAN observations.
4. Any capital-normalized Sharpe, return-on-capital, margin utilization, or broker-buffer result would require an assumption or substitution not supported by historical evidence and is therefore not reported.

### Cannot be concluded
- Exact historical broker margin requirement.
- Exact historical SPAN requirement at 10:00 entry or 14:00 lock.
- Historical intraday peak margin.
- Historical return on peak capital.
- Historical capital drawdown.
- Broker-specific additional buffers/pledge treatment.

## Reproducibility artifacts
- `frozen_cycle_manifest.csv` — frozen 63-cycle dates, strikes and data-status interface.
- `span_acquisition.py` — bounded candidate-URL probe with checksums and HTTP diagnostics.
- Workflow run 36627668048.
- Artifact 11060409066 — `span_manifest.json`, including all 18 failed URL attempts.

## Disposition
Phase 16W is closed under its preregistered stopping rule. No strategy tuning was performed and the Phase 13 holdout remains locked.

### Future research requirement
To complete capital validation, obtain one of:
1. licensed historical NSE/NSCCL risk-parameter files;
2. a broker/clearing-member historical margin ledger for the exact position path;
3. authenticated access to NSE's dynamic historical-report download mechanism.

Until then, capital-normalized results must remain explicitly unavailable.
