# Agent Trust

**Agent Trust** is a small, dependency-free Python package for local pre-action trust checks by autonomous agents.

It creates deterministic review bundles before an agent lets a tool, MCP server, skill, repository helper, x402 endpoint, or other dependency touch sensitive authority such as secrets, filesystem writes, network egress, wallet signing, payments, or external posting.

Core boundary: **local only, no network calls, no wallet access, no tool execution, no real-money action**.

**Authorship:** Agent Trust is created and maintained by **Rain (Ouroboros)** as an agent-security skill for humans and autonomous agents that need inspectable trust boundaries before action.

## Agent compatibility

Agent Trust is packaged as a portable skill/review boundary for **OpenClaw, Hermes-style agents, Claude, Codex, and other agent runtimes** that can read a repository-level `SKILL.md` or follow local CLI instructions.

Use it when an agent is about to install or authorize a tool, MCP server, skill, repository helper, x402 endpoint, or other dependency. The skill gives the agent a local, inspectable way to produce an `allow` / `review` / `deny` packet before secrets, network, filesystem writes, wallet signing, payments, or posting are allowed.

## Why

Autonomous agents increasingly install skills, call tools, connect MCP servers, negotiate x402-style paid resources, and act across accounts. Discovery is not trust. A public repository, DNS record, package name, or manifest is only evidence. Agent Trust turns that evidence into a small machine-readable packet that other humans/agents can inspect before action.

## Install

```bash
git clone https://github.com/tigrohvost/agent-trust.git
cd agent-trust
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
```

## Quick start

Print the CLI contract:

```bash
agent-trust --print-contract
# or
python3 -m agent_trust.cli --print-contract
```

Build a trust bundle from the checked-in example:

```bash
agent-trust --input examples/input.json
```

Run the skill manifest/check interface:

```bash
agent-trust-skill manifest --compact
agent-trust-skill check \
  --action install_skill \
  --source github \
  --url https://github.com/example/pr-review-helper \
  --requested-permission repo_read,read_env,network \
  --warrant 'summarize current PR only' \
  --boundary 'no secrets, no external upload, no credential access' \
  --compact
```

Run tests:

```bash
pytest -q
```

## What the bundle says

A bundle includes:

- `verdict`: `allow`, `review`, or `deny`
- `reasons`: why review/denial was chosen
- `controls`: explicit safety controls
- `policy_quote`: local x402-style budget/resource policy quote
- `tool_risk`: risk signals for tools/MCP/skills/helpers
- `provenance_evidence`: discovery/identity evidence, explicitly not treated as authorization
- side-effect flags: `network_calls=false`, `wallet_access=false`, `execution=false`

## Typical use cases

- Gate a new MCP server before it sees secrets or tools.
- Review an agent skill/plugin before installation.
- Produce a machine-readable packet for a human reviewer.
- Check whether an x402 resource is inside local policy before any live payment flow.
- Convert scanner findings into `allow/review/deny` pre-action decisions.

## Security model

Agent Trust is a **pre-action review boundary**, not a sandbox and not a formal proof system.

It does not:

- execute third-party code;
- fetch remote manifests;
- read secret values;
- sign wallet messages;
- submit payments;
- publish posts or contact people;
- make compliance claims.

It does:

- classify obvious authority surfaces;
- preserve evidence in deterministic JSON;
- make risky next steps explicit;
- force discovery/provenance to remain evidence rather than trust.

## Python API

```python
from agent_trust import build_agent_trust_bundle

bundle = build_agent_trust_bundle(
    policy={
        "agent_id": "demo-agent",
        "budget": "1.00",
        "spent": "0.10",
        "allowed_resources": ["https://api.example.test/report"],
        "settlement": "none",
    },
    resource="https://api.example.test/report",
    tool_descriptor={
        "name": "pr-review-helper",
        "transport": "https",
        "env": ["GITHUB_TOKEN"],
        "command": "run helper",
    },
)
print(bundle["verdict"])
```

## Repository layout

```text
agent_trust/          Python package
examples/             sample input/output and skill manifest
schemas/              JSON-schema contract artifacts
tests/                pytest coverage for bundle, CLI, and skill behavior
README.md             English + Russian documentation
```

## Status

Alpha. The contract is intentionally small and inspectable. Expect iteration, but the current safety boundary is part of the public promise: local-only review, no hidden action.

---

# Agent Trust / русский

**Agent Trust** — небольшой Python-пакет без обязательных зависимостей для локальной проверки действий автономных агентов перед тем, как они получают доступ к чувствительным полномочиям.

Он строит детерминированный trust bundle перед использованием tool/MCP/skill/repository helper/x402 endpoint или другой зависимости, которая может запросить секреты, запись в файловую систему, сетевой выход, подпись кошельком, платежи или внешнюю публикацию.

Главная граница: **только локально, без сетевых вызовов, без доступа к кошельку, без выполнения чужих инструментов, без real-money действий**.

**Авторство:** Agent Trust создан и поддерживается **Rain (Ouroboros)** как agent-security skill для людей и автономных агентов, которым нужна проверяемая граница доверия перед действием.

## Совместимость с агентами

Agent Trust оформлен как переносимый skill / review boundary для **OpenClaw, Hermes-style агентов, Claude, Codex и других agent runtimes**, которые умеют читать корневой `SKILL.md` или следовать локальным CLI-инструкциям.

Используйте его, когда агент собирается установить или разрешить tool, MCP server, skill, repository helper, x402 endpoint или другую зависимость. Skill даёт агенту локальный и проверяемый способ получить `allow` / `review` / `deny` packet до доступа к секретам, сети, записи в файловую систему, подписи кошельком, платежам или публикациям.

## Зачем это нужно

Агенты всё чаще устанавливают скиллы, подключают MCP-серверы, вызывают инструменты, работают с x402 и действуют через аккаунты. Обнаружение — это не доверие. Публичный репозиторий, DNS-запись, имя пакета или manifest — только свидетельство. Agent Trust превращает такие свидетельства в маленький machine-readable пакет, который человек или другой агент может проверить до действия.

## Установка

```bash
git clone https://github.com/tigrohvost/agent-trust.git
cd agent-trust
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
```

## Быстрый старт

Показать контракт CLI:

```bash
agent-trust --print-contract
# или
python3 -m agent_trust.cli --print-contract
```

Построить bundle по примеру:

```bash
agent-trust --input examples/input.json
```

Проверить skill-интерфейс:

```bash
agent-trust-skill manifest --compact
agent-trust-skill check \
  --action install_skill \
  --source github \
  --url https://github.com/example/pr-review-helper \
  --requested-permission repo_read,read_env,network \
  --warrant 'summarize current PR only' \
  --boundary 'no secrets, no external upload, no credential access' \
  --compact
```

Тесты:

```bash
pytest -q
```

## Что внутри bundle

- `verdict`: `allow`, `review` или `deny`
- `reasons`: причины review/deny
- `controls`: явные safety controls
- `policy_quote`: локальная x402-style оценка бюджета/ресурса
- `tool_risk`: признаки риска tool/MCP/skill/helper
- `provenance_evidence`: evidence происхождения/идентичности, но не авторизация
- флаги побочных эффектов: `network_calls=false`, `wallet_access=false`, `execution=false`

## Модель безопасности

Agent Trust — это **граница предварительной проверки**, а не sandbox и не формальное доказательство безопасности.

Он не выполняет чужой код, не скачивает удалённые manifests, не читает значения секретов, не подписывает кошельком, не делает платежи, не публикует сообщения и не заявляет compliance.

Он классифицирует поверхности полномочий, сохраняет evidence в JSON, явно показывает risky next steps и не позволяет путать provenance с trust.

## License

MIT.
