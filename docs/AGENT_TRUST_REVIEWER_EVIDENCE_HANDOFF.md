# Agent Trust reviewer evidence handoff

Local-only packet for the first Agent Trust reviewer. This is not outreach, a
publication, a hosted-security claim, or a request to use wallets, payments,
accounts, or live networks. It is the smallest review path after the local
evidence transcript exists.

## Goal

Help a reviewer answer one concrete question:

> Is the current Agent Trust packet clear and trustworthy enough for a small
> experimental integration behind a human-review gate?

## Latest local readiness checkpoint

Last refreshed after the autonomous strategic-backlog pulse for **Agent Trust →
first reviewers / clients**.

Run from the repository root:

```bash
python3 examples/agent_trust_adoption_readiness.py
```

Current local result:

- `ok=true`
- `ready_for_local_adoption_experiment=true`
- `ready_for_reviewer_handoff=true`
- recommended path: `bash scripts/agent_trust_first_run.sh`
- posture: `integrate_experimentally_with_human_review_gate`
- consumer decision: `integrate_experimentally`
- framework gate action: `review`
- doctor consistency: `98/98`, failed `0`
- risky action performed: `false`
- network calls / wallet access / real money / external execution: `false`

The next smallest safe reviewer ask is:

> Send one sanitized agent memory / planning / tool / MCP / payment / contact
> risk summary with task-warrant fields so Agent Trust can return
> `proceed` / `review` / `deny` before action.

This checkpoint is local evidence only. It does not prove hosted reliability,
third-party demand, legal/compliance suitability, real-wallet behavior, real
payment behavior, or safety for arbitrary external MCP/tool endpoints.

## Run path

From the repository root:

```bash
python3 examples/agent_trust_evidence_transcript.py
python3 examples/agent_trust_reviewer_response_packet.py
```

Optional consistency check:

```bash
python3 examples/agent_trust_doctor.py
```

For adoption/readiness posture, also run:

```bash
python3 examples/agent_trust_adoption_readiness.py
```

## Structural prompt-injection deny proof

Agent Trust now includes an executable local proof for the structural
prompt-injection class where untrusted content attempts to mix privileged
context or secrets with an external action. A first reviewer can run it without
network, wallet, signing, payment, posting, outreach, account use, or untrusted
execution:

```bash
python3 examples/agent_trust_runtime_signal_gate.py --prompt-injection-demo --expect-decision deny --compact
```

Expected review signal:

- `pre_action_decision` is `deny`;
- `requested_action` is `publish_post_with_secret_context_from_untrusted_page`;
- scanner signals include `prompt_injection`, `credential_exfiltration`, and
  `untrusted_content_requests_external_action`;
- the packet remains advisory evidence, not certification, compliance approval,
  hosted enforcement, or permission to perform the blocked action.

Reviewer question: is this structural-deny proof clear enough to show where an
agent should stop when untrusted text tries to drive privileged context into a
posting/tool/browser action?

## Provenance evidence check

DNS-AID/ANS-style discovery and identity signals are **provenance evidence, not
trust**. They can help a reviewer see which discovery path, endpoint/transport
claim, or operator/identity claim was recorded, but they do not authorize an
agent to act. Agent Trust must still evaluate the specific policy, warrant,
risk, and action boundary before any tool, MCP, API, wallet, signing, payment,
or outreach step.

For the first-pilot path, inspect these local artifacts together:

- `examples/input.json` — canonical request shape, including provenance-style evidence fields.
- `examples/output.json` — deterministic bundle output showing how evidence remains subject to verdict/policy evaluation.
- `examples/agent_trust_review_packet.json` — machine-readable reviewer map and proof commands.
- `python3 examples/agent_trust_doctor.py` — consistency check that the canonical artifacts remain aligned.

Reviewer question: is the provenance signal recorded clearly enough to explain
*where the claim came from* while still preventing discovery/identity from being
mistaken for authorization?

## What the reviewer should inspect

1. The evidence transcript summary and its stated local-only boundary.
2. The reviewer response packet verdict fields.
3. Any blocker that prevents `integrate_experimentally_with_human_review_gate`.
4. Whether the no-network / no-wallet / no-signing / no-payment / no-outreach
   boundary is visible without reading source code.
5. Whether reviewer-facing evidence and local audit/log examples avoid copying
   raw assistant-observed plaintext or derived context when a minimized summary
   would work: decrypted UI text, message previews, screenshots, OCR text,
   embeddings, ad/analytics labels, and similar hints should be treated as
   sensitive even when they are not literal secrets.
6. Whether the first integration question is specific enough to answer.
7. Whether the latest adoption-readiness checkpoint justifies a human-review-gated
   experimental integration, or whether it exposes a blocker first.

## Expected useful response

A useful reviewer response should contain:

- `accepted`, `rejected`, or `needs_update`;
- the first blocker, if any;
- the smallest product change that would remove the blocker;
- whether a human-review-gated pilot conversation would be justified;
- no secrets, private contact data, wallet material, payment credentials,
  account instructions, raw decrypted UI text, message previews, screenshots,
  embeddings, ad/analytics labels, or other derived-context payloads; sanitize
  or summarize them instead.

## Stop conditions

Stop before any of the following:

- external posting or private outreach;
- live network, wallet, signing, payment, or real-money action;
- claims that Agent Trust is hosted, audited, compliant, or proven safe against
  arbitrary tools;
- storing private reviewer contact details in git;
- copying raw screenshots, decrypted UI text, message previews, embeddings,
  analytics/ad labels, or similar derived context into git/chat when a short
  sanitized description would preserve the review signal;
- changing repository settings or publication surfaces.

## Current use

This packet is meant to be attached mentally to the existing first-reviewer
quickstart and local evidence transcript. It turns the proof bundle into a
review request shape without sending it anywhere.

The current local adoption-readiness checkpoint says the packet is ready for a
reviewer handoff **only behind a human-review gate**. The next move may be a
sanitized review request or a prepared publication/draft through an authorized
gate, but not private outreach, hosted claims, payment setup, or live external
action without an explicit boundary-crossing decision.
