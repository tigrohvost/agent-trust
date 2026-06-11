"""Command-line contract for local Agent Trust Bundle checks.

This module performs no network calls, no wallet access, and no tool execution.
It only reads a JSON action description and prints the deterministic trust bundle.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agent_trust.bundle import (
    AGENT_TRUST_BUNDLE_CONTRACT_VERSION,
    AGENT_TRUST_MAX_JSON_INPUT_BYTES,
    AGENT_TRUST_MAX_JSON_NESTING_DEPTH,
    SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS,
    AgentTrustInputGuardError,
    build_agent_trust_bundle,
    guard_agent_trust_json_depth,
    guard_agent_trust_json_text,
)


AGENT_TRUST_CLI_CONTRACT = {
    "contract": "agent-trust-cli",
    "version": "agent-trust-cli-v1",
    "description": "Local no-network/no-wallet/no-execution Agent Trust Bundle CLI contract.",
    "bundle_contract_version": AGENT_TRUST_BUNDLE_CONTRACT_VERSION,
    "supported_bundle_contract_versions": SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS,
    "schemas": {
        "request": "schemas/agent_trust_request.schema.json",
        "bundle_output": "schemas/agent_trust_bundle.schema.json",
    },
    "safety_boundary": {
        "network_calls": False,
        "wallet_access": False,
        "execution": False,
        "real_money": False,
    },
    "input": {
        "format": "json_object",
        "guardrails": {
            "max_input_bytes": AGENT_TRUST_MAX_JSON_INPUT_BYTES,
            "max_nesting_depth": AGENT_TRUST_MAX_JSON_NESTING_DEPTH,
            "failure_mode": "reject_with_sanitized_error_before_bundle_processing",
        },
        "fields": {
            "policy": {"required": True, "type": "object"},
            "ledger": {"required": False, "type": "array"},
            "resource": {"required": False, "type": "string"},
            "tool_descriptor": {"required": False, "type": "object"},
            "intended_integration_context": {"required": False, "type": "string"},
            "provenance_evidence": {"required": False, "type": "object|array|string"},
            "contract_version": {"required": False, "type": "string", "default": AGENT_TRUST_BUNDLE_CONTRACT_VERSION},
        },
    },
    "output": {
        "format": "json_object",
        "top_level_fields": [
            "bundle_id",
            "contract_version",
            "supported_contract_versions",
            "verdict",
            "reasons",
            "controls",
            "network_calls",
            "wallet_access",
            "execution",
            "settlement",
            "policy_quote",
            "tool_risk",
            "intended_integration_context",
            "provenance_evidence",
            "account_recovery_takeover_detector",
            "context_control_plane_detector",
        ],
    },
    "error_envelope": {
        "stream": "stderr",
        "shape": {"error": {"code": "invalid_agent_trust_input|unsupported_agent_trust_contract_version", "message": "string"}},
    },
    "exit_codes": {
        "0": "success or contract printed",
        "2": "invalid input JSON, unsupported contract version, missing required fields, or input read error",
    },
    "examples": [
        "python3 -m agent_trust.cli --print-contract",
        "python3 -m agent_trust.cli --input examples/input.json",
        "python3 -m agent_trust.cli --contract-version agent-trust-bundle-v1 --input examples/input.json",
        "cat examples/input.json | python3 -m agent_trust.cli --input -",
    ],
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a local no-network/no-wallet/no-execution Agent Trust Bundle.",
    )
    parser.add_argument(
        "input_arg",
        nargs="?",
        help="Optional positional input JSON path kept for demo-script compatibility.",
    )
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Path to Agent Trust input JSON, or '-' for stdin. Omit to read stdin.",
    )
    parser.add_argument(
        "--print-contract",
        action="store_true",
        help="Print the machine-readable Agent Trust CLI contract and exit.",
    )
    parser.add_argument(
        "--contract-version",
        default=None,
        help="Requested Agent Trust bundle contract version. Defaults to the current supported version.",
    )
    args = parser.parse_args()
    if args.print_contract:
        print(json.dumps(AGENT_TRUST_CLI_CONTRACT, sort_keys=True, indent=2, ensure_ascii=False))
        raise SystemExit(0)

    input_path = args.input_path if args.input_path is not None else args.input_arg

    try:
        if input_path in {None, "-"}:
            raw = sys.stdin.read(AGENT_TRUST_MAX_JSON_INPUT_BYTES + 1)
        else:
            path = Path(input_path)
            size = path.stat().st_size
            if size > AGENT_TRUST_MAX_JSON_INPUT_BYTES:
                raise AgentTrustInputGuardError(
                    "Agent Trust input exceeds JSON size limit "
                    f"({size} bytes > {AGENT_TRUST_MAX_JSON_INPUT_BYTES} bytes)"
                )
            raw = path.read_text(encoding="utf-8")
        guard_agent_trust_json_text(raw)
        data = json.loads(raw)
        guard_agent_trust_json_depth(data)
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        if not isinstance(data.get("policy"), dict):
            raise ValueError("input requires object field: policy")
        requested_contract_version = args.contract_version or data.get("contract_version")
        try:
            bundle = build_agent_trust_bundle(
                data["policy"],
                ledger=data.get("ledger"),
                resource=data.get("resource"),
                tool_descriptor=data.get("tool_descriptor"),
                contract_version=requested_contract_version,
                intended_integration_context=data.get("intended_integration_context"),
                provenance_evidence=data.get("provenance_evidence"),
            )
        except ValueError:
            print(
                json.dumps(
                    {"error": {"code": "unsupported_agent_trust_contract_version", "message": f"unsupported Agent Trust contract version: {requested_contract_version}", "requested_contract_version": requested_contract_version, "supported_contract_versions": SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS}},
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            raise SystemExit(2)
        print(json.dumps(bundle, sort_keys=True, indent=2, ensure_ascii=False))
    except (OSError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        print(
            json.dumps(
                {"error": {"code": "invalid_agent_trust_input", "message": str(exc)}},
                sort_keys=True,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)
