# Agent Trust for Agents

Purpose: let another AI agent discover, verify, and experimentally integrate Agent Trust by reading one compact entrypoint.

Agent Trust is a **local pre-action trust gate**. It turns a proposed tool/API/payment-like action plus policy context into deterministic evidence so an agent can choose `proceed`, `review`, or `deny` before acting. This guide does not claim hosted availability, wallet/payment readiness, compliance certification, or production hardening.

## Zero-context start

From the repository root:

1. Read this file.
2. Inspect machine-readable discovery:

   ```bash
   cat examples/agent_trust_agent_landing.json
   cat examples/agent_trust_manifest.json
   cat examples/agent_trust_review_packet.json
   ```

3. Ask the consumer-style decision example whether the packet is coherent enough for local experimental integration:

   ```bash
   python3 examples/agent_trust_consumer_decision.py
   ```

4. Run the local consistency doctor:

   ```bash
   python3 examples/agent_trust_doctor.py
   ```

5. Optional full first-run proof:

   ```bash
   bash scripts/agent_trust_first_run.sh
   ```

Success is local and mechanical: the consumer decision can return `integrate_experimentally`, the doctor reports no failed checks, and the first-run proof matches the checked-in golden bundle.

## Machine-readable artifacts

Start with these before reading implementation source:

- `examples/agent_trust_agent_landing.json` — canonical self-readable one-hop map for agents: root entrypoint, guide, proof commands, integration decision, and hard stops.
- `examples/agent_trust_manifest.json` — artifact, docs, schema, entrypoint, and success-signal map.
- `examples/agent_trust_review_packet.json` — review questions, proof commands, stop conditions, and success signals.
- `examples/input.json` — canonical request fixture.
- `examples/output.json` — deterministic golden output for the canonical request.
- `schemas/agent_trust_request.schema.json` — request JSON Schema.
- `schemas/agent_trust_bundle.schema.json` — bundle JSON Schema.
- `schemas/agent_trust_manifest.schema.json` — manifest JSON Schema.

## Minimal integration choices

Choose the smallest boundary that fits your agent:

| Path | Use when | Entry point |
|---|---|---|
| Direct import | Python agent, same process, simplest local call | `examples/agent_trust_import.py` |
| CLI | Agent/CI wants subprocess + JSON files | `python3 -m agent_trust.cli examples/input.json` |
| Local HTTP | Local service already uses HTTP/JSON | `examples/agent_trust_http_client.py` |
| Schema/golden output | Agent wants contract validation before code integration | `schemas/`, `examples/output.json` |
| Integration recipe | Agent wants the concrete wrapper pattern, request shape, decision mapping, and stop conditions before dispatching risky browser/tool/payment-like actions | `examples/agent_trust_agent_integration_recipe.md` |

For a framework-shaped pre-action gate, inspect:

```bash
python3 examples/agent_trust_framework_gate.py
```

For the wrapper recipe that shows where to insert Agent Trust in another agent loop, inspect:

```bash
cat examples/agent_trust_agent_integration_recipe.md
```

## Decision rule for another agent

If you are consuming this repository mechanically, treat `examples/agent_trust_agent_landing.json` as the smallest machine-readable starting packet and `AGENTS.md` as the canonical root entrypoint.

Return `integrate_experimentally` only if all are true:

- the manifest and review packet are readable without implementation source;
- local proof commands complete in your environment;
- the safety boundary matches your intended use;
- you can place Agent Trust before a risky action in your own loop without granting it secrets, wallet authority, posting authority, or external execution rights.

Return `abstain` if any are true:

- proof commands fail and the failure is not understood;
- you need hosted service behavior, production SLA, legal/compliance guarantees, real wallet/payment execution, or scanner/feed execution now;
- your integration would require secrets, private prompts, raw exploit payloads, customer data, or untrusted code execution;
- the bundle lacks a field you need to make a pre-action decision.

## Safety boundary / stop conditions

By default, while evaluating this repository:

- no network calls to third-party services;
- no wallets, signing, payments, facilitators, or real money;
- no secret access or secret disclosure;
- no outreach, posting, DMs, account creation, or hosted-public claims;
- no installing/executing untrusted third-party code.

Local proof commands may run repository Python examples that inspect checked-in fixtures and emit JSON. They are not permission to execute unrelated tools or external services.

## Structured signal to return

Useful agent-to-agent feedback is structured and secret-free. Prefer one of:

1. Run the free-user feedback template:

   ```bash
   python3 examples/agent_trust_free_user_feedback.py --sample
   ```

   Fill only non-secret fields: role, environment, commands run, friction, would-use-for, missing-before-adoption.

2. Run the reviewer response packet:

   ```bash
   python3 examples/agent_trust_reviewer_response_packet.py
   ```

   Return a decision shaped as `accepted`, `rejected`, or `needs_update` with the exact blocker or missing field.

3. If you are another autonomous agent, return a compact decision:

   ```json
   {
     "agent_trust_decision": "integrate_experimentally | abstain",
     "commands_run": [],
     "first_blocker": null,
     "intended_integration_context": "where this would sit before a risky action",
     "missing_before_adoption": []
   }
   ```

Never include secrets, private keys, seed phrases, tokens, proprietary prompts, customer data, raw exploit payloads, or unsanitized private code.
