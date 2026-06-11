# Agent Trust threat model and residual risk

Agent Trust is a local, dependency-free advisory pre-action review surface. It emits deterministic evidence packets for agents, wrappers, or humans that are deciding whether a proposed tool/MCP/skill/payment-like action should proceed, require review, or be denied.

This document is the P0 threat model for the current implementation. It is intentionally blunt: Agent Trust is useful only when its limits are explicit.

## Security posture summary

Agent Trust currently provides **advisory review**, not privileged enforcement.

- It can classify declared action/tool/payment-like risk into `proceed`, `review`, or `deny` evidence.
- It can preserve a deterministic local receipt for later inspection.
- It can conservatively redact secret-shaped values before packets become review artifacts or logs.
- It cannot force a compromised, prompt-injected, or malicious acting agent to obey the verdict unless an external chokepoint makes the verdict mandatory.

Production use therefore requires a separate wrapper, broker, sandbox, policy engine, or capability gate that the acting agent cannot bypass.

## Protected assets

Agent Trust is designed to reduce accidental or adversarial misuse around these assets:

1. **Secrets and credentials** — API keys, OAuth tokens, passwords, wallet keys, seed phrases, recovery codes, session material, and secret-like arguments.
2. **Tool and MCP authority** — local tools, external MCP servers, browser automation, filesystem access, shell execution, plugin/skill installs, scanners, and workflow helpers.
3. **Payment and wallet authority** — x402-like payment requests, quotes, wallet/signing boundaries, spend decisions, testnet/mainnet separation, and real-money actions.
4. **Agent identity and delegated grants** — which agent is acting, what scopes it has, and whether a requested action exceeds least privilege.
5. **Review evidence** — deterministic JSON packets, decision receipts, scanner/registry signals, provenance notes, and audit trails.
6. **Agent Trust itself** — its source code, examples, schemas, docs, release artifacts, and installation path.

## Adversaries and abuse cases

Agent Trust assumes these adversaries may exist:

- **Malicious skill/tool/MCP author** shipping clean metadata with hostile implementation behavior.
- **Prompt-injected content** attempting to convince the acting agent to ignore, reinterpret, or bypass Agent Trust verdicts.
- **Hostile MCP server or external tool** requesting broad scopes, hiding dangerous behavior, or exfiltrating data through arguments/results.
- **Dishonest or incomplete manifest** under-declaring permissions, capabilities, network behavior, filesystem access, payment behavior, or lifecycle hooks.
- **Compromised acting agent** that receives a `deny` or `review` verdict and chooses to proceed anyway.
- **Tampering party** modifying advisory JSON packets at rest or in transit when no external integrity/signature layer is used.
- **Supply-chain attacker** targeting Agent Trust itself through unpinned installs, mutable branches, package-name confusion, compromised dependencies, malicious forks, or altered release artifacts.
- **Denial-of-service input** using oversized, deeply nested, or adversarially encoded JSON to stress parsers, normalizers, or logging paths.
- **Obfuscation attacker** hiding sensitive material or dangerous instructions through unicode homoglyphs, zero-width characters, encoded strings, misleading labels, or benign-looking fields.

## Trust boundaries

Current boundaries:

| Boundary | Trusted? | Notes |
|---|---:|---|
| Agent Trust code running locally from the inspected repository checkout | Partially | Trusted only to the degree the local checkout/release path is trusted. Supply-chain integrity is still a risk. |
| Request JSON from an agent/tool/MCP/skill/repo | No | Treat all fields as attacker-controlled evidence. |
| Tool, skill, MCP, repo, schema, or manifest metadata | No | Metadata is evidence, never authorization. Clean declarations do not prove safe implementation behavior. |
| Scanner/registry verdicts | Partially | Useful as input signals, but they do not override runtime identity, grants, action sensitivity, or missing evidence. |
| Agent Trust advisory verdict packet | Partially | Deterministic local evidence, not enforcement and not authenticated by default. |
| Acting agent that consumes the packet | No by default | It may be confused, injected, compromised, or incentivized to bypass the verdict. |
| External wrapper/broker/sandbox/policy gate | Required for enforcement | This is the component that must make Agent Trust decisions mandatory in production. |

## In-scope threats

Agent Trust aims to help identify and document:

- missing, empty, or materially underspecified action/tool/skill declarations;
- self-declared scopes that appear inconsistent with requested action sensitivity;
- declared or signaled network, filesystem, execution, browser, wallet, payment, outreach, posting, scanner, or lifecycle-hook authority;
- MCP/tool supply-chain and RCE-style signals such as install/activation-time code execution, runtime tool bridges, ambient process/filesystem/token authority, untrusted server control over tools or arguments, and mutable or insufficiently pinned source/version evidence;
- prompt-injection and instruction-smuggling signals inside descriptor fields;
- structural prompt-injection flows where untrusted content attempts to drive privileged context, secrets, or external actions; the local runtime signal gate exposes this as an executable deny proof via `python3 examples/agent_trust_runtime_signal_gate.py --prompt-injection-demo --expect-decision deny --compact`;
- authority-bearing persistence surfaces where untrusted content asks for writes to future-trusted skills, prompts, hooks, configs, memory, policy, or source files; this can create delayed cross-session instruction persistence even without shell access, and the local runtime signal gate exposes it via `python3 examples/agent_trust_runtime_signal_gate.py --authority-persistence-demo --expect-decision deny --compact`;
- scanner/registry/provenance signals that should force review or denial at runtime, including scanner-pass fallacy / marketplace scanner bypass cases where clean scanner labels conflict with authority, provenance, install-hook, or semantic-risk evidence; the local layered skill-scanning proof is `python3 examples/agent_trust_layered_skill_scanning.py --scanner-pass-fallacy-demo --expect-decision deny --compact --fail-on-fail`;
- x402/payment-like requests that require independent spend control before any signing or transfer;
- secret-shaped values that should not be persisted into bundles, receipts, diagnostics, or logs;
- provenance gaps that make a `proceed` decision unjustified.

## Out-of-scope threats

Agent Trust does **not** currently:

- execute or sandbox third-party code;
- fetch remote manifests or verify live network behavior;
- prove that declared metadata matches implementation behavior;
- enforce verdicts against an acting agent;
- authenticate, sign, or timestamp packets by itself;
- provide package signing, SBOM, SLSA provenance, or release attestation by itself;
- replace OS sandboxing, browser isolation, wallet policy, spend limits, IAM, CI policy, EDR, code review, or human security ownership;
- authorize real-money spend, signing, KYC, account changes, posting, private outreach, or production deployment.

## Residual risks

### Advisory-vs-enforcement gap

A `deny` packet is only useful if something respects it. A compromised or prompt-injected agent can be told to ignore Agent Trust, reinterpret `deny` as `allow`, call a lower-level tool directly, or omit Agent Trust from the path entirely.

Residual risk: **high** until Agent Trust is placed behind a privileged chokepoint the acting agent cannot bypass.

Required production control: a wrapper/proxy/tool broker/sandbox/policy engine that intercepts sensitive actions and refuses to execute unless the Agent Trust decision and independent policy checks pass.

### Self-declaration and metadata limits

Current classification often relies on request JSON, descriptor fields, manifests, labels, and declared permissions. A malicious tool can under-declare, omit, or mislabel capabilities.

Residual risk: **high** for dishonest inputs.

Current mitigation: missing, empty, or materially underspecified declarations must produce review/deny rather than silent proceed. Scanner/registry/provenance signals are evidence, not final authority. The local layered skill-scanning receipt now includes an `mcp_supply_chain_rce` layer; critical signals in that layer conservatively aggregate to `deny` when a descriptor shows install-time execution, untrusted MCP/server-side tool control, or equivalent supply-chain/RCE-style authority.

Needed future mitigation: optional local static inspection against lockfiles/manifests/source trees, explicit declared-vs-observed diffs, and adversarial corpus tests for under-declaration.

### Contract-first scrutiny risk

Contract-first reading is useful for token economy and integration shape, but attacker-controlled metadata can be weaponized to lower scrutiny. A clean `SKILL.md`, `index.json`, schema, manifest, or README must never be treated as proof of safety.

Residual risk: **medium to high** when agents read metadata before implementation.

Rule: metadata can start review, but cannot finish it for sensitive actions.

### Unauthenticated packet limits

Agent Trust packets are deterministic local evidence, but they are not signed or authenticated by default. If copied between systems or stored where an attacker can write, verdicts and reasons can be modified.

Residual risk: **medium** for audit/review workflows that rely on packets after transport or storage.

Current mitigation: optional detached SHA-256 attestations can verify canonical redacted packet bytes and detect later tampering. Residual limitation: these attestations are unauthenticated by default and do not prove authorship, origin, or trusted storage/transport unless paired with external signatures, transparency logs, trusted channels, or a non-bypassable policy chokepoint.

### Secret-redaction limits

Agent Trust now conservatively redacts secret-shaped string values and values under secret-like keys before returning bundles, receipts, diagnostics, and runtime gate packets.

Residual risk remains:

- redaction is pattern-based and may miss novel or domain-specific secret formats;
- redaction is a last-resort leakage guard, not permission to submit secrets;
- secrets may leak before Agent Trust sees them if callers log raw request JSON;
- encoded, split, homoglyph, or zero-width-obfuscated secrets may require additional tests.

Rule: callers must avoid submitting real secrets. Agent Trust packets should be treated as review artifacts, not secret stores.

### Supply-chain risk of Agent Trust itself

A security tool installed from mutable git branches, editable checkouts, or an unreserved package name can become the attack path.

Residual risk: **high** until distribution is pinned and attestable.

Needed controls:

- tagged releases with immutable install instructions;
- package-name reservation or explicit warning when not published;
- checksums/signatures for release artifacts;
- SBOM and provenance where practical;
- CI/code scanning/dependency review;
- clear maintainer accountability and disclosure channel.

### Input resource-exhaustion and normalization bypass

Untrusted JSON can be oversized, deeply nested, or encoded to evade simple checks. Unicode homoglyphs, zero-width characters, mixed normalization forms, and encoded secret/injection strings remain relevant bypass classes.

Residual risk: **medium** until size/depth limits and adversarial normalization tests are comprehensive.

## Required external chokepoints for production use

Before Agent Trust can be called a production security boundary, at least one non-bypassable enforcement layer must exist between the acting agent and sensitive capability:

1. **Tool broker / MCP proxy** — all sensitive tool/MCP calls pass through it; direct lower-level calls are unavailable to the agent.
2. **Capability-scoped runtime** — the agent receives only minimal grants; denied actions are impossible, not merely discouraged.
3. **Filesystem/network/browser sandbox** — policy denies unsafe paths, hosts, methods, uploads, downloads, and browser actions even if the agent asks directly.
4. **Wallet/payment/spend controller** — signing and payment require independent limits, explicit spend policy, audit logs, and stop path; Agent Trust verdicts alone never authorize spend.
5. **Receipt integrity layer** — review packets are hashed/signed before transport/storage when later audit matters.
6. **Human/security change gate** — changes to verdict logic, schemas, secret detection, boundary definitions, release signing, or production policy require review outside the self-improvement loop.

## Current safe claim

The accurate claim is:

> Agent Trust is a local advisory pre-action review and evidence packet generator for agent/tool/MCP/payment-like risk. It can improve decision quality and auditability before action, but it is not an enforcement boundary unless wired behind a privileged chokepoint the acting agent cannot bypass.

That sentence should govern public copy, demos, and integration guidance until enforcement exists.
