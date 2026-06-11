#!/usr/bin/env python3
"""Local scanner-evidence example for Agent Trust.

This demonstrates how a first agent-client can submit sanitized scanner
finding summaries as pre-action evidence. It does not install, import, execute,
or trust any third-party scanner code. External scanner results are evidence,
not authority.
"""

from __future__ import annotations

import hashlib
import json

CONTRACT_VERSION = "agent-trust-scanner-evidence-v2"
SAFETY_BOUNDARY = {
    "network_calls": False,
    "wallet_access": False,
    "external_scanner_executed": False,
    "external_upload_performed": False,
    "action_performed": False,
    "real_money": False,
}
ATTACK_MAPPING_DISCLAIMER = (
    "ATT&CK-style mappings are reviewer vocabulary only. They are not claims of "
    "ATT&CK coverage, certification, enterprise telemetry detection, compliance, "
    "or authority to proceed/deny without local evidence."
)

SANITIZED_FINDING_SUMMARIES = {
    "mcp_prompt_injection": (
        "High-severity prompt-injection class finding against the exact MCP/tool "
        "action target. Raw prompt, exploit string, customer data, secrets, and "
        "scanner logs are intentionally omitted."
    ),
    "skill_pipeline_taint": (
        "Critical skill-package finding: scanner summary reports shell pipeline "
        "taint and bytecode/source mismatch in a local agent skill package. Raw "
        "files, bytecode, exploit strings, secrets, and customer repository paths "
        "are intentionally omitted."
    ),
}


def _hash_evidence(evidence: dict[str, object], sanitized_summary: str) -> str:
    public_hash_material = {
        "scanner_name": evidence["scanner_name"],
        "scanner_version": evidence["scanner_version"],
        "scan_target_type": evidence["scan_target_type"],
        "finding_count": evidence["finding_count"],
        "highest_severity": evidence["highest_severity"],
        "finding_categories": evidence["finding_categories"],
        "finding_engines": evidence.get("finding_engines", []),
        "sanitized_summary": sanitized_summary,
    }
    return hashlib.sha256(
        json.dumps(public_hash_material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _with_hash(evidence: dict[str, object], summary_key: str) -> dict[str, object]:
    evidence = dict(evidence)
    evidence["sanitized_summary"] = SANITIZED_FINDING_SUMMARIES[summary_key]
    evidence["evidence_hash"] = _hash_evidence(evidence, evidence["sanitized_summary"])
    return evidence


SCANNER_EVIDENCE = [
    _with_hash(
        {
            "evidence_id": "scanner-evidence-mcp-prompt-injection-001",
            "scanner_name": "promptfoo-compatible-summary",
            "scanner_version": "sanitized-example",
            "scanner_origin_url": "https://github.com/wearetyomsmnv/Awesome-LLMSecOps#tools-for-scanning",
            "scan_target_type": "mcp_server",
            "executed_by": "customer",
            "execution_boundary": "local_no_network",
            "finding_count": 1,
            "highest_severity": "high",
            "finding_categories": ["prompt_injection", "tool_abuse", "policy_bypass"],
            "scanner_output_format": "summary",
            "finding_engines": ["llm_semantic", "unknown"],
            "raw_output_included": False,
            "no_findings_is_not_no_risk": True,
            "external_upload_performed": False,
            "attack_mapping": [
                {
                    "framework": "MITRE ATT&CK Enterprise",
                    "tactic": "Execution",
                    "technique_id": "T1059",
                    "confidence": "analogical",
                    "note": "Agent-runtime analogue: prompt text attempts to steer tool execution.",
                },
                {
                    "framework": "MITRE ATT&CK Enterprise",
                    "tactic": "Defense Evasion",
                    "technique_id": "unknown",
                    "confidence": "weak",
                    "note": "Only vocabulary; local evidence is the scanner finding against the exact target.",
                },
            ],
            "sanitization_notes": [
                "No raw exploit payloads are included.",
                "No customer private data, secrets, system prompts, or scanner logs are included.",
                "Scanner code was not installed, imported, or executed by Rain.",
            ],
        },
        "mcp_prompt_injection",
    ),
    _with_hash(
        {
            "evidence_id": "scanner-evidence-agent-skill-package-001",
            "scanner_name": "cisco-skill-scanner-shaped-summary",
            "scanner_version": "sanitized-local-fixture",
            "scanner_origin_url": "https://github.com/cisco-ai-defense/skill-scanner",
            "scan_target_type": "agent_skill_package",
            "skill_format": "openai_codex_skill",
            "executed_by": "customer",
            "execution_boundary": "local_no_network",
            "scanner_policy_name": "balanced",
            "scanner_policy_version": "example-2026-06-06",
            "scanner_policy_fingerprint": "sha256:example-policy-fingerprint-no-secret-material",
            "scanner_output_format": "sarif",
            "finding_count": 2,
            "highest_severity": "critical",
            "finding_categories": ["skill_supply_chain", "persistence", "defense_impairment"],
            "finding_engines": ["pipeline_taint", "bytecode", "behavioral_dataflow"],
            "raw_output_included": False,
            "no_findings_is_not_no_risk": True,
            "external_upload_performed": False,
            "attack_mapping": [
                {
                    "framework": "MITRE ATT&CK Enterprise",
                    "tactic": "Supply Chain Compromise",
                    "technique_id": "T1195",
                    "confidence": "analogical",
                    "note": "Agent skill package behaves like a dependency with authority.",
                },
                {
                    "framework": "MITRE ATT&CK Enterprise",
                    "tactic": "Persistence",
                    "technique_id": "unknown",
                    "confidence": "analogical",
                    "note": "Skill-level trigger or hook persistence requires reviewer inspection before use.",
                },
                {
                    "framework": "MITRE ATT&CK Enterprise",
                    "tactic": "Defense Impairment",
                    "technique_id": "unknown",
                    "confidence": "analogical",
                    "note": "Reported attempt to interfere with local guards/scanners/logging.",
                },
            ],
            "sanitization_notes": [
                "This is a local Cisco-shaped fixture; Cisco code was not installed or executed.",
                "No SARIF raw result, repository path, bytecode blob, customer file, or secret is included.",
                "No VirusTotal, cloud analyzer, or external upload was performed by Rain.",
            ],
        },
        "skill_pipeline_taint",
    ),
]

DECISION_MATRIX = [
    {
        "condition": "critical_or_high_finding_against_exact_action_target",
        "suggested_move": "deny",
        "reason": "Do not proceed until target is fixed or a human explicitly accepts the risk.",
    },
    {
        "condition": "unknown_scanner_provenance_or_raw_output_unavailable",
        "suggested_move": "review",
        "reason": "Unknown provenance reduces confidence; it cannot support proceed by itself.",
    },
    {
        "condition": "clean_local_scan_with_clear_target_provenance",
        "suggested_move": "review_or_reduce_uncertainty",
        "reason": "No findings is not no risk; tool/payment/runtime policy must still pass.",
    },
    {
        "condition": "ics_ot_cyber_physical_target_with_non_read_only_action",
        "suggested_move": "review_or_deny",
        "reason": "Require authorization, passive-first posture, and no operational impact.",
    },
]
EVIDENCE_REQUIREMENTS_FOR_CLIENT = [
    "scanner name, version, origin URL, and policy name/version/fingerprint if available",
    "scan target type and exact action/tool/skill the finding applies to",
    "execution boundary: local_no_network, ci, sandbox, hosted, or unknown",
    "finding count, highest severity, categories, and finding engines",
    "whether raw output is included; default false and sanitized summaries only",
    "whether any external upload/cloud analyzer was used; default false",
    "optional ATT&CK-style mapping with confidence exact/analogical/weak and a reviewer disclaimer",
]

highest_severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4, "unknown": -1}
highest_observed = max(
    (str(item["highest_severity"]) for item in SCANNER_EVIDENCE),
    key=lambda severity: highest_severity_order.get(severity, -1),
)
agent_trust_action = "deny" if highest_severity_order[highest_observed] >= 3 else "review"

PACKET = {
    "contract_version": CONTRACT_VERSION,
    "purpose": "Convert sanitized scanner findings into Agent Trust pre-action evidence without executing scanner code.",
    "safety_boundary": SAFETY_BOUNDARY,
    # Keep the original single-evidence field for existing local doctors/consumers.
    "scanner_evidence": SCANNER_EVIDENCE[0],
    "additional_scanner_evidence": SCANNER_EVIDENCE[1:],
    "attack_mapping_disclaimer": ATTACK_MAPPING_DISCLAIMER,
    "decision_matrix": DECISION_MATRIX,
    "evidence_requirements_for_client": EVIDENCE_REQUIREMENTS_FOR_CLIENT,
    "agent_trust_move": {
        "action": agent_trust_action,
        "highest_observed_severity": highest_observed,
        "targets": [item["scan_target_type"] for item in SCANNER_EVIDENCE],
        "requires_human_review": True,
        "reasons": [
            "High/critical scanner findings affect exact tool, MCP, or skill-package targets.",
            "Scanner evidence is advisory evidence, not certification or automatic authority.",
            "Pre-action gate should not proceed until target is fixed or a human explicitly accepts risk.",
        ],
        "allowed_next_step": "share_sanitized_summary_with_reviewer",
    },
    "client_acquisition_ask": (
        "Send one sanitized scanner finding summary for a risky tool, MCP server, payment flow, or agent skill package; "
        "Agent Trust will map it to proceed, review, or deny before action."
    ),
}

print(json.dumps(PACKET, sort_keys=True, indent=2, ensure_ascii=False))
