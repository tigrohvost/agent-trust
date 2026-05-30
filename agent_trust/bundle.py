"""Local pre-action trust bundle combining x402 quote and tool/MCP risk signals."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import hashlib
import json
import re
from typing import Any

from agent_trust.tool_risk import AUTH_KEYS, DANGEROUS_WORDS, EXEC_KEYS, FS_KEYS, NETWORK_KEYS, RISK_ORDER
from agent_trust.x402_policy import quote_x402_policy


AGENT_TRUST_BUNDLE_CONTRACT_VERSION = "agent-trust-bundle-v1"
SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS = [AGENT_TRUST_BUNDLE_CONTRACT_VERSION]



def _normalize_provenance_evidence(provenance_evidence: Any = None) -> dict[str, Any]:
    """Normalize discovery/identity provenance without treating it as trust.

    DNS-AID/ANS-style records can help another agent understand where an
    endpoint was discovered and who claims to operate it. They are evidence,
    not authorization: policy, warrant, and risk evaluation still decide.
    """
    subjects = [] if provenance_evidence is None else provenance_evidence if isinstance(provenance_evidence, list) else [provenance_evidence]
    items: list[dict[str, Any]] = []
    for raw in subjects:
        source = raw if isinstance(raw, dict) else {"description": str(raw)}
        evidence: dict[str, Any] = {
            "source": str(source.get("source") or source.get("kind") or "unspecified"),
            "kind": str(source.get("kind") or "discovery_or_identity"),
        }
        for key in ("name", "dns_name", "endpoint", "transport", "discovery_claim", "identity_claim"):
            if source.get(key) is not None:
                evidence[key] = source[key]
        if isinstance(source.get("capability_claims"), list):
            evidence["capability_claims"] = sorted(str(item) for item in source["capability_claims"])
        elif source.get("capability_claims") is not None:
            evidence["capability_claims"] = [str(source["capability_claims"])]
        serialized = json.dumps(evidence, sort_keys=True, ensure_ascii=False).lower()
        evidence["signals"] = {
            "discovery_claim_present": "discovery_claim" in evidence or "dns_name" in evidence or "endpoint" in evidence,
            "identity_claim_present": "identity_claim" in evidence,
            "dns_aid_ans_style": any(marker in serialized for marker in ("dns-aid", "dns_aid", "ans", "dnssec", "dane")),
        }
        items.append(evidence)
    return {
        "attestation_version": "provenance-evidence-v1",
        "evidence_count": len(items),
        "items": items,
        "network_calls": False,
        "execution": False,
        "trust_boundary": "Discovery and identity provenance is evidence only; it is not authorization, trust, or permission to act without policy and warrant evaluation.",
    }


def _build_agent_trust_bundle(policy: dict[str, Any], ledger: list[dict[str, Any]] | None = None, resource: str | None = None, tool_descriptor: Any = None, *, contract_version: str | None = None, intended_integration_context: str | None = None, provenance_evidence: Any = None, registered_tool_manifest: list[dict[str, Any]] | None = None, loaded_tool_count: int = 0) -> dict[str, Any]:
    """Build a deterministic no-network/no-wallet/no-execution pre-action trust report."""
    negotiated_contract_version = contract_version or AGENT_TRUST_BUNDLE_CONTRACT_VERSION
    if negotiated_contract_version not in SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS:
        supported = ", ".join(SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS)
        raise ValueError(f"unsupported Agent Trust contract version: {negotiated_contract_version}; supported: {supported}")
    quote = quote_x402_policy(policy, ledger=ledger, resource=resource)
    provenance = _normalize_provenance_evidence(provenance_evidence)
    subjects = [] if tool_descriptor is None else tool_descriptor if isinstance(tool_descriptor, list) else [tool_descriptor]
    findings = []
    max_risk = "LOW"
    for raw in subjects:
        item = raw if isinstance(raw, dict) else {"description": str(raw)}
        serialized = json.dumps(item, sort_keys=True, ensure_ascii=False).lower()
        keys = {str(k).lower() for k in item}
        transport = str(item.get("transport") or "").lower()
        remote = transport in {"sse", "http", "https", "websocket"} or any(w in serialized for w in ("http://", "https://", "websocket"))
        auth = any(k in keys for k in AUTH_KEYS) or any(w in serialized for w in ("api_key", "bearer", "token", "secret", "credential", "env"))
        fs = (any(k in keys for k in FS_KEYS) or any(w in serialized for w in ("filesystem", "workspace", "delete", "write"))) and not item.get("read_only") is True
        execution = any(k in keys for k in EXEC_KEYS) or any(w in serialized for w in ("shell", "subprocess", "exec", "docker", "command"))
        score = (2 if remote else 0) + (2 if auth else 0) + (2 if fs else 0) + (3 if execution else 0) + (1 if any(w in serialized for w in DANGEROUS_WORDS if w not in {"filesystem"}) else 0)
        risk = "BLOCK" if execution and (remote or auth) else "HIGH" if score >= 5 else "MEDIUM" if score >= 2 else "LOW"
        max_risk = risk if RISK_ORDER[risk] > RISK_ORDER[max_risk] else max_risk
        findings.append({"name": item.get("name") or item.get("id") or item.get("url") or "unnamed-tool", "kind": item.get("kind") or item.get("type") or "tool_or_mcp", "risk": risk, "signals": {"remote_or_network": remote, "auth_or_secret_reference": auth, "filesystem_or_write_reach": fs, "execution_capability": execution, "dangerous_words": sorted(w for w in DANGEROUS_WORDS if w in serialized), "urls": sorted(set(re.findall(r'https?://[^\s"\'<>]+', serialized)))[:5]}})
    if registered_tool_manifest is not None or loaded_tool_count > 0:
        findings.append({"name": "ouroboros-registered-tools", "kind": "local_registry_snapshot", "risk": "MEDIUM", "signals": {"loaded_tool_count": int(loaded_tool_count or 0), "manifest_available": bool(registered_tool_manifest)}})
        max_risk = "MEDIUM" if RISK_ORDER["MEDIUM"] > RISK_ORDER[max_risk] else max_risk
    risk = {"attestation_version": "tool-risk-v1", "overall_risk": max_risk, "finding_count": len(findings), "findings": findings, "network_calls": False, "execution": False}
    reasons = []
    try:
        remaining = None if quote.get("remaining_budget") is None else Decimal(str(quote.get("remaining_budget")))
    except (InvalidOperation, ValueError):
        remaining = None
    if risk["overall_risk"] == "BLOCK":
        reasons.append("tool_risk_block")
    if quote.get("resource_allowed") is False:
        reasons.append("resource_not_allowlisted")
    if remaining is not None and remaining < 0:
        reasons.append("agent_budget_negative")
    verdict = "deny" if reasons else "review" if RISK_ORDER.get(risk["overall_risk"], 3) >= RISK_ORDER["MEDIUM"] or quote.get("resource_allowed") is None or not quote.get("resource") else "allow"
    if verdict == "review" and not reasons:
        if RISK_ORDER.get(risk["overall_risk"], 3) >= RISK_ORDER["MEDIUM"]:
            reasons.append(f"tool_risk_{risk['overall_risk'].lower()}")
        if quote.get("resource_allowed") is None or not quote.get("resource"):
            reasons.append("resource_not_supplied")
    controls = ["network_calls_false", "wallet_access_false", "execution_false", f"x402_settlement:{quote.get('settlement')}"]
    canonical_payload = {"policy_quote": quote, "tool_risk": risk, "provenance_evidence": provenance, "verdict": verdict, "reasons": reasons, "controls": controls}
    if intended_integration_context:
        canonical_payload["intended_integration_context"] = intended_integration_context
    canonical = json.dumps(canonical_payload, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    bundle = {"bundle_id": f"agenttrust-{digest[:16]}", "contract_version": negotiated_contract_version, "supported_contract_versions": SUPPORTED_AGENT_TRUST_BUNDLE_CONTRACT_VERSIONS, "digest": digest, "verdict": verdict, "reasons": reasons, "controls": controls, "network_calls": False, "wallet_access": False, "execution": False, "settlement": quote.get("settlement"), "policy_quote": quote, "tool_risk": risk, "provenance_evidence": provenance}
    if intended_integration_context:
        bundle["intended_integration_context"] = intended_integration_context
    return bundle


build_agent_trust_bundle = _build_agent_trust_bundle
