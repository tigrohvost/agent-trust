#!/usr/bin/env python3
"""Emit a reviewer-facing local Agent Trust evidence transcript.

Inert local proof only: no network, wallet, signing, transaction, payment,
outreach, or real-money behavior.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs" / "examples"
SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "external_execution": False,
    "signing": False,
    "payment": False,
    "real_money": False,
    "outreach": False,
}
PROVENANCE_EVIDENCE = {
    "signals": [
        "dns_aid_style_discovery_claims",
        "ans_style_identity_claims",
    ],
    "classification": "provenance_evidence_not_trust",
    "records": "Discovery and identity claims may help locate an agent, MCP endpoint, or declared operator.",
    "does_not_authorize": [
        "tool_or_mcp_use",
        "api_call",
        "wallet_access",
        "signing",
        "payment",
        "outreach",
    ],
    "still_requires": [
        "policy_evaluation",
        "work_warrant_or_action_scope",
        "risk_review",
        "action_boundary_check",
    ],
}
COMMANDS = [
    (
        "doctor",
        [sys.executable, str(EXAMPLES / "agent_trust_doctor.py")],
        "Validate examples, schemas, manifest, checksums, and golden output consistency.",
    ),
    (
        "adoption_readiness",
        [sys.executable, str(EXAMPLES / "agent_trust_adoption_readiness.py")],
        "Summarize whether local evidence supports experimental adoption with a human review gate.",
    ),
    (
        "daily_review",
        [sys.executable, str(EXAMPLES / "agent_trust_daily_review.py")],
        "Check release posture, local consistency, Base Sepolia dry-run boundary, and adoption readiness.",
    ),
    (
        "loopback_readiness",
        [sys.executable, str(EXAMPLES / "agent_trust_loopback_readiness.py")],
        "Prove the dedicated 8766-style Agent Trust path locally on 127.0.0.1 without hosted availability claims.",
    ),
]

skip_nested_doctor = os.environ.get("AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT") == "1"
env = os.environ.copy()
env.setdefault("AGENT_TRUST_DAILY_REVIEW_ALLOW_DIRTY", "1")
env.setdefault("AGENT_TRUST_DAILY_REVIEW_ALLOW_UNTAGGED", "1")
env.setdefault("AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT", "1")
evidence = []
for name, command, purpose in COMMANDS:
    if name == "doctor" and skip_nested_doctor:
        payload = {
            "ok": True,
            "checks_total": None,
            "checks_failed": None,
            "nested_doctor_skipped": True,
            "skip_reason": "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT avoids doctor -> transcript -> doctor recursion",
        }
        error = ""
    elif name == "daily_review" and skip_nested_doctor:
        payload = {
            "ok": True,
            "nested_daily_review_skipped": True,
            "skip_reason": "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT avoids daily_review -> doctor -> prelaunch -> transcript recursion",
            "next_step": "continue_parent_doctor_or_prelaunch_check",
            "review": {
                "latest_agent_trust_release": {},
                "adoption_posture": None,
                "adoption_recommended_path": None,
            },
        }
        error = ""
    elif name == "loopback_readiness" and skip_nested_doctor:
        payload = {
            "ok": True,
            "nested_loopback_readiness_skipped": True,
            "skip_reason": "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT avoids dependency-heavy loopback proof inside doctor/prelaunch; direct reviewer transcript still runs it",
            "decision": "skipped_inside_parent_doctor_or_prelaunch_check",
        }
        error = ""
    else:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        payload = {}
        error = ""
        output = completed.stdout.strip() or completed.stderr.strip()
        if output:
            try:
                payload = json.loads(output)
            except json.JSONDecodeError as exc:
                error = f"non-json output: {exc}"
        if completed.returncode != 0 and not error:
            error = completed.stderr.strip() or completed.stdout.strip()
    dependency_unavailable = (
        name == "loopback_readiness"
        and payload.get("ok") is False
        and payload.get("decision") == "runtime_dependency_unavailable"
    )
    ok = bool(payload.get("ok") is True or dependency_unavailable)
    if name == "doctor":
        summary = {
            "ok": payload.get("ok"),
            "checks_total": payload.get("checks_total"),
            "checks_failed": payload.get("checks_failed"),
            "nested_doctor_skipped": payload.get("nested_doctor_skipped", False),
            "skip_reason": payload.get("skip_reason"),
        }
    elif name == "adoption_readiness":
        readiness = payload.get("adoption_readiness", {})
        summary = {
            "ok": payload.get("ok"),
            "posture": readiness.get("posture"),
            "recommended_path": readiness.get("recommended_path"),
            "risky_action_performed": readiness.get("risky_action_performed"),
        }
    elif name == "daily_review":
        review = payload.get("review", {})
        latest_release = review.get("latest_agent_trust_release", {})
        summary = {
            "ok": payload.get("ok"),
            "latest_release": latest_release.get("version"),
            "latest_release_title": latest_release.get("title"),
            "next_step": payload.get("next_step"),
            "adoption_posture": review.get("adoption_posture"),
            "adoption_recommended_path": review.get("adoption_recommended_path"),
            "nested_daily_review_skipped": payload.get("nested_daily_review_skipped", False),
            "skip_reason": payload.get("skip_reason"),
        }
    else:
        summary = {
            "ok": payload.get("ok"),
            "decision": payload.get("decision"),
            "gate_decision": payload.get("gate_decision"),
            "recent_hard_timeouts": payload.get("recent_hard_timeouts"),
            "health_status": payload.get("health_status"),
            "health_service": payload.get("health_service"),
            "probe_decision": payload.get("probe_decision"),
            "probe_ok": payload.get("probe_ok"),
            "edge_path_checks": payload.get("edge_path_checks"),
            "nested_loopback_readiness_skipped": payload.get("nested_loopback_readiness_skipped", False),
            "dependency_unavailable": dependency_unavailable,
            "missing_dependencies": payload.get("missing_dependencies"),
            "skip_reason": payload.get("skip_reason"),
        }
    rendered_command = []
    for part in command:
        if part == sys.executable:
            rendered_command.append("python3")
        else:
            try:
                rendered_command.append(str(Path(part).relative_to(ROOT)))
            except ValueError:
                rendered_command.append(str(part))
    record = {
        "name": name,
        "command": " ".join(rendered_command),
        "purpose": purpose,
        "ok": ok,
        "summary": summary,
    }
    if error:
        record["error"] = error
    evidence.append(record)

all_ok = all(item["ok"] for item in evidence)
transcript = {
    "ok": all_ok,
    "artifact": "agent_trust_reviewer_evidence_transcript",
    "contract_version": "agent-trust-bundle-v1",
    "safety_boundary": SAFETY_BOUNDARY,
    "provenance_evidence": PROVENANCE_EVIDENCE,
    "reviewer_question": "Is this local Agent Trust packet coherent enough for an experimental pre-action integration review?",
    "evidence": evidence,
    "interpretation": (
        "Local evidence is coherent enough for reviewer inspection without external action; DNS-AID/ANS-style discovery or identity is recorded only as provenance evidence, not action authorization."
        if all_ok
        else "One or more required local evidence commands failed; inspect evidence[].error before review."
    ),
    "must_stop_before": [
        "outreach or publication",
        "hosted endpoint claims",
        "wallet access or private-key handling",
        "signing or x402 payment submission",
        "mainnet or real-money activity",
        "legal, compliance, or customer commitment claims",
    ],
    "next_smallest_safe_step": (
        "Use this transcript as the local attachment for a human or agent reviewer before any outreach."
        if all_ok
        else "Repair the failing local evidence command before using the transcript."
    ),
}
print(json.dumps(transcript, indent=2, sort_keys=True))
raise SystemExit(0 if all_ok else 1)
