from pathlib import Path
import json

OUT = Path("research/phase21w_external_full_strike_recovery/output")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    "2026-01-13",
    "2026-02-10",
    "2026-03-10",
    "2026-04-13",
    "2026-05-12",
]

rows = [
    {
        "source": "RISSIN / Hugging Face",
        "route": "rissin/nse-options-intraday; upstox_intraday/NIFTY/NIFTY_2026.parquet",
        "status": "candidate — pinned public 1-minute archive",
        "revision": "78b1c5468255d18cf492984bfe6fe4e3ac874d7c",
        "documented_fields": ["expiry", "strike", "option_type", "open", "high", "low", "close", "volume"],
        "documented_coverage": "NIFTY 1-minute intraday from Oct 2024 through 2026",
        "oi_status": "intraday OI documented as unavailable",
        "admission": "automated five-expiry full-variant probe in this workflow",
    },
    {
        "source": "Upstox",
        "route": "expired option contracts / historical 1-minute candles",
        "status": "requires credentials/entitlement for direct API access",
        "admission": "fallback if public RISSIN recovery fails",
    },
    {
        "source": "ICICI Breeze",
        "route": "historical option data API",
        "status": "requires API credentials/session",
        "admission": "fallback if public RISSIN recovery fails",
    },
    {
        "source": "Dhan",
        "route": "expired options / historical API",
        "status": "requires API credentials/session",
        "admission": "fallback if public RISSIN recovery fails",
    },
    {
        "source": "NSE/BSE",
        "route": "exchange-published derivatives archives",
        "status": "public/controlled access varies; full intraday strike reconstruction is not yet verified for the five targets",
        "admission": "secondary provenance/cross-check only until exact 1-minute bars are demonstrated",
    },
    {
        "source": "MoneyTicks",
        "route": "public expired-options catalogue / authenticated API",
        "status": "catalog documents 1-minute NIFTY archive, but programmatic raw access is gated",
        "admission": "last-resort external route; do not purchase or substitute data without explicit authorization",
    },
    {
        "source": "HF-03 / HF-02 existing recovery",
        "route": "frozen Phase 21 combined input",
        "status": "already admitted for 58 expiries",
        "admission": "must not be replaced or mixed with external bars",
    },
]

report = {
    "phase": "21W",
    "targets": TARGETS,
    "rows": rows,
    "rules": [
        "No synthetic/interpolated bars.",
        "No cross-source leg mixing within an expiry cycle.",
        "External data can fill only the five currently missing target expiries.",
        "The frozen 224 variants, train/validation/holdout split, costs, slippage and stop rules remain unchanged.",
    ],
}

(OUT / "source_access_audit.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
