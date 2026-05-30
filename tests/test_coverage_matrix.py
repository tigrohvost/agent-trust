from pathlib import Path


def test_coverage_matrix_names_core_boundaries():
    text = Path("docs/COVERAGE_MATRIX.md").read_text(encoding="utf-8")
    for phrase in [
        "Secret exposure",
        "Tool / MCP / plugin risk",
        "Wallet / signing / payment boundary",
        "External skill installability",
        "Intentionally out of scope",
        "not by becoming huge",
    ]:
        assert phrase in text


def test_readme_and_skill_link_coverage_matrix():
    for file in ["README.md", "SKILL.md"]:
        assert "docs/COVERAGE_MATRIX.md" in Path(file).read_text(encoding="utf-8")
