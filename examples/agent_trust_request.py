#!/usr/bin/env python3
"""Print the canonical local Agent Trust Bundle request JSON.

This example is intentionally tiny and standard-library only. It performs no
network calls, no wallet access, no tool execution, and no real-money action.
It only prints a versioned JSON request that can be sent to the local Agent
Trust CLI or HTTP surfaces.
"""

from __future__ import annotations

import json
from pathlib import Path

REQUEST = json.loads((Path(__file__).with_name("input.json")).read_text(encoding="utf-8"))

print(json.dumps(REQUEST, sort_keys=True, indent=2, ensure_ascii=False))
