#!/usr/bin/env python3
"""Verify the public Agent Trust CLI against the checked-in golden output."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "input.json"
EXPECTED = ROOT / "examples" / "output.json"
SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "execution": False,
    "real_money": False,
}

completed = subprocess.run(
    [sys.executable, "-m", "agent_trust.cli", str(INPUT.relative_to(ROOT))],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if completed.returncode != 0:
    print(json.dumps({
        "ok": False,
        "matches_golden": False,
        "error": {"code": "agent_trust_cli_failed", "message": completed.stderr.strip() or completed.stdout.strip()},
        "input": str(INPUT.relative_to(ROOT)),
        "expected_output": str(EXPECTED.relative_to(ROOT)),
        "safety_boundary": SAFETY_BOUNDARY,
    }, sort_keys=True, indent=2))
    raise SystemExit(2)

actual = json.loads(completed.stdout)
expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
comparable_keys = [
    "contract_version",
    "verdict",
    "reasons",
    "controls",
    "network_calls",
    "wallet_access",
    "execution",
    "settlement",
]
matches = all(actual.get(key) == expected.get(key) for key in comparable_keys)
print(json.dumps({
    "ok": matches,
    "matches_golden": matches,
    "contract_version": actual.get("contract_version"),
    "verdict": actual.get("verdict"),
    "bundle_id": actual.get("bundle_id"),
    "checked_fields": comparable_keys,
    "input": str(INPUT.relative_to(ROOT)),
    "expected_output": str(EXPECTED.relative_to(ROOT)),
    "safety_boundary": SAFETY_BOUNDARY,
}, sort_keys=True, indent=2))
raise SystemExit(0 if matches else 1)
