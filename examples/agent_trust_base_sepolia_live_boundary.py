#!/usr/bin/env python3
"""Dry-run boundary for a future live Base Sepolia x402 client.

This is deliberately not the live client. It imports the secret-safe preflight,
turns readiness into an explicit future command contract, and refuses by design
to perform network, wallet, signing, transaction, payment, mainnet, or real-money
behavior. It is script-shaped on purpose to avoid growing the production/example
function surface for a static boundary packet.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from agent_trust_base_sepolia_preflight import REPORT, REQUIRED_ENV_VARS
except ModuleNotFoundError:  # pragma: no cover - supports import from outside docs/examples
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from agent_trust_base_sepolia_preflight import REPORT, REQUIRED_ENV_VARS

FUTURE_COMMAND = [
    "python3",
    "examples/agent_trust_base_sepolia_live_client.py",
    "--network",
    "$AGENT_TRUST_X402_NETWORK",
    "--asset",
    "$AGENT_TRUST_X402_ASSET",
    "--amount-usdc",
    "$AGENT_TRUST_X402_AMOUNT_USDC",
    "--facilitator-url",
    "$AGENT_TRUST_X402_FACILITATOR_URL",
    "--wallet-address",
    "$AGENT_TRUST_X402_TEST_WALLET_ADDRESS",
    "--private-key-env",
    "AGENT_TRUST_X402_TEST_PRIVATE_KEY",
    "--idempotency-key",
    "$AGENT_TRUST_X402_IDEMPOTENCY_KEY",
    "--confirm-testnet-only",
]

preflight = REPORT
ready = preflight.get("status") == "ready_for_manual_live_testnet_step"
boundary = {
    "name": "Agent Trust Base Sepolia x402 future live client boundary",
    "dry_run_only": True,
    "status": "ready_for_manual_live_client_implementation" if ready else "not_ready",
    "live_call_performed": False,
    "future_live_client_exists": False,
    "safety_boundary": {
        "network_calls_performed": False,
        "wallet_access_performed": False,
        "signing_performed": False,
        "payment_performed": False,
        "transaction_performed": False,
        "mainnet_allowed": False,
        "real_money_allowed": False,
        "secrets_printed": False,
    },
    "proposed_future_command_shape": {
        "description": "Shape only; this command is intentionally not executable until a separate reviewed live-client release exists.",
        "argv": FUTURE_COMMAND,
        "forbidden_now": "Do not create, invoke, or emulate the live client from this dry-run boundary script.",
    },
    "env_contract": {
        "required_public_or_shape_checked": list(REQUIRED_ENV_VARS),
        "required_secret_by_presence_only": ["AGENT_TRUST_X402_TEST_PRIVATE_KEY"],
        "forbidden_secret_inputs": [
            "AGENT_TRUST_X402_TEST_SEED_PHRASE",
            "AGENT_TRUST_X402_WALLET_KEY",
        ],
        "optional_future_env": {
            "AGENT_TRUST_X402_IDEMPOTENCY_KEY": "Future logical request id persisted across retries; never reuse for different resources.",
            "AGENT_TRUST_X402_RESOURCE_URL": "Future protected resource URL; must be manually verified as Base Sepolia/testnet-compatible before use.",
        },
    },
    "sanitized_logging_rules": [
        "print booleans, lengths, hashes, chain/network labels, and public test wallet address previews only",
        "never print private keys, seed phrases, bearer tokens, raw PAYMENT-SIGNATURE headers, wallet credentials, or full request authorization material",
        "record idempotency key presence or hash only, not any secret value",
        "log facilitator/resource hostnames only after manual review; never log signed payloads",
    ],
    "stop_conditions_before_implementation_or_live_call": preflight.get("stop_conditions_before_live_call", [])
    + [
        "future live client code has not had a separate review/release",
        "no idempotency key strategy exists for retry-safe payment attempts",
        "facilitator/resource compatibility with Base Sepolia is not manually confirmed",
        "any output would include raw PAYMENT-SIGNATURE, private key, seed phrase, bearer token, or wallet credential material",
        "any dependency would auto-detect or switch to mainnet",
        "any transaction would exceed the owner-confirmed testnet cap",
    ],
    "preflight": preflight,
}
print(json.dumps(boundary, indent=2, sort_keys=True))
raise SystemExit(0 if boundary["status"] == "ready_for_manual_live_client_implementation" else 2)
