#!/usr/bin/env python3
"""Agent Trust skill: a local pre-action gate for risky agent skill installs.

This script is deliberately dependency-free and inert. It performs no network
requests, no installs, no shell execution, no secret/env reads, no wallet access,
no signing, no payment, and no outreach. It only classifies an intended action
and returns a deterministic JSON decision for another agent or human to inspect.
"""
from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse

CONTRACT_VERSION = "agent-trust-skill.v1"
HARD_BOUNDARIES = [
    "no_network_calls_performed_by_this_skill",
    "no_install_or_shell_execution",
    "no_secret_or_environment_value_reads",
    "no_wallet_access_or_signing",
    "no_payment_or_real_money_action",
    "no_outreach_posting_or_account_action",
]

SECRET_PERMS = {"read_env", "env", "secrets", "read_secrets", "credentials", "tokens", "api_keys", "private_keys"}
NETWORK_PERMS = {"network", "external_upload", "http", "https", "telemetry", "egress"}
EXEC_PERMS = {"execute", "shell", "install_script", "postinstall", "subprocess", "run_code"}
WRITE_PERMS = {"repo_write", "write_files", "modify_repo", "filesystem_write"}
READONLY_PERMS = {"repo_read", "read_repo", "read_files", "diff_read", "metadata_read", "readonly", "read_only"}


def _authority_surface(perms: set[str]) -> list[str]:
    surface: list[str] = []
    if _contains_any(perms, READONLY_PERMS):
        surface.append("repository_or_workspace_read")
    if _contains_any(perms, WRITE_PERMS):
        surface.append("repository_or_workspace_write")
    if _contains_any(perms, SECRET_PERMS):
        surface.append("secret_or_environment_read")
    if _contains_any(perms, NETWORK_PERMS):
        surface.append("network_or_external_upload")
    if _contains_any(perms, EXEC_PERMS):
        surface.append("local_execution_or_install_hook")
    return surface or ["unspecified_authority_requires_review"]


def _exfiltration_paths(perms: set[str], source_classification: str) -> list[str]:
    paths: list[str] = []
    if _contains_any(perms, NETWORK_PERMS):
        paths.append("network_or_telemetry_egress")
    if _contains_any(perms, WRITE_PERMS):
        paths.append("repository_or_workspace_writeback")
    if _contains_any(perms, EXEC_PERMS):
        paths.append("install_or_runtime_script_side_effects")
    if source_classification == "untrusted_external_skill":
        paths.append("untrusted_component_receives_agent_context")
    return paths or ["no_direct_exfiltration_path_declared"]


def _lifecycle_hooks(perms: set[str]) -> list[str]:
    hooks = ["discovery", "pre_install_review"]
    if _contains_any(perms, EXEC_PERMS):
        hooks.extend(["install_script", "activation_or_runtime_execution"])
    else:
        hooks.append("activation_without_declared_execution")
    return hooks


def _dependency_inventory(
    *,
    action: str,
    source: str,
    url: str,
    source_classification: str,
    permissions: list[str],
    decision: str,
) -> dict:
    perms = set(permissions)
    return {
        "name": url or source,
        "component_kind": "agent_skill_or_plugin_dependency" if action == "install_skill" else "unsupported_component",
        "dependency_kind": "external_agent_extension" if source_classification == "untrusted_external_skill" else source_classification,
        "source": source,
        "url": url,
        "source_classification": source_classification,
        "requested_permissions": permissions,
        "authority_surface": _authority_surface(perms),
        "access_surface": _authority_surface(perms),
        "exfiltration_paths": _exfiltration_paths(perms, source_classification),
        "lifecycle_hooks": _lifecycle_hooks(perms),
        "provenance_evidence_not_trust": True,
        "review_requirement": (
            "block_install_until_source_review_sandbox_or_permission_reduction"
            if decision in {"deny_or_require_review", "require_review"}
            else "record_constraints_before_install_or_enable"
        ),
    }


def _split_permissions(values: list[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for part in value.split(","):
            normalized = part.strip().lower().replace("-", "_")
            if normalized:
                result.append(normalized)
    return sorted(set(result))


def _classify_source(source: str, url: str) -> str:
    text = f"{source} {url}".lower()
    parsed = urlparse(url)
    if source.lower() in {"local", "file"} or parsed.scheme == "file" or url.startswith("./") or url.startswith("../"):
        return "local_or_file_source"
    if any(marker in text for marker in ("github", "gitlab", "marketplace", "http://", "https://")):
        return "untrusted_external_skill"
    if parsed.scheme in {"http", "https", "git", "ssh"}:
        return "untrusted_external_skill"
    return "unknown_source_requires_review"


def _contains_any(perms: set[str], needles: set[str]) -> bool:
    return bool(perms.intersection(needles))


def check_action(args: argparse.Namespace) -> dict:
    permissions = _split_permissions(args.requested_permission)
    perms = set(permissions)
    action = args.action.strip().lower().replace("-", "_")
    source_classification = _classify_source(args.source, args.url)

    risk_signals: list[str] = []
    allowed_next_steps: list[str] = []
    forbidden_next_steps = [
        "run_untrusted_install_script_before_review",
        "grant_secret_or_env_access_to_untrusted_skill",
        "combine_secret_access_with_network_egress",
        "upload_repository_or_environment_context_before_review",
        "treat_discovery_or_popularity_as_trust",
    ]

    has_secret = _contains_any(perms, SECRET_PERMS)
    has_network = _contains_any(perms, NETWORK_PERMS)
    has_exec = _contains_any(perms, EXEC_PERMS)
    has_write = _contains_any(perms, WRITE_PERMS)
    readonly_only = bool(perms) and perms.issubset(READONLY_PERMS)

    if action != "install_skill":
        risk_signals.append("unsupported_action: this v1 skill only gives concrete policy for install_skill")

    if source_classification == "untrusted_external_skill":
        risk_signals.append("untrusted_external_skill: source is external and must not be treated as trusted by name or popularity")
    elif source_classification == "unknown_source_requires_review":
        risk_signals.append("unknown_source: provenance is insufficient for automatic install")

    if has_secret and has_network:
        risk_signals.append("network_exfiltration_path: secret/env/credential access combined with network or upload")
    if has_secret:
        risk_signals.append("secret_access_requested: install_skill warrant rarely justifies env/token/private-key access")
    if has_exec and source_classification != "local_or_file_source":
        risk_signals.append("untrusted_execution_requested: external install/postinstall/script execution requires review or sandbox")
    if has_write and source_classification == "untrusted_external_skill":
        risk_signals.append("repo_write_requested_by_external_skill: write access should follow source review and constrained sandboxing")
    if not args.warrant.strip():
        risk_signals.append("missing_warrant: intended task scope is empty")
    if not args.boundary.strip():
        risk_signals.append("missing_boundary: safety boundary is empty")

    secret_access_authorized = False
    if has_secret or (has_network and source_classification == "untrusted_external_skill") or has_exec:
        decision = "deny_or_require_review"
        allowed_next_steps = [
            "inspect_source_without_execution",
            "run_in_sandbox_without_env_or_secrets",
            "remove_secret_and_network_permissions",
            "request_human_or_security_review",
            "use_builtin_readonly_alternative",
        ]
    elif (
        readonly_only
        and source_classification in {"local_or_file_source", "untrusted_external_skill"}
        and args.warrant.strip()
        and args.boundary.strip()
    ):
        decision = "allow_with_constraints"
        allowed_next_steps = [
            "read_source_or_diff_only",
            "do_not_execute_install_scripts",
            "do_not_grant_env_or_secret_access",
            "do_not_upload_context",
            "record_decision_before_any_followup_action",
        ]
    else:
        decision = "review_optional" if not risk_signals else "require_review"
        allowed_next_steps = [
            "clarify_requested_permissions",
            "inspect_source_without_execution",
            "prefer_readonly_mode",
            "record_decision_before_install",
        ]

    if decision in {"deny_or_require_review", "require_review"}:
        forbidden_next_steps.append("continue_install_as_if_approved")

    return {
        "ok": True,
        "contract_version": CONTRACT_VERSION,
        "decision": decision,
        "action": action,
        "source": args.source,
        "url": args.url,
        "component_kind": "agent_skill_or_plugin_dependency" if action == "install_skill" else "unsupported_component",
        "dependency_kind": "external_agent_extension" if source_classification == "untrusted_external_skill" else source_classification,
        "source_classification": source_classification,
        "requested_permissions": permissions,
        "asbom": _dependency_inventory(
            action=action,
            source=args.source,
            url=args.url,
            source_classification=source_classification,
            permissions=permissions,
            decision=decision,
        ),
        "warrant": args.warrant,
        "boundary": args.boundary,
        "risk_signals": risk_signals,
        "allowed_next_steps": allowed_next_steps,
        "forbidden_next_steps": forbidden_next_steps,
        "secret_access_authorized": secret_access_authorized,
        "hard_boundaries": HARD_BOUNDARIES,
        "interpretation": "This is a pre-action decision only. It does not install, fetch, execute, read secrets, or authorize external action.",
    }


def manifest() -> dict:
    return {
        "ok": True,
        "contract_version": CONTRACT_VERSION,
        "name": "agent-trust-skill",
        "purpose": "Local dependency firewall before installing agent skills/plugins/MCP-like extensions.",
        "supply_chain_model": "External skills are dependencies with authority surface; provenance is evidence, not trust.",
        "asbom_fields": [
            "component_kind",
            "dependency_kind",
            "authority_surface",
            "exfiltration_paths",
            "lifecycle_hooks",
            "provenance_evidence_not_trust",
            "review_requirement",
        ],
        "entrypoint": "python3 -m agent_trust.skill check",
        "commands": {
            "manifest": "python3 -m agent_trust.skill manifest",
            "check_install_skill": "python3 -m agent_trust.skill check --action install_skill --source github --url <url> --requested-permission repo_read,read_env,network --warrant <why> --boundary <limits>",
        },
        "supported_actions": ["install_skill"],
        "decision_values": ["allow_with_constraints", "review_optional", "require_review", "deny_or_require_review"],
        "never_does": HARD_BOUNDARIES,
        "agent_rule": "Call this skill before installing or enabling any external skill/plugin. Treat deny_or_require_review as a stop until source review, sandboxing, or permission reduction changes the input.",
    }


def _print(obj: dict, compact: bool) -> None:
    print(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=None if compact else 2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Agent Trust skill gate")
    sub = parser.add_subparsers(dest="command", required=True)

    manifest_parser = sub.add_parser("manifest", help="emit agent-readable skill manifest")
    manifest_parser.add_argument("--compact", action="store_true", help="emit compact JSON")

    check = sub.add_parser("check", help="check an intended risky action")
    check.add_argument("--action", required=True)
    check.add_argument("--source", required=True)
    check.add_argument("--url", required=True)
    check.add_argument("--requested-permission", action="append", default=[], help="repeatable or comma-separated permission list")
    check.add_argument("--warrant", required=True, help="why this action is needed")
    check.add_argument("--boundary", required=True, help="limits that must not be crossed")
    check.add_argument("--compact", action="store_true", help="emit compact JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "manifest":
        _print(manifest(), args.compact)
        return 0
    if args.command == "check":
        _print(check_action(args), args.compact)
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
