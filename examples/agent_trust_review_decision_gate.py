#!/usr/bin/env python3
"""Emit the local Agent Trust reviewer decision gate.

This turns the evidence transcript into an explicit review decision boundary.
It performs only local Python subprocess inspection and authorizes no outreach,
wallet access, signing, live testnet call, payment, or real-money behavior.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs" / "examples"
EXPECTED_SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "external_execution": False,
    "signing": False,
    "payment": False,
    "real_money": False,
    "outreach": False,
}

command = [sys.executable, str(EXAMPLES / "agent_trust_evidence_transcript.py")]
env = {
    **os.environ,
    "AGENT_TRUST_DAILY_REVIEW_ALLOW_DIRTY": "1",
    "AGENT_TRUST_DAILY_REVIEW_ALLOW_UNTAGGED": "1",
    "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT": "1",
}
completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env=env, check=False)
transcript: dict[str, object] = {}
error = ""
if completed.returncode == 0:
    try:
        loaded = json.loads(completed.stdout)
        transcript = loaded if isinstance(loaded, dict) else {}
    except json.JSONDecodeError as exc:
        error = f"evidence transcript emitted non-json output: {exc}"
else:
    error = completed.stderr.strip() or completed.stdout.strip() or "evidence transcript failed"

evidence = transcript.get("evidence", []) if isinstance(transcript, dict) else []
evidence_names = [item.get("name") for item in evidence if isinstance(item, dict)]
evidence_all_ok = bool(evidence) and all(item.get("ok") is True for item in evidence if isinstance(item, dict))
boundary_ok = transcript.get("safety_boundary") == EXPECTED_SAFETY_BOUNDARY
provenance_evidence = transcript.get("provenance_evidence", {})
provenance_ok = (
    isinstance(provenance_evidence, dict)
    and provenance_evidence.get("classification") == "provenance_evidence_not_trust"
    and "policy_evaluation" in provenance_evidence.get("still_requires", [])
    and "work_warrant_or_action_scope" in provenance_evidence.get("still_requires", [])
    and "action_boundary_check" in provenance_evidence.get("still_requires", [])
    and "tool_or_mcp_use" in provenance_evidence.get("does_not_authorize", [])
    and "wallet_access" in provenance_evidence.get("does_not_authorize", [])
    and "payment" in provenance_evidence.get("does_not_authorize", [])
)
transcript_ok = (
    completed.returncode == 0
    and transcript.get("ok") is True
    and evidence_all_ok
    and boundary_ok
    and provenance_ok
)
decision = "ready_for_human_or_agent_review_only" if transcript_ok else "repair_local_evidence_before_review"

gate = {
    "ok": transcript_ok,
    "artifact": "agent_trust_review_decision_gate",
    "contract_version": "agent-trust-bundle-v1",
    "input": {
        "command": "python3 examples/agent_trust_evidence_transcript.py",
        "artifact": transcript.get("artifact"),
        "ok": transcript.get("ok"),
        "evidence_names": evidence_names,
        "provenance_classification": provenance_evidence.get("classification") if isinstance(provenance_evidence, dict) else None,
    },
    "safety_boundary": EXPECTED_SAFETY_BOUNDARY,
    "provenance_evidence_check": {
        "ok": provenance_ok,
        "classification": provenance_evidence.get("classification") if isinstance(provenance_evidence, dict) else None,
        "meaning": "DNS-AID/ANS-style discovery and identity claims are reviewer-visible provenance evidence, not trust or action authorization.",
        "still_requires": provenance_evidence.get("still_requires", []) if isinstance(provenance_evidence, dict) else [],
        "does_not_authorize": provenance_evidence.get("does_not_authorize", []) if isinstance(provenance_evidence, dict) else [],
    },
    "status": "ready" if transcript_ok else "needs_repair",
    "ready_for_review": transcript_ok,
    "decision": decision,
    "next_step": (
        "share_or_inspect_this_local_transcript_with_a_human_or_agent_reviewer"
        if transcript_ok
        else "repair_the_failing_local_evidence_command_before_any_review"
    ),
    "refusals": [
        "publication_or_outreach",
        "hosted_endpoint_or_uptime_claims",
        "wallet_access_or_private_key_handling",
        "signing_or_x402_payment_submission",
        "Base_Sepolia_live_network_call",
        "mainnet_or_real_money_activity",
        "legal_compliance_or_customer_commitment_claims",
    ],
    "reviewer_may_decide": [
        "whether the local Agent Trust packet is coherent enough for an experimental pre-action integration review",
        "whether additional local evidence or schema/documentation repair is needed",
        "whether a separate explicitly bounded outreach or Base Sepolia live-testnet proposal should be prepared",
    ],
    "authorized_next_actions": (
        [
            "share_or_inspect_this_local_transcript_with_a_human_or_agent_reviewer",
            "run_a_local_integration_experiment_with_a_human_review_gate",
            "prepare_a_separate_bounded_proposal_for_outreach_or_live_testnet_if_review_approves",
        ]
        if transcript_ok
        else ["repair_the_failing_local_evidence_command_before_any_review"]
    ),
    "not_authorized_next_actions": [
        "publication_or_outreach",
        "hosted_endpoint_or_uptime_claims",
        "wallet_access_or_private_key_handling",
        "signing_or_x402_payment_submission",
        "Base_Sepolia_live_network_call",
        "mainnet_or_real_money_activity",
        "legal_compliance_or_customer_commitment_claims",
    ],
    "requires_explicit_separate_authorization_before": [
        "contacting external people or accounts",
        "publishing an endpoint, claim, or announcement",
        "using secrets, wallets, private keys, or facilitator credentials",
        "performing any live network payment-like action including Base Sepolia",
        "spending real money or making legal/customer commitments",
    ],
    "interpretation": (
        "Evidence is locally coherent; provenance signals are visible for review, but the only approved next movement is review, not external action."
        if transcript_ok
        else "Local evidence is not coherent enough for review; repair it before proceeding."
    ),
}
if error:
    gate["error"] = error
print(json.dumps(gate, indent=2, sort_keys=True))
raise SystemExit(0 if transcript_ok else 1)
