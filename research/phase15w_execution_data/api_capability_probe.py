#!/usr/bin/env python3
"""Phase 15W API capability probe.

This script performs a single-contract/single-session probe when credentials are
provided. It never places orders and never reads the Phase 13 holdout.

The script intentionally treats OHLC-only responses as a failed BBO probe.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

OUT = Path(os.getenv("PHASE15W_OUT", "research/phase15w_execution_data/probe_output"))
OUT.mkdir(parents=True, exist_ok=True)

def save(name, payload):
    (OUT / name).write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required credential/environment variable: {name}")
    return value

def main():
    provider = os.getenv("PHASE15W_PROVIDER", "").lower()
    if provider not in {"truedata", "dhan", "breeze", "upstox"}:
        raise SystemExit("Set PHASE15W_PROVIDER to truedata, dhan, breeze, or upstox.")

    # This is deliberately a capability gate. Provider-specific authenticated
    # requests should be implemented only after the account's documented API
    # contract is confirmed; no credential is stored in the repository.
    result = {
        "provider": provider,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "credential_required",
        "bbo_qualified": False,
        "holdout_read": False,
        "strategy_parameters_changed": False,
        "message": "Provider-specific credentials/access are required for an empirical probe."
    }

    save("probe_status.json", result)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
