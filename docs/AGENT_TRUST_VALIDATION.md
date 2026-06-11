# Agent Trust validation packet

A compact, non-publishing packet for showing the local **Agent Trust Bundle** MVP to early agent-framework, MCP/tooling, and x402 developers.

This file is a preparation artifact only. It does not publish anything, contact any external service, create accounts, spend money, or request wallet credentials.

## Target early adopters

- Developers building autonomous agents that may call paid APIs or x402 resources.
- MCP/tool-server authors who want a machine-readable pre-action trust check.
- Agent-framework maintainers experimenting with tool risk, local policy, and audit receipts.
- Security-minded agent builders who prefer local/no-wallet/no-execution prototypes before hosted services.

## One-line pitch

Agent Trust Bundle is a local, deterministic pre-action JSON report that helps an agent decide whether a contemplated paid-resource or tool/MCP action is safe enough to proceed, review, or deny.

## 60-second demo path

From the repository root:

```bash
python3 -m agent_trust.cli --print-contract
python3 -m agent_trust.cli --input examples/input.json
```

Then compare the output shape with:

```bash
diff -u examples/output.json <(python3 -m agent_trust.cli --input examples/input.json)
```

For Python integration without a subprocess:

```bash
python3 examples/agent_trust_import.py
```

## Validation ask

For structured responses, use the [Agent Trust feedback template](AGENT_TRUST_FEEDBACK.md).


Ask one concrete question:

> Would this pre-action trust bundle give your agent enough structured evidence to decide whether to call a paid API or tool server? If not, what exact field, proof, or integration shape is missing?

Useful answers name:

- the contemplated paid API, x402 resource, MCP server, or tool action;
- the integration path they would actually use: import, CLI, local HTTP, or schemas;
- the minimum fields required before automation;
- which `verdict`, `reasons`, or `controls` they would trust;
- what would make the bundle worth calling before every paid/tool action.

## Draft outreach messages

Do not send these without explicit human confirmation.

### x.com short post

Building a local Agent Trust Bundle: deterministic JSON for agents deciding whether to pay for an x402 resource or use a tool/MCP endpoint. No wallet, no network, no execution — just pre-action policy + risk signals. Looking for agent builders to tell me what field is missing.

### GitHub issue/comment style note

I am testing a small local Agent Trust Bundle for agent runtimes: a deterministic JSON pre-action report combining x402 policy quote signals and tool/MCP risk attestation. It has CLI, local HTTP, direct Python import, schemas, and golden examples. I am not asking for integration yet — only whether the contract has the fields an agent would need before calling a paid API or tool server.

### Discord/Telegram community note

Question for people building autonomous agents or MCP tools: would you use a local JSON trust bundle before an agent pays for an API or calls an external tool? Current MVP is no-network/no-wallet/no-execution and returns `verdict`, `reasons`, `controls`, x402 policy quote, and tool-risk signals. I need feedback on missing fields, not hype.

### Direct DM/email

Hi — I am validating a narrow Agent Trust Bundle MVP for agents that may call paid APIs, x402 resources, or external tools/MCP servers. It is local-only and deterministic, with CLI/HTTP/import/schema examples. Could you glance at the contract and tell me what evidence your agent would need before automating a proceed/review/deny decision?

## Safety boundary and non-goals

Current boundary:

- no hosted service;
- no network calls from the bundle builder;
- no wallet access;
- no private keys, seed phrases, or payment credentials;
- no execution of supplied tool/MCP descriptors;
- no real money;
- no public posting from this packet.

Non-goals for validation:

- proving market demand statistically;
- integrating a real x402 facilitator;
- scanning remote MCP servers live;
- building reputation or compliance infrastructure;
- asking anyone for credentials or funds.

## Stop conditions requiring explicit human confirmation

Stop and ask before:

- publishing to x.com, Telegram, Discord, Reddit, GitHub, or any public channel;
- creating or using an external account;
- sending DMs/emails to real people;
- offering a hosted endpoint;
- touching wallet/payment credentials or real money;
- changing repository visibility/settings/collaborators;
- making legal/compliance claims beyond the local technical boundary.

## Success signals

Continue the Agent Trust line if at least one of these appears:

- a developer names a real paid/tool action they would run through the bundle;
- someone asks for a specific missing field or proof type;
- someone prefers a concrete integration path and explains why;
- a maintainer asks for an example in their framework shape;
- feedback says the proceed/review/deny semantics are understandable enough to test.

Pause or pivot if feedback is only vague approval, likes, or curiosity without a contemplated action.
