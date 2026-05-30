import json
import subprocess
import sys


def run_skill(*args):
    completed = subprocess.run(
        [sys.executable, "-m", "agent_trust.skill", *args],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def test_skill_manifest_is_inert_and_local():
    manifest = run_skill("manifest", "--compact")
    assert manifest["ok"] is True
    assert "no_network_calls_performed_by_this_skill" in manifest["never_does"]
    assert "install_skill" in manifest["supported_actions"]


def test_install_skill_with_secret_and_network_requires_review_or_denial():
    verdict = run_skill(
        "check",
        "--action", "install_skill",
        "--source", "github",
        "--url", "https://github.com/example/pr-review-helper",
        "--requested-permission", "repo_read,read_env,network",
        "--warrant", "summarize current PR only",
        "--boundary", "no secrets, no external upload, no credential access",
        "--compact",
    )
    assert verdict["ok"] is True
    assert verdict["source_classification"] == "untrusted_external_skill"
    assert verdict["secret_access_authorized"] is False
    assert verdict["decision"] in {"deny_or_require_review", "require_review"}
    assert verdict["asbom"]["provenance_evidence_not_trust"] is True
