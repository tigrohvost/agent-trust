# Agent Trust Coverage Matrix

Agent Trust is intentionally small. This matrix tells an installing agent or reviewer what the skill covers, what it refuses to cover, and which local proof command checks the boundary.

## Covered surfaces

| Surface | What Agent Trust checks | Default move | Proof / entrypoint |
|---|---|---|---|
| Secret exposure | Detects requests that include or normalize tokens, private keys, seed phrases, passwords, payment credentials, or similarly sensitive values. | Deny or require human/agent review; never paste real secrets into examples, issues, prompts, or logs. | `agent-trust --input examples/input.json` |
| Tool / MCP / plugin risk | Classifies risky capabilities such as shell execution, environment reads, filesystem writes, network egress, browser automation, posting, repo writes, and privileged integrations. | Proceed only for low-risk local checks; review/deny broad authority. | `agent-trust --print-contract` |
| Wallet / signing / payment boundary | Flags wallet, signing, transaction, x402/payment, real-money, and settlement-like behavior. | Review/deny by default unless a separate explicit warrant exists. | `agent-trust --input examples/input.json` |
| External skill installability | Gives agents a metadata-first path: read `SKILL.md`, `index.json`, plugin metadata, schemas, and CLI contract before source diving. | Install/use only after local proof commands pass. | `agent-trust-skill manifest --compact` |
| Improvement selection | Provides a small local loop for choosing one safe, high-value improvement without turning the repo into a large library. | Pick one bounded improvement, test it, then stop or re-rank. | `python3 examples/agent_trust_idea_selector.py examples/ideas.json` |

## Intentionally out of scope

| Not covered | Why |
|---|---|
| Malware execution or sandbox detonation | Agent Trust is a local pre-action review skill, not a malware lab. |
| Vulnerability scanning of third-party targets | Avoids authorization ambiguity and network side effects. |
| Live wallet signing, payments, or mainnet actions | These require explicit external accountability, limits, and stop paths outside this skill. |
| Secret management or vault replacement | Agent Trust can detect secret-handling risk, but it is not a credential store. |
| Broad cybersecurity curriculum | Large skill libraries are useful, but Agent Trust stays compact: trust boundaries, not every security domain. |

## Comparison posture

Large cybersecurity skill libraries win by breadth. Agent Trust should win by **installability, clear boundaries, local proof commands, and agent-readable metadata** — not by becoming huge. If a new idea does not improve those properties, it should stay out of the core skill.
