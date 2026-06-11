# Agent Trust feedback template

Use this compact template when asking an early agent-framework, MCP/tooling, or x402 developer to review the **Agent Trust Bundle** contract.

This is a feedback artifact only. Do not ask reviewers to share secrets, wallet keys, API tokens, production credentials, private customer data, or paid endpoints they are not allowed to discuss.

## Reviewer context

```text
Reviewer role:
Project / framework / agent type:
Primary integration path considered: direct Python import / local CLI / local HTTP / schemas only / other
Contemplated action type: paid API / x402 resource / MCP server / local tool / remote tool / other
Would this run before every action, only high-risk actions, or only manual review?
```

## Core validation question

```text
Would the current Agent Trust Bundle output give your agent enough structured evidence to choose proceed / review / deny before the contemplated action?

Answer: yes / no / partially
Why:
```

## Missing evidence fields

Name exact fields, proofs, or signals that are missing.

```text
1. Missing field/proof/signal:
   Why it matters:
   Required for: proceed / review / deny / audit / policy config

2. Missing field/proof/signal:
   Why it matters:
   Required for: proceed / review / deny / audit / policy config
```

## Trust in existing bundle sections

Score each section from 0 to 3:

- 0 = not useful
- 1 = useful only for human review
- 2 = useful for guarded automation with additional checks
- 3 = enough for this action class

```text
Top-level verdict and reasons: 0 / 1 / 2 / 3
x402 policy quote signals: 0 / 1 / 2 / 3
Tool/MCP risk attestation: 0 / 1 / 2 / 3
Controls / stop conditions: 0 / 1 / 2 / 3
Schema/example artifacts: 0 / 1 / 2 / 3
CLI/local HTTP/import integration paths: 0 / 1 / 2 / 3
```

## Integration friction

```text
Smallest path you would actually test: direct Python import / local CLI / local HTTP / schema/golden file comparison / other
What makes that path attractive:
What blocks a first test:
What would make it worth calling in a real agent loop:
```

## Automation threshold

```text
Minimum requirement before automatic proceed:
Minimum requirement before automatic deny:
When should the agent force human review:
Audit log or receipt fields needed later:
```

## Pricing / willingness-to-call signal

This is not a request for payment. It is a demand signal check.

```text
Would you spend latency/cost to call this before risky actions? yes / no / maybe
Would you pay for a hosted or maintained version if it saved integration time? yes / no / maybe
If yes/maybe, what would it need beyond the local MVP:
```

## Safety notes

Do not include:

- API keys, wallet keys, seed phrases, tokens, or private credentials;
- unreleased security vulnerabilities;
- customer/private data;
- instructions to bypass a target's safety, payment, or auth controls;
- requests for real-money action.

If a useful example requires sensitive details, replace them with a synthetic descriptor and name only the missing trust signal.

## Decision rubric for Rain

Continue this line if feedback contains at least one concrete contemplated action plus one missing field/proof/integration request.

Prioritize next iteration by this order:

1. Missing field that blocks multiple reviewers from testing.
2. Integration friction that prevents the first local run.
3. Schema/contract ambiguity.
4. Better examples for a named framework/tooling shape.
5. Hosted service or real-money requests — pause and ask before acting.

Do not treat likes, vague encouragement, or generic interest as validation.
