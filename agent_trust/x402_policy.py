"""Local no-money x402-style policy receipts for Agent Trust.

This module intentionally does not implement live x402 settlement. It produces
small deterministic policy quotes that can be embedded in a pre-action trust
bundle before any real network, wallet, signing, or payment flow exists.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

POLICY_VERSION = "agent-trust-x402-policy-v1"
SETTLEMENT = "none"


def _decimal_or_none(value: Any) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _allowed_resources(policy: dict[str, Any]) -> set[str]:
    raw = policy.get("allowed_resources") or policy.get("allowlist") or []
    if isinstance(raw, str):
        raw = [raw]
    return {str(item) for item in raw}


def quote_x402_policy(policy: dict[str, Any], ledger: list[dict[str, Any]] | None = None, resource: str | None = None) -> dict[str, Any]:
    """Return a deterministic local quote for a possible paid/resource action."""
    ledger = ledger or []
    budget = _decimal_or_none(policy.get("budget") or policy.get("max_budget"))
    spent = _decimal_or_none(policy.get("spent"))
    if spent is None:
        spent = sum((_decimal_or_none(item.get("amount")) or Decimal("0")) for item in ledger if isinstance(item, dict))
    remaining = None if budget is None else budget - spent
    allowed = _allowed_resources(policy)
    resource_allowed = None if not resource else resource in allowed if allowed else None
    return {
        "policy_version": POLICY_VERSION,
        "settlement": str(policy.get("settlement") or SETTLEMENT),
        "agent_id": policy.get("agent_id") or policy.get("subject") or "unspecified-agent",
        "resource": resource,
        "resource_allowed": resource_allowed,
        "budget": None if budget is None else str(budget),
        "spent": str(spent),
        "remaining_budget": None if remaining is None else str(remaining),
        "ledger_entries": len(ledger),
        "network_calls": False,
        "wallet_access": False,
        "real_money": False,
    }


def evaluate_x402_policy(payment: dict[str, Any], policy: dict[str, Any], ledger: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Evaluate a proposed local payment/resource request against policy."""
    resource = payment.get("resource") if isinstance(payment, dict) else None
    quote = quote_x402_policy(policy, ledger=ledger, resource=resource)
    amount = _decimal_or_none(payment.get("amount") if isinstance(payment, dict) else None) or Decimal("0")
    remaining = _decimal_or_none(quote.get("remaining_budget"))
    reasons: list[str] = []
    if quote.get("resource_allowed") is False:
        reasons.append("resource_not_allowlisted")
    if remaining is not None and amount > remaining:
        reasons.append("amount_exceeds_remaining_budget")
    return {
        **quote,
        "requested_amount": str(amount),
        "allowed": not reasons,
        "reasons": reasons,
    }


__all__ = ["POLICY_VERSION", "SETTLEMENT", "evaluate_x402_policy", "quote_x402_policy"]
