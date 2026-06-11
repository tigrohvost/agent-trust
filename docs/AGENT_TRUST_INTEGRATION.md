# Agent Trust integration checklist

A compact choose-your-path guide for wiring the local **Agent Trust Bundle** into an agent prototype. Use this when you already understand the MVP and only need to choose the smallest integration surface.

## Safety boundary

Every path below keeps the same local MVP boundary:

- no network calls from the trust-bundle builder;
- no wallet access;
- no execution of supplied tool/MCP descriptors;
- no real payments or payment credentials;
- deterministic JSON output for the same input.


## Choose your path

| If you are... | Start with | Why | First command / file |
|---------------|------------|-----|----------------------|
| A Python agent running in the same process | **Direct Python import** | Smallest integration: no subprocess, no local HTTP hop. | `python3 examples/agent_trust_import.py` |
| A shell-based agent, CI job, or non-Python prototype | **Local CLI** | Stable JSON stdin/file interface with machine-readable errors and contract discovery. | `python3 -m agent_trust.cli --input examples/input.json` |
| An agent validating compatibility before integration | **Checked-in schemas/examples** | Validate request/output shape without reading source or starting the app. | `schemas/agent_trust_request.schema.json` and `examples/output.json` |

## Minimal decision flow

1. **Describe the contemplated action**: requested resource, local mock x402 policy, current ledger, and tool/MCP descriptor.
2. **Build a trust bundle** using exactly one integration path above.
3. **Read `verdict`, `reasons`, and `controls`** before the caller decides whether to proceed, review, or deny.
4. **Log the bundle or selected fields** in the caller's own audit trail; the bundle is designed to be machine-readable evidence, not a human dashboard.

## Path details

### 1. Direct Python import

Use this when your agent is Python and can import the repository code directly.

```bash
python3 examples/agent_trust_import.py
```

The example calls:

```python
from agent_trust.bundle import build_agent_trust_bundle
```

Best for: in-process prototypes, Python agent frameworks, and tests that should avoid shelling out.

### 2. Local CLI

Use this when you want a stable process boundary or your caller is not Python.

```bash
python3 -m agent_trust.cli --input examples/input.json
```

Discover the machine-readable CLI contract first:

```bash
python3 -m agent_trust.cli --print-contract
```

Best for: shell agents, CI checks, language-agnostic prototypes, and simple subprocess integrations.

Bundle endpoint:

```text
POST http://127.0.0.1:8765/api/agent-trust/bundle
```

Best for: local multi-language agents, browser-side demos, and service-oriented prototypes. Not a hosted public API.

### 4. Schemas and examples

Use these before wiring code, or inside your own compatibility tests:

- `examples/input.json` — canonical sample request.
- `examples/output.json` — deterministic golden output for the sample request.
- `schemas/agent_trust_schema.json` — compact schema-like overview.
- `schemas/agent_trust_request.schema.json` — draft-2020-12 request schema.
- `schemas/agent_trust_bundle.schema.json` — draft-2020-12 output schema.

Best for: another agent deciding whether it understands the contract, or a developer adding validation around the CLI/HTTP/import paths.

## When not to use this yet

Do not treat this MVP as:

- a real payment gateway;
- a wallet integration;
- a remote tool scanner;
- a hosted reputation oracle;
- legal/compliance approval.

It is a local pre-action trust bundle: useful before an agent pays for or uses something, but intentionally narrow until demand and missing fields are validated.

## Next useful feedback

If this checklist still leaves friction, the most useful feedback is concrete:

- Which path did you choose: import, CLI, HTTP, or schema-only?
- What exact field did your agent need but not receive?
- Which verdict/reason/control would you trust enough to automate?
- What would make this worth calling before a paid API or MCP/tool action?
