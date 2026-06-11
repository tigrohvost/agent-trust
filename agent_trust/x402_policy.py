"""Local no-wallet x402 policy quote helpers for Agent Trust.

This module is deliberately self-contained for the public package: it performs
no network calls, no wallet access, no signing, and no settlement.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

POLICY_VERSION = "x402-policy-v1"
SETTLEMENT = "local_no_wallet_no_payment"


def _decimal_or_none(value: Any) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def quote_x402_policy(
    policy: dict[str, Any],
    ledger: list[dict[str, Any]] | None = None,
    resource: str | None = None,
) -> dict[str, Any]:
    """Return a deterministic local x402-style policy quote.

    The result is an advisory budget/resource receipt. It never contacts a
    facilitator, reads a wallet, signs a transaction, or transfers money.
    """
    ledger = ledger or []
    resource = resource or policy.get("resource") or policy.get("endpoint")
    allowed_resources = policy.get("allowed_resources")
    if allowed_resources is None:
        resource_allowed: bool | None = None
    else:
        allowed = {str(item) for item in allowed_resources}
        resource_allowed = str(resource) in allowed if resource is not None else False

    budget = _decimal_or_none(
        policy.get("budget") or policy.get("max_budget") or policy.get("per_agent_budget_cap")
    )
    # Spend already declared on the policy counts alongside ledger entries;
    # ignoring it silently understates spend and overstates remaining budget.
    spent = _decimal_or_none(policy.get("spent")) or Decimal("0")
    for entry in ledger:
        amount = _decimal_or_none(entry.get("amount") if isinstance(entry, dict) else None)
        if amount is not None:
            spent += amount
    remaining = None if budget is None else budget - spent

    return {
        "policy_version": POLICY_VERSION,
        "settlement": SETTLEMENT,
        "resource": resource,
        "resource_allowed": resource_allowed,
        "budget": None if budget is None else str(budget),
        "spent": str(spent),
        "remaining_budget": None if remaining is None else str(remaining),
        "network_calls": False,
        "wallet_access": False,
        "payment_submitted": False,
        "real_money": False,
    }
