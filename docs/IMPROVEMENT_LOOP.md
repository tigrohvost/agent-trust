# Agent Trust improvement loop

Agent Trust should improve by evidence, not by vague roadmap expansion. When an agent or maintainer asks "what should be applied next?", use this small loop.

## Loop

1. **Collect candidate ideas** from concrete evidence: install failures, unclear skill instructions, repeated reviewer questions, security boundary gaps, schema mismatches, or external skill best practices.
2. **Score each idea** using the same dimensions:
   - `impact`: how much it improves installability, safety, or adoption;
   - `evidence`: how concrete the source signal is;
   - `risk`: how likely it is to widen authority, confuse users, or break compatibility;
   - `effort`: how large the change is.
3. **Select one idea** with the best risk-adjusted score.
4. **Apply the smallest complete version**: docs, schema, CLI, tests, or metadata — whichever makes the improvement real.
5. **Verify locally** before publishing:

```bash
python3 -m pytest -q
python3 -m agent_trust.cli --print-contract
python3 -m agent_trust.skill manifest --compact
python3 examples/agent_trust_idea_selector.py --ideas examples/ideas.json
```

## Current candidate ideas

| Idea | Why it exists | Default decision |
| --- | --- | --- |
| Machine-readable improvement selector | The skill should show agents how to prioritize evidence-backed improvements instead of accumulating prose. | Applied first because it is local-only, low-risk, and reusable. |
| More framework-specific install probes | Codex, Claude, OpenClaw, and Hermes-style hosts differ in discovery paths. | Useful next, but should be added only when backed by concrete host evidence. |
| More detailed threat taxonomy | Agent Trust can become stronger at classifying tool/MCP/repo risks. | Useful, but higher complexity; apply in narrow slices. |
| Hosted demo or remote endpoint | Could improve adoption. | Not now: crosses network/exposure boundaries and needs a separate decision. |

## Hard stops

Do not choose an idea that requires real secrets, wallet signing, payment, private outreach, repository settings changes, KYC, debt, recurring obligations, or legal/compliance claims without explicit human authorization.
