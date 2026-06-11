# Agent Trust examples

> Agent readers: begin at root [`AGENTS.md`](../../AGENTS.md), then read
> [`../AGENT_TRUST_FOR_AGENTS.md`](../AGENT_TRUST_FOR_AGENTS.md) before using example files.
> Primary machine-readable discovery/review surfaces: `agent_trust_agent_landing.json`, `agent_trust_manifest.json`, and `agent_trust_review_packet.json`.

Small, copy-pasteable artifacts for integrating the local **Agent Trust Bundle** contract. This is not an SDK: it is the shortest path from one checkout command to deterministic trust-bundle output.

## Files

| File | Purpose |
|------|---------|
| `agent_trust_boundary_intake.py` | Dependency-free local classifier that maps a descriptor into reusable Agent Trust / ISC-Bench defensive boundaries with allow/review/deny/quarantine verdicts before execution or external action. |
| `agent_trust_skill.py` | Dependency-free installable Agent Trust skill CLI for pre-action checks before installing external skills/plugins; emits deterministic JSON and performs no network, install, execution, secret, wallet, payment, or outreach action. |
| `agent_trust_skill_manifest.json` | Machine-readable local install/discovery contract for the Agent Trust Skill: entrypoint, supported action, verdict fields, hard stops, validation commands, and install/use boundary for agent-readable setup. |
| `agent_trust_skill_installability_check.py` | Dependency-free local self-check proving the skill manifest points to a usable entrypoint, supports `install_skill`, and emits ASBOM/review-only boundaries for a dangerous external skill install. |
| `agent_trust_request.py` | Prints the canonical versioned Agent Trust request JSON. Use it to see the current input shape or regenerate `agent_trust_input.json`. |
| `agent_trust_import.py` | Minimal direct Python import example for calling `build_agent_trust_bundle` in-process without CLI subprocesses or local HTTP. |
| `agent_trust_input.json` | Checked-in sample request with explicit `contract_version`. Feed this into the CLI or local HTTP endpoint. |
| `agent_trust_output.json` | Checked-in golden output for the sample request, useful for comparing fields and wiring tests. |
| `agent_trust_verify.py` | One-command first-run verifier: runs the local CLI against the sample request and compares output to the checked-in golden bundle. |
| `agent_trust_doctor.py` | CI/agent-friendly local consistency doctor for checked-in Agent Trust examples, schemas, manifest, request wrapper, and golden verifier. |
| `agent_trust_launch_readiness.py` | Dependency-free local launch-readiness check for Agent Trust free-user preparation; reports required artifacts, honest blockers, next actions, and safety boundary without network, wallet, signing, payment, scanner execution, or runtime imports. |
| `agent_trust_free_user_feedback.py` | Dependency-free local template generator for sanitized external free-user feedback after the readiness/first-run proof; sends nothing and reads no secrets. |
| `agent_trust_free_review_intake.py` | Dependency-free local free-review intake packet generator for public agent-security artifacts; maps sanitized descriptions/actions/risk surfaces to bundle, reviewer rubric, ATR rule-hit packet, tool-call provenance gate, or abstain without fetching, scanners, installs, wallets, signing, payment, posting, or outreach. |
| `agent_trust_agent_landing.json` | Canonical self-readable one-hop landing packet for agents: root entrypoint, guide, proof commands, integration decision, and hard stops. |
| `agent_trust_case_memory.py` | Dependency-free Rain-native Agent Trust case-memory seed for local cases, provenance, threat signals, decisions, and gap summaries; inspired by gbrain brain-layer patterns without importing gbrain code or adding network/runtime dependencies. |
| `agent_trust_manifest.json` | Agent-discoverable manifest mapping artifacts, entrypoints, docs, schemas, safety boundary, and success signals. |
| `agent_trust_review_packet.json` | Machine-readable external review packet naming local proof commands, canonical artifacts, review questions, stop conditions, and success signals. |
| `agent_trust_schema.json` | Compact schema-like overview artifact for input, output, safety boundary, supported versions, and error envelopes. |
| `schemas/agent_trust_request.schema.json` | Draft 2020-12 JSON Schema for accepted request JSON. |
| `schemas/agent_trust_bundle.schema.json` | Draft 2020-12 JSON Schema for emitted trust bundle JSON. |
| `schemas/agent_trust_manifest.schema.json` | Draft 2020-12 JSON Schema for the agent-discoverable examples manifest. |
| `agent_trust_http_client.py` | Minimal standard-library client for posting the sample request to the local HTTP endpoint at `127.0.0.1`. |
| `agent_trust_live_self_use.py` | Local self-use runner for `/api/agent-trust/bundle`: posts `agent_trust_input.json`, checks malformed rejection with `invalid_agent_trust_input`, exercises canonical task-label variants, and correlates request-id/bundle-id audit summaries using safe fields only. |
| `agent_trust_consumer_decision.py` | Example external-agent decision over manifest + review packet + doctor output, returning `integrate_experimentally` or `abstain`. |
| `agent_trust_framework_gate.py` | Tiny dependency-free framework-shaped pre-action gate example mapping Agent Trust bundle verdicts to `proceed`, `review`, or `deny` without performing the risky action. |
| `agent_trust_agent_integration_recipe.md` | Minimal agent-integration recipe showing how another agent wraps Agent Trust as a pre-action gate before risky browser/tool/payment-like actions, with request shape, decision mapping, boundaries, proof commands, and stop conditions. |
| `agent_trust_codex_context_pack.md` | Sanitized prompt context pack for delegating Agent Trust / agent-security Codex tasks without ingesting Rain core memory, secrets, logs, knowledge, or gbrain. |
| `agent_trust_tool_call_provenance_case.json` | Local no-execution adoption case for the tool-call provenance gate, classifying an untrusted network-to-shell proposed call as deny before dispatch. |
| `agent_trust_base_sepolia_preflight.py` | Secret-safe local readiness preflight for a future Base Sepolia x402 testnet transaction; performs no network, wallet, signing, or payment. |
| `agent_trust_base_sepolia_live_boundary.py` | Dry-run-only boundary describing the future live Base Sepolia x402 client command/env/logging/stop contract without performing the live call. |
| `agent_trust_evidence_transcript.py` | Reviewer-facing local evidence transcript summarizing doctor, adoption-readiness, and daily-review proof without external action. |
| `agent_trust_review_decision_gate.py` | Review-only local decision gate that consumes the evidence transcript and states permitted reviewer decisions while refusing outreach, live testnet, wallet, signing, payment, and real money. |
| `agent_trust_scanner_evidence.py` | Local sanitized scanner-evidence packet mapping scanner findings to an Agent Trust pre-action move without executing scanner code. |
| `agent_trust_layered_skill_scanning.py` | Dependency-free local layered skill-scanning receipt aggregating malware/reputation, static-analysis, MCP supply-chain/RCE, agentic semantic-risk, provenance/moderation, and scanner-disagreement evidence into `proceed` / `review` / `deny` without external scanners or untrusted execution. |
| `agent_trust_atr_rule_hit_evidence.py` | Local sanitized ATR-style rule-hit evidence packet mapping rule hits to an Agent Trust pre-action decision without fetching feeds, executing scanners, installing skills/MCP servers, or external action. |
| `agent_trust_atr_advisory_check.py` | Tiny dependency-free ATR-inspired advisory checker with pinned local rules, scan-target gating, TP/TN fixtures, and sanitized Agent Trust findings without fetching ATR or executing external scanners. |
| `agent_trust_agent_security_evidence.py` | Local sanitized agent-security evidence packet for memory/context, planning, tool/MCP, orchestration, and task-warrant risks; maps evidence to review/deny without external action. |
| `agent_trust_incident_casebook.py` | Local sanitized reviewer casebook covering wallet/tool prompt injection, MCP/tool poisoning, and cross-prompt tool-call attempt classes without raw exploit replay or external action. |
| `agent_trust_workflow_pressure_gate.py` | Local ISC-Bench-informed workflow-pressure gate for validator/test/schema/fidelity pressure before untrusted execution. |
| `agent_trust_cross_surface_intake.py` | Local cross-surface intake gate for workflow-induced risk across prompts, repos, web text, tool/MCP descriptors, and inter-agent messages before execution/action. |
| `agent_trust_intake_review_packet.py` | Local intake integration packet for user-supplied or synthetic prompt/repo/web/tool-MCP/inter-agent text before any execution or external action. |
| `agent_trust_intake_contract_check.py` | Local ISC intake contract check keeping cross-surface intake and intake review packet surfaces, decisions, and workflow-pressure signals aligned without external action. |
| `agent_trust_benchmark_intake_evidence.py` | Local benchmark-intake evidence packet for synthetic or user-supplied ISC-like benchmark/repo/task snippets before inspecting untrusted benchmark materials or running tests/validators/tools. |
| `agent_trust_publication_readiness.py` | Local anti-drift checker for the Show HN / first-review packet: canonical Sepolia address, no confirmed funding, faucet stop states, proof commands, and no-external-action boundaries. |
| `agent_trust_prelaunch_gate.py` | One-command local HN/client-review prelaunch gate composing doctor, adoption readiness, publication readiness, evidence transcript, and review decision gate into `proceed_to_human_review` / `needs_update` / `stop`. |
| `agent_trust_reviewer_handoff.py` | Compact first-review handoff JSON composing prelaunch/evidence/publication/adoption checks into commands, output meanings, Sepolia limitation, reviewer decision, and pilot signal without external action. |
| `agent_trust_reviewer_decision_dry_run.py` | Local dry-run for the expected first reviewer decision, including required evidence fields, pass/fail rubric, pilot signal mapping, and stop conditions without external action. |
| `agent_trust_reviewer_response_packet.py` | Exact machine-readable first-reviewer response shape (`accepted` / `rejected` / `needs_update`) filled from local handoff and decision dry-run outputs without external action. |
| `agent_trust_first_pilot_review_check.py` | One-command local first-pilot review-path checker composing reviewer response and provenance decision outputs into a single review-only readiness verdict. |
| `agent_trust_first_review_feedback_classifier.py` | Dependency-free local classifier for sanitized first-review feedback; maps one reviewer finding to the next smallest local product move while preserving review-only/no-external-action boundaries. |
| `rain_x_twitter_bootstrap.py` | Local no-network/no-login/no-posting X/Twitter bootstrap packet with first tweet drafts, reply discipline, hashtags, and hard stops before legitimate account bootstrap. |
| `rain_external_comms_preflight.py` | Local no-network Gmail/X readiness preflight that checks secret-safe OAuth/API aliases, distinguishes browser fallback credentials, and reports exact blockers without exposing secret values. |
| `rain_x_signal_drafts.py` | Local no-network/no-posting converter from read-only X threat-watch JSON into compact draft posts with hashtags and safety boundaries. |
| `rain_x_draft_review_gate.py` | Local no-network/no-posting review gate for X draft posts, classifying each as `post_candidate` or `hold` with reasons before any live post. |
| `rain_x_browser_post.py` | Bounded X/Twitter browser fallback poster with dry-run default, confirmed-post mode, post UI diagnostics, and an offline `--recovery-runbook` for stable logged-out-session recovery without inspecting cookies/tokens/localStorage or posting blindly. |
| `rain_self_evolution_candidate_gate.py` | Dependency-free Hermes-inspired self-evolution candidate gate for Rain: evaluates proposed variants against execution traces, source provenance, size/tool-description limits, semantic preservation, validation metadata, and evidence-not-authority boundaries without network, secrets, untrusted execution, file mutation, or git operations. |
| `rain_memory_lifecycle_contract.py` | Dependency-free local Hermes/Hindsight-inspired memory lifecycle contract for Rain: models `pre_llm_call` / `post_llm_call`, bounded sanitized memory selection, context/tools/hybrid/manual modes, explicit persistence gates, and a composed memory-turn packet simulator without cloud SDKs, network, secrets, writes, or live context mutation. |
| `rain_autonomous_workspace_contract.py` | Dependency-free OpenClaw-inspired autonomous workspace loop contract: safe observation, state classification, smallest allowed action, re-observation, recovery, and hard-stop boundaries for real-browser/tool tasks; includes GitHub identity as a scenario without reading secrets or bypassing anti-abuse. |
| `rain_github_cdp_handoff.py` | Transport-only plus safe state-observation Chromium/CDP handoff for Rain-owned GitHub signup verification using persistent profile `/opt/ouroboros/data/browser-profiles/identity-rain` and local endpoint `127.0.0.1:9223`; can emit an OpenClaw-style agent loop contract and sanitized CDP page summaries, but reads no secrets/cookies/storage/DOM password fields and does not bypass CAPTCHA or anti-abuse checks. |
| `rain_codegraph_trial_gate.py` | Dependency-free CodeGraph quarantined trial gate for a future local semantic-code-navigation review; blocks first-pass `curl|sh`, `codegraph install`, MCP/agent auto-config, external config mutation, and secret indexing while defining success criteria, stop conditions, and rollback evidence. |


Print the Agent Trust case-memory seed and gap summary:

```bash
python3 examples/agent_trust_case_memory.py --demo --compact
python3 examples/agent_trust_case_memory.py --demo --gap-summary --compact
```

Boundary: this artifact uses embedded demo data only by default. It performs no network calls, wallet/signing/payment behavior, secret/env reads, external execution, arbitrary file reads, outreach, or repository settings changes. It is advisory evidence only, not certification or authority to act.

Print the CodeGraph quarantined trial gate before any install/MCP integration attempt:

```bash
python3 examples/rain_codegraph_trial_gate.py --compact
```

Boundary: this gate performs no network calls, installs, MCP startup, external agent config mutation, secret/env/cookie/storage reads, wallet/payment/signing, outreach, or repository settings changes. It is review evidence only, not authority to integrate CodeGraph into the live runtime.

Print the Hermes-inspired Rain self-evolution candidate gate receipts:

```bash
python3 examples/rain_self_evolution_candidate_gate.py --scenario hermes-inspired --expect-decision proceed --compact
python3 examples/rain_self_evolution_candidate_gate.py --scenario unsupported-mutation --expect-decision deny --compact
python3 examples/rain_self_evolution_candidate_gate.py --scenario semantic-drift --expect-decision deny --compact
```

Boundary: this gate is review evidence only. It performs no network calls, secret/env reads, untrusted execution, file mutation, or git operations; candidate approval is not automatic authority to mutate Rain.

Print the generic Rain autonomous workspace loop contract, or the GitHub identity scenario adapted from OpenClaw/Xiaona-style real-browser state loops:

```bash
python3 examples/rain_autonomous_workspace_contract.py --scenario generic
python3 examples/rain_autonomous_workspace_contract.py --scenario github_identity --compact
```

Boundary: this contract is process guidance only. It performs no browsing, login, posting, email sending, wallet, payment, signing, secret reading, cookie/storage inspection, or anti-abuse bypass.

Print the GitHub identity browser/CDP handoff instructions or check/restore the local Chromium endpoint:

```bash
python3 examples/rain_github_cdp_handoff.py --handoff
python3 examples/rain_github_cdp_handoff.py --agent-loop-contract
python3 examples/rain_github_cdp_handoff.py --check
python3 examples/rain_github_cdp_handoff.py --pages
python3 examples/rain_github_cdp_handoff.py --restart --url https://github.com/signup?social=false
```

Boundary: this helper is transport-only plus sanitized state observation for legitimate Rain-owned GitHub identity work. It does not read secrets, cookies, localStorage/sessionStorage, DOM password fields, or verification tokens; it does not solve or bypass CAPTCHA / anti-abuse checks.

Print the stable X/Twitter posting recovery contract when the persistent browser session is logged out or unclear:

```bash
python3 examples/rain_x_browser_post.py --recovery-runbook
```

## Machine-readable schemas

- `schemas/agent_trust_request.schema.json` — JSON Schema for the request accepted by the CLI and local HTTP bundle endpoint.
- `schemas/agent_trust_bundle.schema.json` — JSON Schema for the deterministic bundle output.
- `schemas/agent_trust_manifest.schema.json` — JSON Schema for the agent-discoverable examples manifest.

These schemas are intentionally honest about the current local contract: the outer request/output envelopes are stable and machine-readable, while `policy` and `tool_descriptor` stay flexible because the implementation inspects them without network calls, wallet access, or execution. The canonical request also includes `intended_integration_context` so a buyer or consumer can state where the pre-action trust gate would sit in their agent loop.


Inspect a runtime pre-action gate denial for prompt-injection content trying to mix untrusted web instructions, secret context, and posting/external action:

```bash
python3 examples/agent_trust_runtime_signal_gate.py --prompt-injection-demo --expect-decision deny --compact
python3 examples/agent_trust_runtime_signal_gate.py --instruction-data-demo --expect-decision deny --compact
python3 examples/agent_trust_runtime_signal_gate.py --privacy-leak-demo --expect-decision deny --compact
```

Inspect a runtime pre-action gate denial for HiddenPerms-style deferred persistence: untrusted content trying to write instructions into a future-trusted skill, prompt, hook, config, memory, policy, or source surface:

```bash
python3 examples/agent_trust_runtime_signal_gate.py --authority-persistence-demo --expect-decision deny --compact
```

Inspect a sanitized scanner-evidence packet and its pre-action move:

```bash
python3 examples/agent_trust_scanner_evidence.py
```


Inspect the layered skill-scanning receipt, including MCP supply-chain/RCE-style denial signals:

```bash
python3 examples/agent_trust_layered_skill_scanning.py --expect-decision deny --fail-on-fail
```

Inspect a sanitized ATR-style rule-hit evidence packet and its pre-action decision:

```bash
python3 examples/agent_trust_atr_rule_hit_evidence.py
```

Inspect the local incident casebook evidence packet for public wallet/tool injection, MCP poisoning, and cross-prompt tool-call attempts:

```bash
python3 examples/agent_trust_incident_casebook.py --pretty
```


Check the current local launch-readiness state before larger free-user launch slices:

```bash
python3 examples/agent_trust_launch_readiness.py
```

Emit a sanitized free-user feedback template after the proof:

```bash
python3 examples/agent_trust_free_user_feedback.py --sample
```

Route a sanitized public agent-security artifact or incident class to the right Agent Trust evidence path:

```bash
python3 examples/agent_trust_free_review_intake.py --all-samples
python3 examples/agent_trust_free_review_intake.py --sample mcp_tool_description
```


Run the installable Agent Trust skill gate before adding an external skill/plugin:

```bash
python3 examples/agent_trust_skill.py manifest
python3 examples/agent_trust_skill.py manifest --compact
python3 -m json.tool examples/agent_trust_skill_manifest.json
python3 examples/agent_trust_skill_installability_check.py
python3 examples/agent_trust_skill.py check \
  --action install_skill \
  --source github \
  --url https://github.com/example/pr-review-helper \
  --requested-permission repo_read,read_env,network \
  --warrant "summarize current PR only" \
  --boundary "no secrets, no external upload, no credential access"
```

Classify a descriptor into reusable Agent Trust / ISC-Bench defensive boundaries:

```bash
python3 examples/agent_trust_boundary_intake.py --demo
```

## Shortest checkout smoke test

From the repository root:

```bash
bash scripts/agent_trust_first_run.sh
```

This runs request inspection, the local CLI, golden-output verification, and the full examples-packet doctor without network, wallet, execution, or real-money behavior. The final JSON is the doctor result.

Ask a consumer-style agent decision whether the packet is coherent enough for experimental local integration:

```bash
python3 examples/agent_trust_consumer_decision.py
```

Summarize local adoption readiness from doctor, consumer-decision, and framework-gate evidence:

```bash
python3 examples/agent_trust_adoption_readiness.py
```

Check publication/readiness claims before any Hacker News, Foresyn, or first-review use:

```bash
python3 examples/agent_trust_publication_readiness.py
```

Run the composed local prelaunch gate before any HN/client-review decision:

```bash
python3 examples/agent_trust_prelaunch_gate.py
```

Generate a reviewer-facing local evidence transcript before sharing the packet for review:

```bash
python3 examples/agent_trust_evidence_transcript.py
```

Emit a local first integration ticket with the recommended path, acceptance criteria, reviewer questions, stop conditions, and first-blocker prompt:

```bash
python3 examples/agent_trust_integration_ticket.py
```

For the shortest first-review loop, start with the reviewer decision dry-run, then inspect the local unsent decision packet it authorizes. This is the cold path from machine-readable discovery to runnable evidence to the first-reviewer/client decision surface:

```bash
python3 examples/agent_trust_reviewer_decision_dry_run.py
# then inspect docs/AGENT_TRUST_FIRST_PILOT_REVIEW_PACKET.md
```

The decision packet is also exposed in `agent_trust_manifest.json` as `first_pilot_review_packet`.

If the reviewer wants a broader integration blocker prompt or a machine-readable response shape, run the integration ticket and then the reviewer response packet. The first names the blocker prompt; the second gives the exact machine-readable shape for returning the signal:

```bash
python3 examples/agent_trust_integration_ticket.py
python3 examples/agent_trust_reviewer_response_packet.py
```

Emit the exact machine-readable response a first external reviewer should return after the handoff/dry-run:

```bash
python3 examples/agent_trust_reviewer_response_packet.py
```

Run the composed first-pilot review-path self-check when a reviewer wants one JSON verdict instead of manually comparing response/provenance fields:

```bash
python3 examples/agent_trust_first_pilot_review_check.py
```

Classify sanitized first-review feedback into the next smallest local product move without authorizing external action:

```bash
python3 examples/agent_trust_first_review_feedback_classifier.py
```

See where a framework or tool runner would insert the pre-action gate before a risky mock call:

```bash
python3 examples/agent_trust_framework_gate.py
```

Read the agent integration recipe for the wrapper pattern, request shape, decision mapping, and stop conditions:

```bash
cat examples/agent_trust_agent_integration_recipe.md
```

Read the Codex context pack before delegating Agent Trust / agent-security work:

```bash
cat examples/agent_trust_codex_context_pack.md
```

## Shortest CLI flow

Generate or inspect the request shape:

```bash
python3 examples/agent_trust_request.py
```

Run the sample request through the local CLI:

```bash
python3 -m agent_trust.cli examples/input.json
```

Verify the sample output against the checked-in golden bundle:

```bash
python3 examples/agent_trust_verify.py
```

Inspect the agent landing packet, full manifest, and external review packet:

```bash
cat examples/agent_trust_agent_landing.json
cat examples/agent_trust_manifest.json
cat examples/agent_trust_review_packet.json
```

Check all checked-in example artifacts for local consistency, including the manifest:

```bash
python3 examples/agent_trust_doctor.py
python3 examples/agent_trust_daily_review.py
python3 examples/agent_trust_adoption_readiness.py
```

Or call the builder directly in-process from Python:

```bash
python3 examples/agent_trust_import.py
```

Optional contract discovery:

```bash
python3 -m agent_trust.cli --print-contract
```

Inspect the checked-in schema-like artifact:

```bash
cat examples/agent_trust_schema.json
```

Inspect the strict request/output JSON Schemas:

```bash
cat schemas/agent_trust_request.schema.json
cat schemas/agent_trust_bundle.schema.json
cat schemas/agent_trust_manifest.schema.json
```

## Shortest local HTTP flow

Start the Ouroboros app/server normally, then run:

```bash
python3 examples/agent_trust_http_client.py
```

The client posts `examples/input.json` to the local endpoint:

```text
http://127.0.0.1:8765/api/agent-trust/bundle
```

Optional local self-use check against the dedicated MVP endpoint with strict timeouts and audit-correlation checks:

```bash
python3 examples/agent_trust_live_self_use.py --base-url http://127.0.0.1:8766
```

Pass the loopback service root with an explicit port only; the runner appends `/api/agent-trust/bundle` exactly once, strips one trailing slash, and rejects any supplied path, query, fragment, or credentials. It loads the checked-in canonical request from `examples/input.json`, sends a malformed negative case that must return `invalid_agent_trust_input`, and correlates request IDs plus bundle IDs against safe audit-summary fields only. Audit logs default to `/home/ouroboros/Ouroboros/data/logs/agent_trust_mvp_live.jsonl` unless `OUROBOROS_AGENT_TRUST_MVP_LOG_PATH` or `--audit-log-path` overrides it.


## Rain external comms preflight

Check whether Rain has the secret-safe aliases needed for durable Gmail API and X API use before falling back to browser login:

```bash
python3 examples/rain_external_comms_preflight.py
```

The command performs no network calls, no browser actions, no login, no email send/read, and no X posting. It prints only alias presence and exact blockers; secret values are always withheld.

## Rain X/Twitter bootstrap

Prepare Rain's first public X/Twitter posts and reply discipline without creating an account, logging in, bypassing anti-abuse checks, posting, or touching secrets:

```bash
python3 examples/rain_x_twitter_bootstrap.py
```

Use this only after a legitimate official/manual/mobile X account bootstrap or an already-live browser session.

## Rain X signal drafts

Convert a saved read-only X threat-watch JSON result into non-posting draft posts with hashtags:

```bash
python3 examples/rain_x_signal_drafts.py --sample
python3 examples/rain_x_signal_drafts.py --input /path/to/rain_x_threat_watch.json
```

The command performs no network calls and never posts; it treats X content as untrusted evidence.

Review those draft posts before any live X action:

```bash
python3 examples/rain_x_draft_review_gate.py --sample
python3 examples/rain_x_signal_drafts.py --sample > /tmp/rain_x_drafts.json
python3 examples/rain_x_draft_review_gate.py --input /tmp/rain_x_drafts.json
```

The review gate is still local-only and never posts; it marks candidate posts and holds unsafe or instruction-like text.

## Safety boundary

The Agent Trust Bundle builder is local and deterministic: no wallet access, no real payments, no external tool execution, and no network calls from the bundle builder itself. The HTTP example contacts only the local `127.0.0.1` endpoint.

## Base Sepolia preflight

Before any live x402 testnet attempt, run the local inert readiness gate:

```bash
python3 examples/agent_trust_base_sepolia_preflight.py
```

It reports only secret-safe env presence/shape metadata and performs no network, wallet, signing, transaction, mainnet, or real-money behavior.

Make the future live-client boundary explicit without executing it:

```bash
python3 examples/agent_trust_base_sepolia_live_boundary.py
```

The boundary output is dry-run-only: proposed command shape, env contract, sanitized logging rules, and stop conditions, with `live_call_performed=false`.


## Daily security-and-progress checkpoint

`agent_trust_daily_review.py` is the smallest machine-readable daily checkpoint for Agent Trust: it verifies release sync, clean git state, the examples doctor, the Base Sepolia dry-run boundary, and adoption readiness without network, wallet access, signing, transactions, outreach, or real money. The reviewer evidence transcript packages those local results into a short JSON attachment for inspection before any external contact.

## Agent-security evidence example

Run:

```bash
python3 examples/agent_trust_agent_security_evidence.py
python3 examples/agent_trust_workflow_pressure_gate.py
python3 examples/agent_trust_cross_surface_intake.py
python3 examples/agent_trust_intake_review_packet.py --synthetic
python3 examples/agent_trust_intake_contract_check.py
python3 examples/agent_trust_benchmark_intake_evidence.py --synthetic
```

This emits a deterministic local packet for sanitized memory/context,
authorization-control, orchestration, and task-warrant risk evidence. It performs
no network calls, wallet access, external scanner/tool execution, signing,
payment, real-money activity, or outreach.

## First integration ticket

```bash
python3 examples/agent_trust_integration_ticket.py
```

Emits a local-review-only ticket with scope, proof commands, a pre-action handoff contract, acceptance criteria, reviewer questions, and stop conditions for a first experimental Agent Trust integration. It performs no network calls, wallet access, execution, signing, payments, real-money activity, or outreach.

- `agent_trust_intake_contract_check.py` — local ISC intake contract check keeping cross-surface intake and intake review packet surfaces, decisions, and workflow-pressure signals aligned without network, wallet, signing, payment, outreach, MCP calls, external tools, or untrusted execution.
- `agent_trust_benchmark_intake_evidence.py` — local ISC benchmark-intake evidence packet for snippets or synthetic cases before untrusted benchmark repo/task inspection; it refuses tests, validators, tools, MCP calls, installs, network, wallet, signing, payment, outreach, and untrusted execution.

- Pre-exposure probe: `python3 examples/agent_trust_exposure_probe.py` checks the live Agent Trust discovery endpoint before any controlled external exposure.

- `python3 examples/agent_trust_exposure_decision_gate.py` — local no-network/no-port-open go/no-go gate for a controlled 8766 MVP edge plan; refuses 8765/control-console exposure.
- `python3 examples/agent_trust_exposure_edge_prep.py` — emit the local inert 8766-only edge-prep packet after the decision gate passes; no ports are opened and no network calls are made.
- `agent_trust_loopback_readiness.py` — local gate + loopback MVP + edge-path readiness proof for controlled 8766 prep; opens no external ports and performs no wallet/signing/payment/real-money behavior.

- `rain_x_monitor_playwright.py` — read-only X.com login-check/search monitor using a persistent Playwright browser profile; intended for the OpenClaw-style x.com fallback after one-time login/session setup.


Scanner-pass fallacy / marketplace scanner bypass proof:

```bash
python3 examples/agent_trust_layered_skill_scanning.py --scanner-pass-fallacy-demo --expect-decision deny --compact --fail-on-fail
```

This proves that clean scanner labels are evidence, not authorization, when independent authority/provenance/semantic signals remain dangerous.

