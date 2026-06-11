#!/usr/bin/env python3
"""Framework-shaped Agent Trust pre-action gate example.

Run from the repository root:

    python3 examples/agent_trust_framework_gate.py

This dependency-free sketch shows where an agent framework, workflow engine,
or MCP/tool runner would call Agent Trust before a risky action. It performs no
network calls, no wallet access, no external tool execution, and no real-money
action; the action is a local mock decision only.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_trust.bundle import build_agent_trust_bundle  # noqa: E402

risky_tool_call = {
    "name": "example-report-api",
    "kind": "mcp_server",
    "transport": "https",
    "auth": "env:EXAMPLE_API_KEY",
    "read_only": True,
}
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
    tool_descriptor=risky_tool_call,
    contract_version="agent-trust-bundle-v1",
    intended_integration_context="agent_framework_pre_action_gate_before_mcp_tool_or_paid_api_call",
)
verdict = bundle.get("verdict")
if verdict == "allow":
    action = "proceed"
    reason = "bundle_allows_pre_action"
elif verdict == "deny":
    action = "deny"
    reason = "bundle_denies_pre_action"
else:
    action = "review"
    reason = "bundle_requires_human_or_policy_review"

print(json.dumps({
    "example": "agent_trust_framework_gate",
    "risky_action": "mock_mcp_tool_call",
    "action_performed": False,
    "decision": {
        "action": action,
        "reason": reason,
        "bundle_id": bundle.get("bundle_id"),
        "bundle_verdict": verdict,
        "bundle_reasons": bundle.get("reasons", []),
        "safety_boundary": {
            "network_calls": False,
            "wallet_access": False,
            "execution": False,
            "real_money": False,
        },
    },
}, indent=2, sort_keys=True))
