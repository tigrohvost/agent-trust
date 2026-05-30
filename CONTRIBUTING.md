# Contributing to Agent Trust

Thank you for considering a contribution to Agent Trust.

Agent Trust is a small local-first skill/package for inspecting agent actions before trust-sensitive behavior. Contributions are welcome when they preserve the core boundary: **local, inspectable, no secret exposure, no network/wallet/signing/payment/outreach action by default**.

## Safe contribution rules

Please do **not** include any real secrets or sensitive material in issues, pull requests, examples, tests, logs, screenshots, or pasted JSON:

- API tokens, GitHub PATs, OAuth tokens, cookies, session IDs
- private keys, wallet keys, seed phrases, recovery codes
- payment credentials or real transaction data
- private customer data, proprietary prompts, internal URLs, or access logs

Use placeholders such as `REDACTED_TOKEN`, `example_wallet_address`, or synthetic test data.

## What contributions fit

Good contributions usually improve one of these areas:

- clearer `SKILL.md` instructions for agent frameworks;
- safer request/bundle schemas;
- better local-only CLI behavior;
- tests that preserve deterministic output;
- documentation for installability and verification;
- metadata that helps agents discover the skill without granting extra authority;
- security-boundary clarifications.

Contributions should **not** silently add behavior that performs network calls, wallet access, signing, payments, browser automation, account actions, posting, private outreach, or execution of untrusted code. If you believe one of those capabilities belongs here, open a design discussion first and make the boundary explicit.

## Local verification before submitting

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest -q
python -m agent_trust.cli --print-contract
python -m agent_trust.cli --input examples/input.json
python -m agent_trust.skill manifest --compact
```

Expected result:

- tests pass;
- CLI commands emit JSON;
- no command requires secrets;
- no command performs network, wallet, signing, payment, outreach, or untrusted-code execution.

## Documentation changes

When changing public behavior, update all relevant surfaces together:

- `README.md`
- `SKILL.md`
- `index.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `schemas/` if request or output shape changes
- `examples/` if examples no longer match emitted output

Agent-facing docs should be short first, detailed later: intent, when to use, safe commands, hard stops, then advanced notes.

## Reporting security issues

Please read `SECURITY.md` before reporting security-sensitive issues. Do not paste live secrets or exploit material that would enable harm. Provide a minimal synthetic reproduction whenever possible.

## License

By contributing, you agree that your contribution is licensed under the repository license.
