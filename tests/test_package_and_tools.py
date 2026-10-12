"""Package validation, repo-local deployment, and eval grader self-tests."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import run_evals  # noqa: E402
from validate_package import check  # noqa: E402


def test_package_validates():
    assert check(ROOT) == []


def test_eval_cases_validate_and_cover_lifecycle_and_targets():
    assert run_evals.validate_cases(run_evals.load_cases()) == []


def test_math_eval_suite_passes():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_math.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout


def deploy(*args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "deploy_repo_local.py"), *map(str, args)],
                          capture_output=True, text=True)


def test_deploy_dry_run_writes_nothing(tmp_path):
    r = deploy(tmp_path, "--dry-run")
    assert r.returncode == 0 and "DRY-RUN" in r.stdout
    assert not (tmp_path / ".github").exists()


def test_deploy_links_resolve_and_manifest(tmp_path):
    assert deploy(tmp_path).returncode == 0
    gh = tmp_path / ".github"
    skills = list((gh / "skills").glob("*/SKILL.md"))
    assert len(skills) == 14
    assert (gh / "agents" / "q-mentor.agent.md").exists()
    for s in skills:
        for link in re.findall(r"\]\(([^)#\s]+)", s.read_text()):
            if not link.startswith("http"):
                assert (s.parent / link).resolve().exists(), f"{s}: {link}"
    m = json.loads((gh / "q-mentor" / "MANIFEST.json").read_text())
    assert m["version"] and m["files"] and m["domains"] == ["finance"]
    assert not any(p.is_symlink() for p in tmp_path.rglob("*"))


def test_deploy_selects_target_packs(tmp_path):
    assert deploy(tmp_path, "--targets", "qiskit,pennylane").returncode == 0
    k = tmp_path / ".github" / "q-mentor" / "knowledge"
    assert (k / "providers-qiskit.md").exists()
    assert not (k / "providers-dwave.md").exists()


def test_deploy_refuses_to_overwrite_local_changes(tmp_path):
    assert deploy(tmp_path).returncode == 0
    f = tmp_path / ".github" / "skills" / "q-mentor-learn" / "SKILL.md"
    f.write_text(f.read_text() + "\nlocal edit\n")
    r = deploy(tmp_path)
    assert r.returncode == 2 and "REFUSE" in r.stdout
    assert "local edit" in f.read_text()


def test_deploy_refuses_unmanaged_existing_file(tmp_path):
    f = tmp_path / ".github" / "agents" / "q-mentor.agent.md"
    f.parent.mkdir(parents=True)
    f.write_text("someone else's agent")
    assert deploy(tmp_path).returncode == 2


def test_remove_keeps_changed_files(tmp_path):
    assert deploy(tmp_path).returncode == 0
    keep = tmp_path / ".github" / "skills" / "q-mentor-exec" / "SKILL.md"
    keep.write_text("changed")
    assert deploy(tmp_path, "--remove").returncode == 0
    assert keep.exists()
    assert not (tmp_path / ".github" / "skills" / "q-mentor-learn").exists()


CASE = {"id": "x", "suite": "behavior", "kind": "adversarial", "prompt": "p",
        "expect": {"verdict": "classical-now", "must_include": ["classical"],
                   "must_not_include": ["quantum advantage is achieved"], "max_words": 20}}


def test_grader_passes_good_response():
    assert run_evals.grade_response(CASE, "Verdict: classical-now. Use classical sorting.") == []


def test_grader_catches_hype_and_length():
    bad = "Verdict: bounded-experiment. Quantum advantage is achieved " + "word " * 30
    fails = run_evals.grade_response(CASE, bad)
    assert any("forbidden" in f for f in fails)
    assert any("verdict" in f for f in fails)
    assert any("words" in f for f in fails)


def test_grader_routing():
    case = {"id": "r", "suite": "routing", "kind": "positive", "prompt": "p", "expect": {"skill": "q-mentor-learn"}}
    assert run_evals.grade_response(case, "skill: q-mentor-learn\n...") == []
    assert run_evals.grade_response(case, "skill: q-mentor-verdict\n...")


def test_records_validate_against_schemas(qubo):
    import jsonschema
    from qmentor.demo import run
    from qmentor.targets import classiq_target, dwave_target, pennylane_target, pulser_target, qiskit_target
    cap = json.loads((ROOT / "schemas" / "capability-report.schema.json").read_text())
    for mod in (qiskit_target, pennylane_target, classiq_target, dwave_target, pulser_target):
        jsonschema.validate(mod.capability(qubo), cap)
    out = Path(__import__("tempfile").mkdtemp())
    rec = run(out, skip_quantum=True)
    jsonschema.validate(rec, json.loads((ROOT / "schemas" / "result-record.schema.json").read_text()))
    brief = (out / "executive-brief.md").read_text()
    assert "classical-now" in brief and "not** quantum advantage" in brief
    assert rec["advantage_claimed"] is False
