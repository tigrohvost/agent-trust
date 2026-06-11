# Agent Trust first run

A two-minute path from checkout to a deterministic **Agent Trust Bundle** verdict.

Use this when you want to see the contract before reading the full MVP packet or choosing an integration path.

## Why this exists

Agent Trust is a local **pre-action trust gate** for AI agents before they take side-effectful or authority-bearing actions:

- calling tools or MCP servers;
- running browser actions;
- installing external skills/plugins;
- touching wallets, x402, payments, or paid endpoints;
- publishing, outreach, or other external side effects.

The pain is simple: an agent often reaches the moment of action before it has a compact, inspectable receipt explaining **why this action should proceed, require review, or be denied**.

Agent Trust gives that moment a small deterministic JSON boundary:

```text
proposed agent action -> local trust bundle -> proceed / review / deny receipt
```

It is local-first and intentionally narrow: no vendor lock-in, no cloud dependency, no secret collection, no wallet access, no real-money action, and no external tool execution in the proof path.

## Fastest proof path

From the repository root:

```bash
bash scripts/agent_trust_first_run.sh
```

Expected outcome: the command exits `0` and prints final JSON from `examples/agent_trust_doctor.py` with a successful `validation_summary`. That proves the canonical request, CLI bundle output, golden verifier, schemas, manifest, and example packet are mutually consistent.

If you only inspect one follow-up artifact, inspect the checked-in golden output:

```bash
python3 examples/agent_trust_verify.py
```

Expected result: JSON with `ok: true` and `matches_golden: true`.

## 0. Boundary

This first run is local only:

- no hosted service;
- no wallet access;
- no real payments;
- no external tool execution;
- no network calls from the bundle builder.

The optional HTTP step calls only your local Ouroboros server at `127.0.0.1`.

## 1. One-command checkout smoke test

```bash
bash scripts/agent_trust_first_run.sh
```

This runs the canonical request inspection, local CLI contract, golden-output verifier, and full examples-packet doctor from one repo-root command. The final JSON includes `validation_summary`, a compact machine-readable map of the packet name, first-run command, contract discovery command, canonical request, golden output, manifest, schema directory, success signals, and local-integration readiness.

## 2. Inspect the canonical request

```bash
python3 examples/agent_trust_request.py
```

This prints the current versioned request shape, including `contract_version`.

## 3. Run the local CLI

```bash
python3 -m agent_trust.cli examples/input.json
```

Expected result: deterministic JSON with a top-level trust verdict and supporting x402 policy/tool-risk signals.

## 4. Compare against the checked-in golden output

```bash
python3 examples/agent_trust_verify.py
```

Expected result: JSON with `ok: true`, `matches_golden: true`, the current contract version, verdict, bundle ids, and the local safety boundary. If it exits `0`, the local CLI contract matches the documented sample output. The repo-root shell wrapper runs this verifier as an internal step before the full doctor.

## 5. Optional: check example consistency for CI/agents

```bash
python3 examples/agent_trust_doctor.py
```

Use this if you want one JSON result showing whether the checked-in request, golden output, schemas, manifest, manifest schema, request wrapper, and verifier are mutually consistent. This is also the final JSON emitted by `scripts/agent_trust_first_run.sh`, including the same `validation_summary` for agents that want to choose the next integration path without reading prose first.

## 6. Optional: check the installable skill boundary

```bash
python3 -m agent_trust.skill manifest --compact
```

Use this when the next integration step is installing or approving an external agent skill, plugin, MCP server, or repo helper. The command is dependency-free and local-only: it emits the Agent Trust Skill manifest (supported actions, decision values, hard boundaries) so an agent can confirm the review-only contract before any secrets, network, execution, wallets, payments, or outreach are authorized.

## 7. Optional: consumer-style integration decision

```bash
python3 examples/agent_trust_consumer_decision.py
```

This reads the manifest, external review packet, and doctor output and returns a machine-readable `integrate_experimentally` or `abstain` decision for another local agent. It is still local-only and does not publish, call wallets, contact paid endpoints, or make real-money decisions.

## 8. Optional: inspect the agent-discoverable manifest

```bash
cat examples/agent_trust_manifest.json
```

Use this path if another agent needs a machine-readable map of the local artifacts, entrypoints, docs, schemas, and safety boundary before choosing how to integrate.

## 9. Optional: direct Python import

```bash
python3 examples/agent_trust_import.py
```

Use this path if your agent is Python-native and you do not want a subprocess or local HTTP call.

## 10. What to read next

| If you now want to... | Go here |
|---|---|
| Understand the product shape | [MVP packet](AGENT_TRUST_MVP.md) |
| Choose import vs CLI vs HTTP vs schemas | [Integration checklist](AGENT_TRUST_INTEGRATION.md) |
| Inspect every example artifact | [Examples quickstart](examples/README.md) |
| Validate whether anyone cares | [Validation packet](AGENT_TRUST_VALIDATION.md) |
| Collect concrete feedback | [Feedback template](AGENT_TRUST_FEEDBACK.md) |

## Success signal

A useful first run is not applause. It is one of these:

- another agent/developer can reproduce the golden output;
- they can name one missing evidence field;
- they can say which integration path they would actually use;
- they can give a concrete paid/tool action where the bundle would reduce risk.
