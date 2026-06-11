#!/usr/bin/env python3
"""Layered local Agent Trust skill-scanning evidence receipt.

This is an inert, dependency-free model of layered skill-review evidence inspired
by public descriptions of registry/reputation, static-analysis, agentic-risk,
provenance, and moderation-history review pipelines. It does not call
VirusTotal, NVIDIA SkillSpector, ClawHub, ClawScan, or any external scanner; it
executes no untrusted skill code and claims no third-party verification.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any

SAFETY_BOUNDARY = {
    "network_calls": False,
    "external_scanners_called": False,
    "virus_total_called": False,
    "nvidia_skillspector_called": False,
    "clawhub_or_clawscan_called": False,
    "untrusted_code_execution": False,
    "secret_values_read": False,
    "wallet_access": False,
    "cryptographic_signing": False,
    "payment": False,
    "real_money": False,
    "external_verification_claimed": False,
}


@dataclass(frozen=True)
class Finding:
    layer: str
    code: str
    severity: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "layer": self.layer,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }


SEVERITY_SCORE = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def default_descriptor() -> dict[str, Any]:
    return {
        "skill_id": "synthetic-layered-skill-001",
        "declared_purpose": "Summarize repository documentation",
        "declared_permissions": ["read:docs"],
        "requested_permissions": ["read:repo", "read:env", "network:egress", "shell:execute"],
        "reputation": {
            "known_bad_hash": False,
            "malware_label": False,
            "low_reputation_source": True,
            "unsigned_archive": True,
        },
        "static_analysis": {
            "secret_patterns": ["AWS_ACCESS_KEY_ID-like placeholder"],
            "dynamic_code": True,
            "suspicious_install_hooks": ["postinstall shell hook"],
            "dangerous_imports": ["subprocess"],
        },
        "mcp_supply_chain_rce": {
            "installer_executes_code": True,
            "runtime_tool_bridge": True,
            "ambient_process_authority": True,
            "untrusted_server_controls_tools": True,
            "version_or_source_mutable": True,
        },
        "agentic_semantics": {
            "hidden_instructions": True,
            "tool_poisoning": True,
            "data_exfiltration": True,
            "description_behavior_mismatch": True,
            "excessive_agency": True,
        },
        "provenance": {
            "source": "synthetic-local-descriptor",
            "pinned_commit": False,
            "publisher_verified": False,
            "metadata_complete": False,
            "moderation_history": ["prior_report_unreviewed"],
        },
        "scanner_results": {
            "reputation_layer": "review",
            "static_layer": "deny",
            "agentic_layer": "deny",
            "provenance_layer": "review",
        },
    }


def scanner_pass_fallacy_descriptor() -> dict[str, Any]:
    """Synthetic proof that scanner pass labels are evidence, not authorization."""
    return {
        "skill_id": "synthetic-scanner-pass-fallacy-001",
        "declared_purpose": "Format local markdown notes",
        "declared_permissions": ["read:docs"],
        "requested_permissions": ["read:repo", "read:env", "network:egress", "shell:execute"],
        "reputation": {
            "known_bad_hash": False,
            "malware_label": False,
            "low_reputation_source": False,
            "unsigned_archive": True,
        },
        "static_analysis": {
            "secret_patterns": [],
            "dynamic_code": True,
            "suspicious_install_hooks": ["postinstall activation hook"],
            "dangerous_imports": ["subprocess"],
        },
        "mcp_supply_chain_rce": {
            "installer_executes_code": True,
            "runtime_tool_bridge": True,
            "ambient_process_authority": True,
            "untrusted_server_controls_tools": False,
            "version_or_source_mutable": True,
        },
        "agentic_semantics": {
            "hidden_instructions": True,
            "tool_poisoning": True,
            "data_exfiltration": True,
            "description_behavior_mismatch": True,
            "excessive_agency": True,
        },
        "provenance": {
            "source": "synthetic-local-descriptor",
            "pinned_commit": False,
            "publisher_verified": False,
            "metadata_complete": True,
            "moderation_history": [],
        },
        "scanner_results": {
            "marketplace_scanner": "proceed",
            "static_scanner": "proceed",
            "reputation_scanner": "proceed",
            "metadata_scanner": "proceed",
        },
    }


def _truthy_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def collect_findings(descriptor: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    rep = descriptor.get("reputation", {}) if isinstance(descriptor.get("reputation"), dict) else {}
    if rep.get("known_bad_hash") or rep.get("malware_label"):
        findings.append(Finding("malware_reputation", "known_malware_or_bad_hash", "critical", "reputation evidence indicates known malware or known-bad hash"))
    if rep.get("low_reputation_source"):
        findings.append(Finding("malware_reputation", "low_reputation_source", "medium", "source reputation is weak or newly observed"))
    if rep.get("unsigned_archive"):
        findings.append(Finding("malware_reputation", "unsigned_or_unverified_package", "medium", "package/archive lacks a local signature or immutable verification evidence"))

    static = descriptor.get("static_analysis", {}) if isinstance(descriptor.get("static_analysis"), dict) else {}
    if _truthy_list(static.get("secret_patterns")):
        findings.append(Finding("static_analysis", "secret_shaped_values", "high", "static evidence contains secret-shaped values or placeholders requiring redaction/review"))
    if static.get("dynamic_code"):
        findings.append(Finding("static_analysis", "dynamic_code_execution_pattern", "high", "dynamic code execution pattern is present"))
    if _truthy_list(static.get("suspicious_install_hooks")):
        findings.append(Finding("static_analysis", "suspicious_install_hook", "high", "install hook could execute code during setup or activation"))
    if _truthy_list(static.get("dangerous_imports")):
        findings.append(Finding("static_analysis", "dangerous_runtime_capability", "medium", "dangerous runtime capability appears in static metadata"))

    mcp_rce = descriptor.get("mcp_supply_chain_rce", {}) if isinstance(descriptor.get("mcp_supply_chain_rce"), dict) else {}
    mcp_rce_codes = {
        "installer_executes_code": ("mcp_install_time_code_execution", "critical", "MCP/tool installation or activation can execute code before review completes"),
        "runtime_tool_bridge": ("mcp_runtime_tool_bridge", "high", "MCP/tool bridge can connect model-controlled input to runtime capabilities"),
        "ambient_process_authority": ("ambient_process_authority", "high", "server or skill may inherit broad process, filesystem, token, or environment authority"),
        "untrusted_server_controls_tools": ("untrusted_server_tool_control", "critical", "untrusted MCP/server-side component can influence available tools or tool arguments"),
        "version_or_source_mutable": ("mutable_mcp_or_tool_source", "medium", "MCP/tool source is mutable or version evidence is insufficient for reproducible review"),
    }
    for key, (code, severity, message) in mcp_rce_codes.items():
        if mcp_rce.get(key):
            findings.append(Finding("mcp_supply_chain_rce", code, severity, message))

    semantic = descriptor.get("agentic_semantics", {}) if isinstance(descriptor.get("agentic_semantics"), dict) else {}
    semantic_codes = {
        "hidden_instructions": ("hidden_agent_instruction", "high", "hidden or conflicting instructions are present"),
        "tool_poisoning": ("tool_poisoning_risk", "high", "tool description or behavior could steer unsafe tool use"),
        "data_exfiltration": ("data_exfiltration_risk", "critical", "skill may move private data outside intended boundaries"),
        "description_behavior_mismatch": ("description_behavior_mismatch", "high", "declared purpose does not match requested behavior/capability"),
        "excessive_agency": ("excessive_agency_or_permissions", "high", "requested agency exceeds declared purpose"),
    }
    for key, (code, severity, message) in semantic_codes.items():
        if semantic.get(key):
            findings.append(Finding("agentic_semantic_risk", code, severity, message))

    provenance = descriptor.get("provenance", {}) if isinstance(descriptor.get("provenance"), dict) else {}
    if not provenance.get("pinned_commit"):
        findings.append(Finding("provenance_metadata_moderation", "mutable_or_unpinned_source", "medium", "source is not pinned to an immutable commit/tag in local evidence"))
    if not provenance.get("publisher_verified"):
        findings.append(Finding("provenance_metadata_moderation", "unverified_publisher", "medium", "publisher identity is not locally verified"))
    if not provenance.get("metadata_complete"):
        findings.append(Finding("provenance_metadata_moderation", "incomplete_metadata", "low", "metadata is incomplete for trust review"))
    if _truthy_list(provenance.get("moderation_history")):
        findings.append(Finding("provenance_metadata_moderation", "moderation_history_requires_review", "medium", "moderation history contains unresolved or prior-review signals"))

    scanner_results = descriptor.get("scanner_results", {}) if isinstance(descriptor.get("scanner_results"), dict) else {}
    verdicts = {v for v in scanner_results.values() if v in {"proceed", "review", "deny"}}
    scanner_values = {str(v).lower() for v in scanner_results.values()}
    scanner_pass_values = {"proceed", "pass", "clean", "allow", "ok"}
    if scanner_results and scanner_values <= scanner_pass_values and findings:
        findings.append(Finding("scanner_disagreement", "scanner_pass_is_not_authorization", "high", "clean scanner labels do not override independent authority, provenance, install-hook, or semantic-risk signals"))
    if len(verdicts) > 1:
        findings.append(Finding("scanner_disagreement", "layered_scanner_disagreement", "medium", "scanner layers disagree; conservative aggregation requires review or denial rather than silent allow"))
    return findings


def decide(findings: list[Finding]) -> str:
    if any(f.severity == "critical" for f in findings):
        return "deny"
    high_count = sum(1 for f in findings if f.severity == "high")
    if high_count >= 2:
        return "deny"
    if high_count == 1 or any(f.severity == "medium" for f in findings):
        return "review"
    return "proceed"


def build_receipt(descriptor: dict[str, Any] | None = None) -> dict[str, Any]:
    descriptor = descriptor or default_descriptor()
    findings = collect_findings(descriptor)
    decision = decide(findings)
    layers = ["malware_reputation", "static_analysis", "mcp_supply_chain_rce", "agentic_semantic_risk", "provenance_metadata_moderation", "scanner_disagreement"]
    counts_by_layer = {layer: sum(1 for f in findings if f.layer == layer) for layer in layers}
    counts_by_severity = {severity: sum(1 for f in findings if f.severity == severity) for severity in ["critical", "high", "medium", "low", "info"]}
    return {
        "ok": decision != "proceed" or bool(findings) is True,
        "artifact": "agent_trust_layered_skill_scanning",
        "decision": decision,
        "skill_id": descriptor.get("skill_id", "unknown"),
        "summary": "local synthetic layered skill-scanning receipt; scanner signals are evidence, not authorization or third-party verification",
        "layers": layers,
        "counts": {"findings": len(findings), "by_layer": counts_by_layer, "by_severity": counts_by_severity},
        "findings": [finding.as_dict() for finding in findings],
        "aggregation_policy": {
            "critical_finding": "deny",
            "mcp_supply_chain_rce_critical": "deny",
            "two_or_more_high_findings": "deny",
            "one_high_or_any_medium_finding": "review",
            "scanner_disagreement": "at_least_review",
            "scanner_pass_with_independent_risk_signals": "not_authorization",
            "clean_or_low_only": "proceed",
        },
        "non_claims": [
            "not_virustotal_scanned",
            "not_nvidia_skillspector_verified",
            "not_clawhub_or_clawscan_verified",
            "not_external_catalog_verification",
            "not_runtime_enforcement_boundary",
            "clean_scanner_result_does_not_authorize_install_or_use",
        ],
        "safety_boundary": SAFETY_BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit a local layered Agent Trust skill-scanning receipt.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    parser.add_argument("--scanner-pass-fallacy-demo", action="store_true", help="Use a synthetic descriptor where clean scanner labels conflict with dangerous authority signals.")
    parser.add_argument("--expect-decision", choices=["proceed", "review", "deny"])
    parser.add_argument("--fail-on-fail", action="store_true", help="Exit nonzero if expectation or safety invariants fail.")
    args = parser.parse_args()
    descriptor = scanner_pass_fallacy_descriptor() if args.scanner_pass_fallacy_demo else None
    receipt = build_receipt(descriptor)
    expected_ok = args.expect_decision is None or receipt["decision"] == args.expect_decision
    boundary_ok = all(value is False for value in receipt["safety_boundary"].values())
    receipt["ok"] = expected_ok and boundary_ok and receipt["decision"] in {"proceed", "review", "deny"}
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=None if args.compact else 2))
    if args.fail_on_fail and not receipt["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
