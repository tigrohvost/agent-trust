#!/usr/bin/env python3
"""Secret-safe local preflight for a future Base Sepolia x402 test.

This script does not connect to Base Sepolia, does not access a wallet, does not
sign, and does not perform a payment. It only checks whether the local runtime
shape looks safe enough to consider a later live testnet command.
"""

from __future__ import annotations

import json
import os
from decimal import Decimal, InvalidOperation

REQUIRED_ENV_VARS = (
    "AGENT_TRUST_X402_NETWORK",
    "AGENT_TRUST_X402_ASSET",
    "AGENT_TRUST_X402_AMOUNT_USDC",
    "AGENT_TRUST_X402_FACILITATOR_URL",
    "AGENT_TRUST_X402_TEST_WALLET_ADDRESS",
)

SECRET_ENV_VARS = (
    "AGENT_TRUST_X402_TEST_PRIVATE_KEY",
    "AGENT_TRUST_X402_TEST_SEED_PHRASE",
    "AGENT_TRUST_X402_WALLET_KEY",
)

MAINNET_MARKERS = ("mainnet", "base-mainnet", "ethereum", "polygon")


source = os.environ
env_values = {name: source.get(name, "") for name in REQUIRED_ENV_VARS}
secret_presence = {name: bool(source.get(name)) for name in SECRET_ENV_VARS}
secret_lengths = {name: len(source.get(name, "")) for name in SECRET_ENV_VARS if source.get(name)}

network = env_values["AGENT_TRUST_X402_NETWORK"].strip().lower()
asset = env_values["AGENT_TRUST_X402_ASSET"].strip()
amount_text = env_values["AGENT_TRUST_X402_AMOUNT_USDC"].strip()
facilitator_url = env_values["AGENT_TRUST_X402_FACILITATOR_URL"].strip()
wallet_address = env_values["AGENT_TRUST_X402_TEST_WALLET_ADDRESS"].strip()

missing = [name for name, value in env_values.items() if not value]
checks: list[dict[str, object]] = []

network_ok = network in {"base-sepolia", "base_sepolia", "eip155:84532"}
checks.append(
    {
        "name": "network_is_base_sepolia",
        "passed": network_ok,
        "detail": "AGENT_TRUST_X402_NETWORK must be base-sepolia/base_sepolia/eip155:84532",
    }
)

no_mainnet = not any(marker in network for marker in MAINNET_MARKERS)
checks.append(
    {
        "name": "mainnet_not_selected",
        "passed": no_mainnet,
        "detail": "preflight refuses mainnet-like network labels",
    }
)

wallet_shape_ok = wallet_address.startswith("0x") and len(wallet_address) == 42
checks.append(
    {
        "name": "test_wallet_address_shape",
        "passed": wallet_shape_ok,
        "detail": "address must look like a throwaway EVM test wallet address",
    }
)

asset_shape_ok = asset.startswith("0x") and len(asset) == 42
checks.append(
    {
        "name": "asset_address_shape",
        "passed": asset_shape_ok,
        "detail": "asset should be a Base Sepolia token contract address, not a symbol",
    }
)

try:
    amount = Decimal(amount_text)
    amount_ok = Decimal("0") < amount <= Decimal("0.10")
except (InvalidOperation, ValueError):
    amount_ok = False
checks.append(
    {
        "name": "amount_is_small_testnet_value",
        "passed": amount_ok,
        "detail": "amount must parse as USDC and be <= 0.10 for this readiness gate",
    }
)

facilitator_ok = facilitator_url.startswith("https://")
checks.append(
    {
        "name": "facilitator_url_shape",
        "passed": facilitator_ok,
        "detail": "facilitator must be an explicit HTTPS URL for a later live testnet run",
    }
)

private_key_present = secret_presence["AGENT_TRUST_X402_TEST_PRIVATE_KEY"]
seed_phrase_absent = not secret_presence["AGENT_TRUST_X402_TEST_SEED_PHRASE"]
broad_wallet_key_absent = not secret_presence["AGENT_TRUST_X402_WALLET_KEY"]
checks.append(
    {
        "name": "private_key_present_without_seed_phrase",
        "passed": private_key_present and seed_phrase_absent and broad_wallet_key_absent,
        "detail": "use one throwaway test private key only; never expose seed phrases or broad wallet keys",
    }
)

ready = not missing and all(bool(check["passed"]) for check in checks)

REPORT: dict[str, object] = {
    "name": "Agent Trust Base Sepolia x402 preflight",
    "status": "ready_for_manual_live_testnet_step" if ready else "not_ready",
    "safety_boundary": {
        "network_calls_performed": False,
        "wallet_access_performed": False,
        "signing_performed": False,
        "payment_performed": False,
        "mainnet_allowed": False,
        "secrets_printed": False,
    },
    "required_env": {
        name: {
            "present": bool(value),
            "value_length": len(value),
            "value_preview": (value[:6] + "..." + value[-4:] if value.startswith("0x") and len(value) >= 10 else None),
        }
        for name, value in env_values.items()
    },
    "secret_env": {
        name: {
            "present": secret_presence[name],
            "value_length": secret_lengths.get(name, 0),
            "value_preview": None,
        }
        for name in SECRET_ENV_VARS
    },
    "missing_required_env": missing,
    "activation_path": {
        "template_path": "examples/agent_trust_base_sepolia.env.example",
        "local_filled_env_recommendation": "/tmp/agent_trust_base_sepolia.env",
        "required_public_or_shape_checked_env": list(REQUIRED_ENV_VARS),
        "required_secret_by_presence_only": ["AGENT_TRUST_X402_TEST_PRIVATE_KEY"],
        "forbidden_secret_env": [
            "AGENT_TRUST_X402_TEST_SEED_PHRASE",
            "AGENT_TRUST_X402_WALLET_KEY",
        ],
        "commands": [
            "cp examples/agent_trust_base_sepolia.env.example /tmp/agent_trust_base_sepolia.env",
            "$EDITOR /tmp/agent_trust_base_sepolia.env",
            "set -a; . /tmp/agent_trust_base_sepolia.env; set +a",
            "python3 examples/agent_trust_base_sepolia_preflight.py",
            "python3 examples/agent_trust_base_sepolia_live_boundary.py",
        ],
        "safety_notes": [
            "filled env files must remain local and uncommitted",
            "use a throwaway Base Sepolia test wallet only",
            "never print, paste, commit, or log private keys or seed phrases",
            "the live-boundary script is dry-run-only and performs no network, wallet, signing, or payment action",
        ],
    },
    "checks": checks,
    "stop_conditions_before_live_call": [
        "any required env var missing",
        "network is not Base Sepolia",
        "wallet is not a throwaway test wallet",
        "seed phrase or broad wallet key is present",
        "amount is not tiny testnet USDC",
        "facilitator URL is not explicitly selected",
        "any command would print private keys, seed phrases, bearer tokens, or wallet credentials",
        "any command points to mainnet or real-money settlement",
    ],
    "next_manual_step_if_ready": "Run the future live x402 client only with explicit owner-confirmed testnet limits and sanitized logging.",
}


if __name__ == "__main__":
    print(json.dumps(REPORT, indent=2, sort_keys=True))
    raise SystemExit(0 if REPORT["status"] == "ready_for_manual_live_testnet_step" else 2)
