#!/usr/bin/env python3
"""Select the next Agent Trust improvement from a small scored idea list.

This helper is intentionally dependency-free and local-only. It does not call
network services, read secrets, mutate repositories, or publish anything. Its
purpose is to make the improvement decision legible to another agent.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _as_int(item: dict[str, Any], key: str) -> int:
    value = item.get(key, 0)
    if not isinstance(value, int):
        raise SystemExit(f"idea {item.get('id', '<unknown>')} has non-integer {key!r}")
    if value < 1 or value > 5:
        raise SystemExit(f"idea {item.get('id', '<unknown>')} has {key!r} outside 1..5")
    return value


def score(item: dict[str, Any]) -> int:
    """Risk-adjusted priority score.

    Impact and evidence should pull an idea upward. Risk and effort should pull
    it downward. A small, strongly evidenced improvement should beat a dramatic
    but speculative expansion.
    """

    impact = _as_int(item, "impact")
    evidence = _as_int(item, "evidence")
    risk = _as_int(item, "risk")
    effort = _as_int(item, "effort")
    return impact * 3 + evidence * 2 - risk * 2 - effort


def load_ideas(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise SystemExit("ideas file must contain a non-empty JSON list")
    for item in data:
        if not isinstance(item, dict):
            raise SystemExit("each idea must be a JSON object")
        if not item.get("id") or not item.get("title"):
            raise SystemExit("each idea needs id and title")
        score(item)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Select the next Agent Trust improvement.")
    parser.add_argument("--ideas", type=Path, default=Path("examples/ideas.json"))
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args()

    ranked = sorted(load_ideas(args.ideas), key=lambda item: (-score(item), item["id"]))
    selected = ranked[0]
    result = {
        "selected_id": selected["id"],
        "selected_title": selected["title"],
        "score": score(selected),
        "reason": selected.get("notes", ""),
        "ranked": [
            {
                "id": item["id"],
                "title": item["title"],
                "score": score(item),
                "impact": item["impact"],
                "evidence": item["evidence"],
                "risk": item["risk"],
                "effort": item["effort"],
            }
            for item in ranked
        ],
        "safety_boundary": "local-only; no network, secrets, wallet, signing, payment, outreach, or repository settings changes",
    }
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
