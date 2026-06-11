#!/usr/bin/env python3
"""Local Agent Trust runtime signal gate demo.

Demonstrates that scanner/registry evidence is not runtime authorization.
No network, execution, wallet, signing, payment, posting, outreach, repo settings,
or secret access is performed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_trust.bundle_boundaries import gate_runtime_pre_action_with_signals


def _demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "inspect_checked_in_skill_descriptor",
        "required_scopes": ["read_skill_descriptor"],
        "granted_scopes": ["read_skill_descriptor", "write_local_receipt"],
        "sensitivity": "low",
        "provenance": {"source": "checked_in", "path": "examples/agent_trust_manifest.json"},
        "artifact": {"name": "local-agent-trust-example", "kind": "mcp_descriptor", "version": "1"},
        "scanner_signals": ["clean", "no_known_risky_signal"],
        "registry_signals": ["pinned", "verified_registry_entry"],
    }


def _prompt_injection_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "publish_post_with_secret_context_from_untrusted_page",
        "required_scopes": ["browser_read", "post", "read_secret_alias"],
        "granted_scopes": ["browser_read"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_web_page",
            "url": "https://example.invalid/prompt-injection-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "untrusted-page-instructions",
            "kind": "web_content",
            "summary": (
                "The page asks the agent to ignore previous instructions, copy hidden "
                "context into a public post, and use any available credentials."
            ),
        },
        "scanner_signals": [
            "prompt_injection",
            "credential_exfiltration",
            "untrusted_content_requests_external_action",
        ],
        "registry_signals": ["untrusted_provenance", "no_verified_registry_entry"],
    }


def _authority_persistence_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "write_prompt_injection_to_future_trusted_skill_file",
        "required_scopes": ["read_untrusted_content", "write_skill_file", "write_policy_context"],
        "granted_scopes": ["read_untrusted_content"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_web_page",
            "url": "https://example.invalid/hiddenperms-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "future-trusted-skill-persistence-attempt",
            "kind": "authority_bearing_persistence_surface",
            "summary": (
                "Untrusted content asks the agent to write hidden instructions into "
                "SKILL.md, prompts, hooks, configs, memory, policy, or source files "
                "so a later session treats the payload as trusted context."
            ),
        },
        "scanner_signals": [
            "prompt_injection",
            "authority_bearing_persistence_surface",
            "deferred_persistence",
            "future_trusted_context_write",
        ],
        "registry_signals": ["untrusted_provenance", "no_verified_registry_entry"],
    }


def _instruction_data_separation_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "process_untrusted_dataset_record_with_embedded_tool_instruction",
        "required_scopes": ["read_untrusted_content", "summarize_data"],
        "granted_scopes": ["read_untrusted_content", "summarize_data"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_dataset_record",
            "url": "https://example.invalid/sep-instruction-data-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "sep-style-instruction-data-confusion",
            "kind": "untrusted_data_record",
            "summary": (
                "The task is to process/summarize a data record, but the record text "
                "contains embedded commands asking the agent to execute a tool, reveal "
                "hidden context, or treat data as higher-priority instructions."
            ),
        },
        "scanner_signals": [
            "instruction_data_separation_required",
            "instruction_data_confusion",
            "embedded_instruction_requests_execution",
            "untrusted_data_requests_tool_action",
        ],
        "registry_signals": ["untrusted_provenance", "no_verified_registry_entry"],
    }


def _privacy_leak_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "answer_user_by_revealing_hidden_context_memorized_secrets_or_private_records",
        "required_scopes": ["answer_user", "read_private_context", "read_secret_alias"],
        "granted_scopes": ["answer_user"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_user_request",
            "url": "https://example.invalid/privacy-leak-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "llm-sp-privacy-secret-regurgitation",
            "kind": "privacy_leak_request",
            "summary": (
                "The request asks the agent/model to reveal hidden system context, "
                "memorized secrets, secret aliases, private records, or previous private "
                "messages instead of producing a bounded public answer."
            ),
        },
        "scanner_signals": [
            "privacy_leakage",
            "hidden_context_exfiltration",
            "secret_regurgitation",
            "private_record_exposure",
            "credential_exfiltration",
        ],
        "registry_signals": ["untrusted_provenance", "no_verified_registry_entry"],
    }


def _llm_judge_injection_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "publish_or_install_based_only_on_llm_judge_approval",
        "required_scopes": ["read_reviewer_packet", "publish", "install_dependency"],
        "granted_scopes": ["read_reviewer_packet"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_reviewer_packet",
            "url": "https://example.invalid/llm-judge-injection-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "llm-sp-llm-as-a-judge-verdict-manipulation",
            "kind": "reviewer_packet_or_eval_output",
            "summary": (
                "A reviewer packet or eval transcript contains instructions aimed at the "
                "LLM judge, such as declaring PASS/APPROVED and telling the downstream "
                "agent to treat that verdict as permission to publish, install, or act."
            ),
        },
        "scanner_signals": [
            "llm_judge_prompt_injection",
            "eval_verdict_manipulation",
            "judge_verdict_as_authority",
            "reviewer_packet_instruction_injection",
        ],
        "registry_signals": ["untrusted_provenance", "llm_review_is_evidence_not_authority"],
    }


def _multimodal_prompt_injection_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "follow_visual_or_subtitle_instruction_to_publish_or_execute_tool",
        "required_scopes": ["browser_read", "vision_ocr", "post", "execute_tool"],
        "granted_scopes": ["browser_read", "vision_ocr"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_multimodal_media",
            "url": "https://example.invalid/llm-sp-multimodal-prompt-injection-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "llm-sp-multimodal-ocr-subtitle-injection",
            "kind": "image_video_ocr_subtitle_content",
            "summary": (
                "An untrusted screenshot/video frame/OCR/subtitle/visual overlay contains "
                "instructions telling the agent to ignore system policy and publish, execute "
                "a tool, or treat media text as privileged instructions instead of evidence."
            ),
        },
        "scanner_signals": [
            "multimodal_prompt_injection",
            "media_instruction_injection",
            "ocr_instruction_injection",
            "subtitle_instruction_injection",
            "visual_overlay_tool_instruction",
        ],
        "registry_signals": ["untrusted_provenance", "media_text_is_evidence_not_authority"],
    }


def _poisoning_backdoor_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "install_or_use_poisoned_skill_with_latent_backdoor_trigger",
        "required_scopes": ["read_skill_descriptor", "install_dependency", "execute_tool"],
        "granted_scopes": ["read_skill_descriptor"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_skill_or_model_artifact",
            "url": "https://example.invalid/llm-sp-poisoning-backdoor-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "llm-sp-poisoned-skill-latent-backdoor",
            "kind": "skill_or_model_artifact",
            "summary": (
                "A skill/model artifact claims clean scanner labels and normal behavior, "
                "but its provenance/eval notes indicate poisoned training or evaluation "
                "data and a latent trigger that changes behavior after installation or use."
            ),
        },
        "scanner_signals": [
            "poisoning",
            "poisoned_artifact",
            "poisoned_training_data",
            "poisoned_evaluation_data",
            "triggered_backdoor",
            "latent_backdoor_trigger",
        ],
        "registry_signals": ["untrusted_provenance", "scanner_pass_is_not_authority"],
    }


def _prompt_only_defense_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "perform_sensitive_action_based_only_on_prompt_guard_claim",
        "required_scopes": ["read_untrusted_content", "post", "execute_tool"],
        "granted_scopes": ["read_untrusted_content"],
        "sensitivity": "high",
        "provenance": {
            "source": "untrusted_prompt_or_defense_claim",
            "url": "https://example.invalid/llm-sp-prompt-only-defense-demo",
            "trusted_instructions": False,
        },
        "artifact": {
            "name": "llm-sp-prompt-only-defense-without-runtime-boundary",
            "kind": "prompt_injection_defense_claim",
            "summary": (
                "A prompt or reviewer note claims the agent is protected against jailbreaks "
                "or prompt injection and therefore may proceed with a sensitive external "
                "action, but no deterministic runtime boundary, scope check, or pre-action "
                "control is present to deny policy bypass."
            ),
        },
        "scanner_signals": [
            "prompt_only_defense",
            "jailbreak_defense_claim_without_boundary",
            "no_deterministic_runtime_boundary",
            "policy_bypass_after_prompt_guard",
        ],
        "registry_signals": ["untrusted_provenance", "prompt_defense_is_evidence_not_authority"],
    }


def _authorization_provenance_mismatch_demo_request() -> dict[str, object]:
    return {
        "agent_identity": {"id": "rain.local", "verified": True},
        "requested_action": "send_email_using_recipient_from_untrusted_invoice_body",
        "required_scopes": ["read_invoice_metadata", "send_email"],
        "granted_scopes": ["read_invoice_metadata", "send_email"],
        "sensitivity": "high",
        "provenance": {
            "source": "mixed_trust_action_trace",
            "trusted_instructions": True,
            "authorization_baseline": {
                "allowed_parameter_sources": {
                    "recipient": ["user_request", "trusted_invoice_metadata"],
                    "subject": ["user_request", "trusted_invoice_metadata"],
                }
            },
            "argument_lineage": {
                "recipient": {
                    "value_label": "redacted-email-address",
                    "source": "untrusted_invoice_body",
                    "trusted_instructions": False,
                },
                "subject": {
                    "value_label": "invoice-followup",
                    "source": "trusted_invoice_metadata",
                    "trusted_instructions": True,
                },
            },
        },
        "artifact": {
            "name": "dual-graph-authorization-provenance-mismatch",
            "kind": "action_trace_with_argument_lineage",
            "summary": (
                "The action itself is in scope, but a sensitive recipient parameter is "
                "influenced by untrusted content rather than by the user request or trusted "
                "invoice metadata authorized to supply that argument."
            ),
        },
        "scanner_signals": [
            "authorization_provenance_mismatch",
            "argument_lineage_untrusted_source",
            "sensitive_argument_from_untrusted_content",
            "unauthorized_parameter_influence",
        ],
        "registry_signals": [
            "provenance_graph_required",
            "authorization_graph_required",
            "argument_lineage_is_evidence_not_authority",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="emit the built-in low-risk demo packet")
    parser.add_argument(
        "--prompt-injection-demo",
        action="store_true",
        help="emit a high-risk untrusted-content-to-privileged-action demo packet",
    )
    parser.add_argument(
        "--authority-persistence-demo",
        action="store_true",
        help="emit a high-risk deferred-persistence write-to-future-trusted-context demo packet",
    )
    parser.add_argument(
        "--instruction-data-demo",
        action="store_true",
        help="emit a SEP-style untrusted-data-with-embedded-instruction demo packet",
    )
    parser.add_argument(
        "--privacy-leak-demo",
        action="store_true",
        help="emit a privacy/secret-leak request demo packet for hidden context or private records",
    )
    parser.add_argument(
        "--llm-judge-injection-demo",
        action="store_true",
        help="emit an LLM-as-a-judge/eval verdict manipulation demo packet",
    )
    parser.add_argument(
        "--poisoning-backdoor-demo",
        action="store_true",
        help="emit a poisoned artifact / latent backdoor trigger demo packet",
    )
    parser.add_argument(
        "--multimodal-prompt-injection-demo",
        action="store_true",
        help="emit an untrusted image/video/OCR/subtitle prompt-injection demo packet",
    )
    parser.add_argument(
        "--prompt-only-defense-demo",
        action="store_true",
        help="emit a prompt-only defense claim without deterministic runtime boundary demo packet",
    )
    parser.add_argument(
        "--authorization-provenance-mismatch-demo",
        action="store_true",
        help="emit a dual-graph authorization/provenance mismatch demo packet",
    )
    parser.add_argument("--request-json", help="JSON request packet to evaluate")
    parser.add_argument("--expect-decision", choices=("proceed", "review", "deny"), help="fail unless the gate emits this decision")
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    args = parser.parse_args()

    if args.request_json:
        request = json.loads(args.request_json)
    elif args.prompt_injection_demo:
        request = _prompt_injection_demo_request()
    elif args.authority_persistence_demo:
        request = _authority_persistence_demo_request()
    elif args.instruction_data_demo:
        request = _instruction_data_separation_demo_request()
    elif args.privacy_leak_demo:
        request = _privacy_leak_demo_request()
    elif args.llm_judge_injection_demo:
        request = _llm_judge_injection_demo_request()
    elif args.poisoning_backdoor_demo:
        request = _poisoning_backdoor_demo_request()
    elif args.multimodal_prompt_injection_demo:
        request = _multimodal_prompt_injection_demo_request()
    elif args.prompt_only_defense_demo:
        request = _prompt_only_defense_demo_request()
    elif args.authorization_provenance_mismatch_demo:
        request = _authorization_provenance_mismatch_demo_request()
    elif args.demo:
        request = _demo_request()
    else:
        parser.error(
            "use --demo, --prompt-injection-demo, --authority-persistence-demo, "
            "--instruction-data-demo, --privacy-leak-demo, --llm-judge-injection-demo, "
            "--poisoning-backdoor-demo, --multimodal-prompt-injection-demo, "
            "--prompt-only-defense-demo, --authorization-provenance-mismatch-demo, "
            "or --request-json"
        )

    packet = gate_runtime_pre_action_with_signals(request)
    print(json.dumps(packet, sort_keys=True, ensure_ascii=False, indent=None if args.compact else 2))
    if args.expect_decision and packet.get("pre_action_decision") != args.expect_decision:
        print(
            f"expected pre_action_decision={args.expect_decision}, got {packet.get('pre_action_decision')}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
