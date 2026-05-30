# Security Policy

Agent Trust is a local-first trust-boundary skill for agents. It is designed to inspect
requests, tool/MCP risk signals, and x402-style policy receipts without performing the
risky action itself.

## Supported scope

Security reports are especially welcome for:

- secret exposure risks in examples, logs, schemas, metadata, or CLI output;
- paths where network, wallet, signing, payment, outreach, or untrusted-code execution
  could happen despite the documented local-only boundary;
- unsafe defaults in request handling, tool-risk classification, or policy receipts;
- misleading compatibility or installability claims;
- schema/contract mismatches that could cause another agent to trust the wrong signal.

## Hard safety boundary

Agent Trust must not require or reveal real tokens, API keys, private keys, seed phrases,
payment credentials, wallet secrets, recovery codes, or production customer data.

When reporting a vulnerability, do **not** paste real secrets into issues, pull requests,
examples, or logs. Use redacted placeholders such as `REDACTED_TOKEN` and include the
minimal reproduction steps needed to understand the issue.

## Reporting

Preferred public-safe report format:

1. affected command, file, schema, or metadata artifact;
2. expected safe behavior;
3. observed unsafe behavior;
4. minimal reproduction using redacted dummy data;
5. suggested fix, if known.

If the report cannot be shared publicly without exposing a secret or enabling abuse, open
a minimal issue saying that a private security report is needed and avoid including the
sensitive details.

## Non-goals

Agent Trust is not a scanner that executes third-party code, not a wallet, not a payment
agent, not a posting/outreach agent, and not a compliance certification. It provides local
review evidence and pre-action gates for other agents to inspect before they decide.
