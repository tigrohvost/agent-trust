# Agent Trust examples

> Agent readers: begin at root [`SKILL.md`](../SKILL.md), then read
> [`../docs/AGENT_TRUST_FOR_AGENTS.md`](../docs/AGENT_TRUST_FOR_AGENTS.md) before using example files.
> Primary machine-readable discovery/review surfaces: `agent_trust_agent_landing.json`, `agent_trust_manifest.json`, and `agent_trust_review_packet.json`.

Small, copy-pasteable artifacts for integrating the local **Agent Trust Bundle** contract. This is not an SDK: it is the shortest path from one checkout command to deterministic trust-bundle output.

Every file in this directory is local-only: no network calls, no wallet access, no execution of untrusted input, no signing, no payments, no outreach.

## Files

| File | Purpose |
|------|---------|
| `agent_trust_adoption_readiness.py` | Summarize local Agent Trust adoption readiness without external action. |
| `agent_trust_agent_landing.json` | Canonical self-readable one-hop landing packet for agents: root entrypoint, guide, proof commands, integration decision, and hard stops. |
| `agent_trust_atr_advisory_check.py` | Tiny dependency-free ATR-inspired advisory checker with pinned local rules, scan-target gating, TP/TN fixtures, and sanitized Agent Trust findings without fetching ATR or executing external scanners. |
| `agent_trust_base_sepolia_live_boundary.py` | Dry-run-only boundary describing the future live Base Sepolia x402 client command/env/logging/stop contract without performing the live call. |
| `agent_trust_base_sepolia_preflight.py` | Secret-safe local readiness preflight for a future Base Sepolia x402 testnet transaction; performs no network, wallet, signing, or payment. |
| `agent_trust_checksums.json` | SHA-256 checksums for the checked-in example artifacts. |
| `agent_trust_consumer_decision.py` | Example external-agent decision over manifest + review packet + doctor output, returning `integrate_experimentally` or `abstain`. |
| `agent_trust_doctor.py` | CI/agent-friendly local consistency doctor for checked-in Agent Trust examples, schemas, manifest, request wrapper, and golden verifier. |
| `agent_trust_efficacy_benchmark.py` | Local synthetic efficacy benchmark for Agent Trust advisory classifiers. |
| `agent_trust_evidence_transcript.py` | Reviewer-facing local evidence transcript summarizing doctor, adoption-readiness, and daily-review proof without external action. |
| `agent_trust_framework_gate.py` | Tiny dependency-free framework-shaped pre-action gate example mapping Agent Trust bundle verdicts to `proceed`, `review`, or `deny` without performing the risky action. |
| `agent_trust_idea_selector.py` | Select the next Agent Trust improvement from a small scored idea list. |
| `agent_trust_import.py` | Minimal direct Python import example for calling `build_agent_trust_bundle` in-process without CLI subprocesses or local HTTP. |
| `agent_trust_layered_skill_scanning.py` | Dependency-free local layered skill-scanning receipt aggregating malware/reputation, static-analysis, MCP supply-chain/RCE, agentic semantic-risk, provenance/moderation, and scanner-disagreement evidence into `proceed` / `review` / `deny` without external scanners or untrusted execution. |
| `agent_trust_manifest.json` | Agent-discoverable manifest mapping artifacts, entrypoints, docs, schemas, safety boundary, and success signals. |
| `agent_trust_request.py` | Prints the canonical versioned Agent Trust request JSON. Use it to see the current input shape or regenerate `agent_trust_input.json`. |
| `agent_trust_review_decision_gate.py` | Review-only local decision gate that consumes the evidence transcript and states permitted reviewer decisions while refusing outreach, live testnet, wallet, signing, payment, and real money. |
| `agent_trust_review_packet.json` | Machine-readable external review packet naming local proof commands, canonical artifacts, review questions, stop conditions, and success signals. |
| `agent_trust_runtime_signal_gate.py` | Local Agent Trust runtime signal gate demo. |
| `agent_trust_scanner_evidence.py` | Local sanitized scanner-evidence packet mapping scanner findings to an Agent Trust pre-action move without executing scanner code. |
| `agent_trust_static_scope_check.py` | Local Agent Trust static scope/manifest consistency check. |
| `agent_trust_temporal_multimodal_checklist.py` | Local Agent Trust temporal-multimodal prompt-injection checklist. |
| `agent_trust_trajectory_eval.py` | Local Agent Trust trajectory/stateful eval harness. |
| `agent_trust_verify.py` | One-command first-run verifier: runs the local CLI against the sample request and compares output to the checked-in golden bundle. |
| `agent_trust_zero_trust_gate.py` | Local Agent Trust Zero-Trust identity/policy pre-action gate demo. |
| `ideas.json` | Local Agent Trust example artifact. |
| `input.json` | Checked-in sample request with explicit `contract_version`. Feed this into the CLI or local HTTP endpoint. |
| `output.json` | Checked-in golden output for the sample request, useful for comparing fields and wiring tests. |
| `skill_manifest.json` | Machine-readable local install/discovery contract for the Agent Trust Skill: entrypoint, supported action, verdict fields, hard stops, validation commands, and install/use boundary for agent-readable setup. |

## Shortest proof path

```bash
python3 -m agent_trust.cli --print-contract
python3 -m agent_trust.cli examples/input.json
python3 examples/agent_trust_verify.py
python3 examples/agent_trust_doctor.py
```

Expected: exit code 0 everywhere; the doctor prints JSON with `ok: true`.
