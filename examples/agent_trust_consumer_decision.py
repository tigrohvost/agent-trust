#!/usr/bin/env python3
"""Example external-agent decision over the Agent Trust examples packet.

Local only: reads checked-in Agent Trust artifacts and runs the local doctor.
It makes no network calls, reads no wallet material, performs no real-money
activity, and does not execute external tools.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs" / "examples"
CONTRACT_VERSION = "agent-trust-bundle-v1"
SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "execution": False,
    "real_money": False,
}

manifest = json.loads((EXAMPLES / "agent_trust_manifest.json").read_text(encoding="utf-8"))
review_packet = json.loads((EXAMPLES / "agent_trust_review_packet.json").read_text(encoding="utf-8"))
completed = subprocess.run(
    [sys.executable, str(EXAMPLES / "agent_trust_doctor.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
    env={
        **os.environ,
        "AGENT_TRUST_SKIP_CONSUMER_DECISION": "1",
        "AGENT_TRUST_DOCTOR_SKIP_EVIDENCE_TRANSCRIPT": "1",
        "AGENT_TRUST_DOCTOR_SKIP_PRELAUNCH": "1",
        "AGENT_TRUST_DAILY_REVIEW_ALLOW_DIRTY": "1",
        "AGENT_TRUST_DAILY_REVIEW_ALLOW_UNTAGGED": "1",
    },
)
doctor = json.loads(completed.stdout) if completed.returncode == 0 else {
    "ok": False,
    "checks_failed": 1,
    "error": completed.stderr.strip() or completed.stdout.strip() or "doctor failed",
}
review_commands = {
    item["command"]
    for item in review_packet.get("local_proof_commands", [])
    if isinstance(item, dict) and isinstance(item.get("command"), str)
}
manifest_commands = {
    item["command"]
    for item in manifest.get("entrypoints", [])
    if isinstance(item, dict) and isinstance(item.get("command"), str)
}
manifest_boundary = manifest.get("safety_boundary")
review_boundary = review_packet.get("safety_boundary")
evidence = {
    "manifest_contract_version_ok": manifest.get("contract_version") == CONTRACT_VERSION,
    "review_packet_contract_version_ok": review_packet.get("contract_version") == CONTRACT_VERSION,
    "manifest_safety_boundary_ok": isinstance(manifest_boundary, dict) and all(manifest_boundary.get(key) is value for key, value in SAFETY_BOUNDARY.items()),
    "review_packet_safety_boundary_ok": isinstance(review_boundary, dict) and all(review_boundary.get(key) is value for key, value in SAFETY_BOUNDARY.items()),
    "doctor_ok": bool(doctor.get("ok")) and doctor.get("checks_failed") == 0,
    "first_run_command_present": "bash scripts/agent_trust_first_run.sh" in review_commands,
    "doctor_command_present": "python3 examples/agent_trust_doctor.py" in review_commands,
    "manifest_entrypoint_present": "python3 examples/agent_trust_doctor.py" in manifest_commands,
}
should_integrate = all(evidence.values())
print(json.dumps({
    "ok": True,
    "contract_version": CONTRACT_VERSION,
    "decision": "integrate_experimentally" if should_integrate else "abstain",
    "reason": "local packet evidence is coherent and bounded" if should_integrate else "required local evidence is missing or failed",
    "recommended_path": "bash scripts/agent_trust_first_run.sh" if should_integrate else None,
    "safety_boundary": SAFETY_BOUNDARY,
    "evidence": evidence,
    "doctor_checks_failed": doctor.get("checks_failed"),
    "must_stop_before": review_packet.get("stop_conditions", []),
}, sort_keys=True, indent=2, ensure_ascii=False))
