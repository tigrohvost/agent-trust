#!/usr/bin/env python3
"""Summarize local Agent Trust adoption readiness without external action.

This is a consumer-facing checkpoint for the current local packet. It runs only
local Python examples inside this checkout and performs no network calls, wallet
access, external tool execution, signing, payment, transaction, or real-money
behavior.
"""

from __future__ import annotations

import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs" / "examples"
CONTRACT_VERSION = "agent-trust-bundle-v1"
SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "execution": False,
    "real_money": False,
}
SCRIPT_PATHS = {
    "doctor": EXAMPLES / "agent_trust_doctor.py",
    "consumer_decision": EXAMPLES / "agent_trust_consumer_decision.py",
    "framework_gate": EXAMPLES / "agent_trust_framework_gate.py",
    "agent_security_evidence": EXAMPLES / "agent_trust_agent_security_evidence.py",
}

payloads: dict[str, dict[str, Any] | None] = {}
subprocess_evidence: list[dict[str, Any]] = []
subprocess_env = {
    **os.environ,
    "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT": "1",
    "AGENT_TRUST_DOCTOR_SKIP_PRELAUNCH": "1",
    "AGENT_TRUST_DAILY_REVIEW_ALLOW_DIRTY": "1",
    "AGENT_TRUST_DAILY_REVIEW_ALLOW_UNTAGGED": "1",
}
for name, path in SCRIPT_PATHS.items():
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=subprocess_env,
        check=False,
    )
    evidence: dict[str, Any] = {
        "command": f"python3 {path.relative_to(ROOT).as_posix()}",
        "exit_code": completed.returncode,
        "json_ok": False,
    }
    payload: dict[str, Any] | None = None
    try:
        parsed = json.loads(completed.stdout)
        if isinstance(parsed, dict):
            payload = parsed
            evidence["json_ok"] = True
        else:
            evidence["error"] = "top-level JSON was not an object"
    except json.JSONDecodeError as exc:
        evidence["error"] = f"invalid JSON: {exc}"
    if completed.returncode != 0 and "error" not in evidence:
        evidence["error"] = (completed.stderr or "subprocess returned non-zero status").strip()[:400]
    payloads[name] = payload
    subprocess_evidence.append(evidence)

doctor = payloads["doctor"]
consumer = payloads["consumer_decision"]
framework = payloads["framework_gate"]
agent_security = payloads["agent_security_evidence"]
framework_decision = framework.get("decision", {}) if isinstance(framework, dict) else {}
agent_security_move = agent_security.get("agent_trust_move", {}) if isinstance(agent_security, dict) else {}
doctor_ok = bool(doctor and doctor.get("ok") is True and doctor.get("checks_failed") == 0)
consumer_decision = consumer.get("decision") if isinstance(consumer, dict) else None
consumer_safety_ok = bool(consumer and consumer.get("ok") is True and consumer.get("safety_boundary") == SAFETY_BOUNDARY)
consumer_ok = bool(consumer_safety_ok and consumer_decision == "integrate_experimentally")
consumer_review_ok = bool(consumer_safety_ok and consumer_decision in {"integrate_experimentally", "abstain"})
framework_action = framework_decision.get("action")
framework_safety_ok = bool(
    framework
    and framework.get("action_performed") is False
    and framework_decision.get("safety_boundary") == SAFETY_BOUNDARY
)
framework_ok = bool(framework_safety_ok and framework_action == "review")
agent_security_boundary = agent_security.get("safety_boundary", {}) if isinstance(agent_security, dict) else {}
agent_security_ok = bool(
    agent_security
    and agent_security.get("ok") is True
    and agent_security_boundary.get("network_calls") is False
    and agent_security_boundary.get("wallet_access") is False
    and agent_security_boundary.get("external_tools_executed") is False
    and agent_security_boundary.get("external_scanners_executed") is False
    and agent_security_boundary.get("agent_action_performed") is False
    and agent_security_boundary.get("signing") is False
    and agent_security_boundary.get("payment") is False
    and agent_security_boundary.get("real_money") is False
    and agent_security_boundary.get("outreach") is False
    and agent_security_move.get("action") in {"deny", "review"}
)
local_adoption_ready = doctor_ok and consumer_ok and framework_ok and agent_security_ok
reviewer_ready = doctor_ok and consumer_review_ok and framework_ok and agent_security_ok
ok = reviewer_ready
validation = doctor.get("validation_summary", {}) if isinstance(doctor, dict) else {}
review_readiness = doctor.get("review_readiness", {}) if isinstance(doctor, dict) else {}
must_stop_before = list(consumer.get("must_stop_before", [])) if isinstance(consumer, dict) else []
must_stop_before.extend(review_readiness.get("not_proven_by_this_packet", []))

print(json.dumps({
    "ok": ok,
    "contract_version": CONTRACT_VERSION,
    "checkpoint": "agent_trust_adoption_readiness",
    "safety_boundary": SAFETY_BOUNDARY,
    "adoption_readiness": {
        "ready_for_local_adoption_experiment": local_adoption_ready,
        "ready_for_reviewer_handoff": reviewer_ready,
        "posture": "integrate_experimentally_with_human_review_gate" if reviewer_ready else "not_ready",
        "recommended_path": "bash scripts/agent_trust_first_run.sh",
        "integration_context": validation.get("integration_context"),
        "consumer_decision": consumer.get("decision") if isinstance(consumer, dict) else None,
        "framework_gate_action": framework_decision.get("action"),
        "risky_action_performed": framework.get("action_performed") if isinstance(framework, dict) else None,
        "next_smallest_safe_step": "show this local checkpoint plus the first-run proof and sanitized agent-security evidence ask to a reviewer; stop before outreach, hosted service, wallet, facilitator, signing, payment, or legal/compliance commitments",
        "next_acquisition_ask": "send one sanitized agent memory/planning/tool/MCP/payment/contact risk summary with task-warrant fields so Agent Trust can return proceed/review/deny before action",
    },
    "local_evidence": {
        "doctor": {
            "ok": doctor_ok,
            "checks_total": doctor.get("checks_total") if isinstance(doctor, dict) else None,
            "checks_failed": doctor.get("checks_failed") if isinstance(doctor, dict) else None,
            "command": subprocess_evidence[0]["command"],
        },
        "consumer_decision": {
            "ok": consumer_ok,
            "reviewer_ready": consumer_review_ok,
            "decision": consumer_decision,
            "command": subprocess_evidence[1]["command"],
        },
        "framework_gate": {
            "ok": framework_ok,
            "action": framework_action,
            "action_performed": framework.get("action_performed") if isinstance(framework, dict) else None,
            "command": subprocess_evidence[2]["command"],
        },
        "agent_security_evidence": {
            "ok": agent_security_ok,
            "action": agent_security_move.get("action"),
            "command": subprocess_evidence[3]["command"],
        },
    },
    "not_proven_external_claims": review_readiness.get("not_proven_by_this_packet", []),
    "must_stop_before": sorted(set(str(item) for item in must_stop_before if item)),
    "subprocess_evidence": subprocess_evidence,
}, sort_keys=True, indent=2, ensure_ascii=False))
sys.exit(0 if reviewer_ready else 1)
