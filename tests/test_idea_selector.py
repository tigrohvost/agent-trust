from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_idea_selector_selects_machine_readable_loop() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples" / "agent_trust_idea_selector.py"),
            "--ideas",
            str(ROOT / "examples" / "ideas.json"),
            "--compact",
        ],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["selected_id"] == "machine-readable-improvement-selector"
    assert payload["ranked"][0]["score"] >= payload["ranked"][1]["score"]
    assert "local-only" in payload["safety_boundary"]
