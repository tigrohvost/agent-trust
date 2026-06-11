# Agent Trust Bundle MVP Packet

## Contract schemas

Machine-readable JSON Schema artifacts are checked in under `schemas/`:

- `agent_trust_request.schema.json` for the request shape accepted by CLI and local HTTP.
- `agent_trust_bundle.schema.json` for the deterministic trust-bundle output.

They let another agent or integrator validate the example input/output without reading this prose, while preserving the local safety boundary: no network, no wallet, no execution, no real money.

## Who this is for

Agent developers and integrators who are experimenting with autonomous agents that may call paid APIs, use x402-style payment flows, or connect to external tool/MCP servers.

## Value proposition

Before an agent pays for a resource or uses a tool, produce one deterministic machine-readable trust bundle answering: **can I pay/use this safely enough, and why?**

## Why this is agent-native

Human dashboards are too slow for autonomous pre-action decisions. This packet is designed for agents to read directly: compact JSON-like inputs, deterministic verdicts, explicit reasons, and audit-friendly controls.

## Current safety boundary

This is a local sandbox MVP packet, not a live paid service.

- Local only
- No network calls
- No wallet access
- No execution of supplied tools
- No real money
- No private keys, seed phrases, or payment credentials

## Minimal input contract

Conceptually, an integrator supplies four things to the local trust-bundle builder:

```python
policy = {
    "agent_id": "demo-agent",
    "settlement": "mock-local-no-money-policy",
    "allowed_resources": ["https://api.example.test/report"],
    "per_request_cap": "0.10",
    "per_agent_budget_cap": "1.00",
}

ledger = [
    {"agent_id": "demo-agent", "amount": "0.25", "payment_id": "paid-001"}
]

resource = "https://api.example.test/report"

tool_descriptor = {
    "name": "example-report-api",
    "kind": "mcp_server",
    "transport": "https",
    "auth": "env:EXAMPLE_API_KEY",
    "read_only": True,
}
```

The local surface combines:

1. x402 policy quote signals for the requested resource and mock budget.
2. Tool/MCP risk attestation signals for the descriptor.
3. A single pre-action verdict with reasons and controls.

## Minimal output contract

Example shape, abbreviated:

```json
{
  "bundle_id": "agenttrust-...",
  "contract_version": "agent-trust-bundle-v1",
  "supported_contract_versions": ["agent-trust-bundle-v1"],
  "verdict": "review",
  "reasons": ["tool_risk_medium"],
  "controls": [
    "network_calls_false",
    "wallet_access_false",
    "execution_false",
    "x402_settlement:mock-local-no-money-policy"
  ],
  "settlement": "mock-local-no-money-policy",
  "policy_quote": {
    "agent_id": "demo-agent",
    "resource": "https://api.example.test/report",
    "resource_allowed": true,
    "per_request_cap": "0.10",
    "per_agent_budget_cap": "1.00",
    "remaining_budget": "0.75"
  },
  "tool_risk": {
    "attestation_version": "tool-risk-v1",
    "overall_risk": "MEDIUM",
    "finding_count": 1,
    "network_calls": false,
    "execution": false
  }
}
```

The important contract is not the exact example values; it is the invariant that a consuming agent gets a deterministic `verdict`, explicit `reasons`, and visible `controls` before acting.

## Three-step demo flow

1. **Describe the contemplated action**: target resource, expected mock payment policy, current local ledger, and tool/MCP descriptor.
2. **Build the trust bundle locally** with the existing no-network/no-wallet/no-execution trust-bundle surface.
3. **Let the caller decide**: `allow` can proceed inside the caller's own sandbox, `review` asks for human/agent policy review, and `deny` blocks because the bundle found a hard reason.

## Discover the CLI contract

External integrators can ask the CLI to describe its own stable machine-readable contract without providing an input file:

```bash
python3 -m agent_trust.cli --print-contract
```

The contract JSON includes the safety boundary, current/supported Agent Trust Bundle contract versions, required/optional input fields, expected output fields, error envelope shape, exit-code semantics, and example commands. This lets another agent inspect the interface before deciding whether to call it.

For consumers that prefer checked-in files over live discovery, `schemas/agent_trust_schema.json` provides a concise schema-like overview, while `schemas/agent_trust_request.schema.json` and `schemas/agent_trust_bundle.schema.json` provide draft-2020-12 JSON Schemas for the request and emitted trust bundle.

## Build a versioned request JSON

External consumers do not have to hand-copy the demo input. A tiny standard-library request wrapper prints the canonical local request shape with an explicit supported bundle contract version:

```bash
python3 examples/agent_trust_request.py > /tmp/agent_trust_request.json
python3 -m agent_trust.cli --input /tmp/agent_trust_request.json
```

The wrapper is intentionally not a full SDK and adds no production helper functions. It only prints JSON locally; it performs no network calls, wallet access, tool execution, or real-money action. The checked-in `examples/input.json` is generated from the same canonical shape and includes `"contract_version": "agent-trust-bundle-v1"`.

## Direct Python import example

For Python agents that do not want a CLI subprocess or local HTTP hop, the repository includes a tiny in-process example:

```bash
python3 examples/agent_trust_import.py
```

It imports `agent_trust.bundle.build_agent_trust_bundle`, supplies the same kind of local policy/resource/tool descriptor fields, and prints deterministic pretty JSON. This is still not an SDK and preserves the same boundary: no network calls, no wallet access, no supplied-tool execution, and no real-money action.

## Run the local demo

Use the reusable local CLI contract from the repository root:

```bash
python3 -m agent_trust.cli --input examples/input.json
```

The repository also includes a checked-in expected output for this exact input:

```bash
python3 -m agent_trust.cli --input examples/input.json > /tmp/agent_trust_output.json
diff -u examples/output.json /tmp/agent_trust_output.json
```

This gives external integrators a machine-readable golden example of the deterministic bundle shape before they wire the contract into their own agent. The regression tests compare JSON objects, not formatting, so the example protects the interface without making whitespace part of the contract.

The CLI can also read the same JSON contract from stdin. Consumers may request the explicit supported bundle schema version with `--contract-version agent-trust-bundle-v1`; unsupported versions return a JSON error envelope with `unsupported_agent_trust_contract_version` and the supported version list:

```bash
cat examples/input.json | python3 -m agent_trust.cli --input -
```

The command only reads local JSON and calls the local trust-bundle builder. It does not call the network, access wallets, execute tools, or use real payment credentials. Successful output is deterministic JSON containing `bundle_id`, `verdict`, `reasons`, `controls`, `policy_quote`, and `tool_risk`; ordinary invalid inputs return a JSON error envelope instead of a traceback.


## Early validation ask

I want early adopters to answer one practical question:

> Would this pre-action bundle be enough for your agent to decide whether to call a paid API or tool server? If not, what exact field, proof, or integration shape is missing?

Useful signals:

- A concrete tool/MCP/x402 action you would run through this packet.
- The minimum JSON fields your agent would require.
- Whether you would prefer this as a library call, CLI, local HTTP endpoint, or hosted API later.
- Which verdict/reason semantics would make the result trustworthy enough to automate.

## Non-goals for this MVP

- No hosted service yet.
- No real x402 facilitator integration yet.
- No wallet support yet.
- No real-money payments.
- No remote scanning or execution of tool servers.
- No broad compliance framework.
- No reputation oracle beyond local deterministic signals.

This MVP is intentionally narrow: prove whether agents and agent builders want a machine-readable pre-action trust bundle before adding infrastructure.
