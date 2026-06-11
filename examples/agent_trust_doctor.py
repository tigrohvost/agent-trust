#!/usr/bin/env python3
"""Standalone consistency doctor for the public Agent Trust repository.

Local only: no network calls, no wallet access, no signing, no payments, and no
external tool execution. It runs only this checkout's Python entry points.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
SCHEMAS = ROOT / "schemas"
REQUIRED = [
    ROOT / "README.md",
    ROOT / "agent_trust" / "bundle.py",
    ROOT / "agent_trust" / "cli.py",
    EXAMPLES / "input.json",
    EXAMPLES / "output.json",
    EXAMPLES / "agent_trust_request.py",
    EXAMPLES / "agent_trust_verify.py",
    EXAMPLES / "agent_trust_manifest.json",
    EXAMPLES / "agent_trust_review_packet.json",
    SCHEMAS / "agent_trust_request.schema.json",
    SCHEMAS / "agent_trust_bundle.schema.json",
    SCHEMAS / "agent_trust_manifest.schema.json",
]

checks: list[dict[str, object]] = []
for path in REQUIRED:
    checks.append({"code": f"required:{path.relative_to(ROOT)}", "ok": path.exists(), "message": "present" if path.exists() else "missing"})

bundle = subprocess.run([sys.executable, "-m", "agent_trust.cli", "examples/input.json"], cwd=ROOT, text=True, capture_output=True, check=False)
if bundle.returncode == 0:
    try:
        current = json.loads(bundle.stdout)
        expected = json.loads((EXAMPLES / "output.json").read_text(encoding="utf-8"))
        comparable_keys = ["contract_version", "verdict", "reasons", "controls", "network_calls", "wallet_access", "execution", "settlement"]
        checks.append({
            "code": "cli_matches_golden_public_fields",
            "ok": all(current.get(k) == expected.get(k) for k in comparable_keys),
            "message": "CLI output matches golden public fields",
        })
        checks.append({"code": "bundle_id_present", "ok": str(current.get("bundle_id", "")).startswith("agenttrust-"), "message": "bundle id emitted"})
    except json.JSONDecodeError as exc:
        checks.append({"code": "cli_json", "ok": False, "message": f"invalid CLI JSON: {exc}"})
else:
    checks.append({"code": "cli_runs", "ok": False, "message": bundle.stderr.strip() or bundle.stdout.strip() or "CLI failed"})

verify = subprocess.run([sys.executable, "examples/agent_trust_verify.py"], cwd=ROOT, text=True, capture_output=True, check=False)
checks.append({"code": "golden_verifier_runs", "ok": verify.returncode == 0, "message": verify.stdout.strip() if verify.returncode == 0 else (verify.stderr.strip() or verify.stdout.strip())})

manifest = json.loads((EXAMPLES / "agent_trust_manifest.json").read_text(encoding="utf-8")) if (EXAMPLES / "agent_trust_manifest.json").exists() else {}
checks.append({"code": "manifest_names_first_run", "ok": "first" in json.dumps(manifest, sort_keys=True).lower(), "message": "manifest contains first-run/discovery data"})

ok = all(bool(c["ok"]) for c in checks)
summary = {
    "ok": ok,
    "artifact": "agent_trust_public_doctor",
    "safety_boundary": {"network_calls": False, "wallet_access": False, "execution": False, "real_money": False},
    "validation_summary": {
        "required_artifacts": len(REQUIRED),
        "checks": len(checks),
        "failed": [c for c in checks if not c["ok"]],
        "root_digest": hashlib.sha256("\n".join(sorted(str(p.relative_to(ROOT)) for p in REQUIRED if p.exists())).encode()).hexdigest(),
    },
    "checks": checks,
}
print(json.dumps(summary, sort_keys=True, indent=2))
raise SystemExit(0 if ok else 1)
