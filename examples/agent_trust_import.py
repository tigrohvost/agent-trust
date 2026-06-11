#!/usr/bin/env python3
"""Direct in-process Agent Trust Bundle example.

Run from the repository root:

    python3 examples/agent_trust_import.py

This calls the local builder directly. It performs no network calls, no wallet
access, no tool execution, and no real-money action.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_trust.bundle import build_agent_trust_bundle  # noqa: E402


bundle = build_agent_trust_bundle(
    policy={
        "agent_id": "demo-agent",
        "settlement": "mock-local-no-money-policy",
        "allowed_resources": ["https://api.example.test/report"],
        "per_request_cap": "0.10",
        "per_agent_budget_cap": "1.00",
    },
    ledger=[{"agent_id": "demo-agent", "amount": "0.25", "payment_id": "paid-001"}],
    resource="https://api.example.test/report",
    tool_descriptor={
        "name": "example-report-api",
        "kind": "mcp_server",
        "transport": "https",
        "auth": "env:EXAMPLE_API_KEY",
        "read_only": True,
    },
    contract_version="agent-trust-bundle-v1",
)
print(json.dumps(bundle, indent=2, sort_keys=True))
