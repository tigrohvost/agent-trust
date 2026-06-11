#!/usr/bin/env python3
"""Local Agent Trust Zero-Trust identity/policy pre-action gate demo.

This example performs no network calls, execution, secret reads, wallet/signing,
payment, posting, outreach, or repository-setting changes. It prints a JSON
pre-action receipt for review.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_trust.bundle_boundaries import gate_zero_trust_agent_action


def _demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "summarize_checked_in_agent_trust_doc",
        "required_scopes": ["read_local_docs"],
        "granted_scopes": ["read_local_docs", "write_local_receipt"],
        "sensitivity": "low",
        "provenance": {"source": "checked_in", "path": "docs/AGENT_TRUST.md"},
        "scanner_signals": ["no_known_risky_signal"],
        "description": "Create a local review summary without external side effects.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="emit a built-in low-risk proceed demo")
    parser.add_argument("--file", type=Path, help="read a JSON request from a local file")
    parser.add_argument("--compact", action="store_true", help="print compact JSON")
    args = parser.parse_args(argv)

    if args.demo:
        request = _demo_request()
    elif args.file:
        request = json.loads(args.file.read_text())
    else:
        request = json.loads(sys.stdin.read())

    packet = gate_zero_trust_agent_action(request)
    print(json.dumps(packet, ensure_ascii=False, sort_keys=True, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
