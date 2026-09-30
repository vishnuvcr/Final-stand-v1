# Phase 21W External Full-Strike Recovery Error Log

## E21X-001 — 2026-09-30
- **Issue:** Earlier external source audit recorded broker/API routes as not tested.
- **Correction:** Expanded the audit with current endpoint/documentation evidence and separated documentary qualification from empirical admission.

## E21X-002 — 2026-09-30
- **Issue:** A public dataset with a matching per-expiry 1-minute option schema could be overlooked if only broker APIs were considered.
- **Correction:** Added thetrademarkk/india-index-options-1m as a candidate route and created a deterministic five-expiry probe.

## E21X-003 — 2026-09-30
- **Issue:** Public dataset presence does not guarantee full-strike coverage or acceptable licensing for later capital use.
- **Correction:** Probe exact missing expiries, record provenance, and carry the dataset's CC-BY-NC-4.0 / educational-use limitation into admission criteria.
