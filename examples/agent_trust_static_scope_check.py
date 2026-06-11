#!/usr/bin/env python3
"""Local Agent Trust static scope/manifest consistency check.

Compares self-declared tool/skill scopes with local manifest/lockfile-style
evidence. This is advisory static inspection only: it performs no network,
third-party code execution, wallet/signing/payment behavior, posting/outreach,
repo settings changes, or secret access.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_trust.bundle_boundaries import gate_static_scope_manifest_consistency


def _demo_request() -> dict[str, object]:
    return {
        "declared_scopes": ["read_local_docs", "summarize"],
        "manifest_evidence": {
            "observed_scopes": ["read_local_docs", "summarize"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="emit the built-in demo packet")
    parser.add_argument("--request-json", help="JSON request packet to evaluate")
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    args = parser.parse_args()

    if args.request_json:
        request = json.loads(args.request_json)
    elif args.demo:
        request = _demo_request()
    else:
        parser.error("use --demo or --request-json")

    packet = gate_static_scope_manifest_consistency(request)
    print(json.dumps(packet, sort_keys=True, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
