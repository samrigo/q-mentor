"""Repository-local deployment lifecycle test: clean install, help in repository mode, conflict refusal, update with
backup, rollback, re-install, removal. Optional: Copilot CLI discovery of the deployed project skills when
QMENTOR_COPILOT_BIN points at a `copilot` binary (no login needed for `copilot skill list`)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = [sys.executable, str(ROOT / "scripts/deploy_repo_local.py")]


def run(args, cwd=None, check=True, env=None):
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)
    if check and proc.returncode != 0:
        raise SystemExit(f"command failed: {args}\n{proc.stdout}\n{proc.stderr}")
    return proc


def main() -> int:
    steps = []
    with tempfile.TemporaryDirectory(prefix="qm-repo-") as tmp:
        repo = Path(tmp)
        run(["git", "init", "-q", str(repo)])
        # 1. dry run writes nothing
        run(DEPLOY + ["--target", str(repo), "--dry-run"])
        assert not (repo / ".github").exists()
        steps.append("dry-run writes nothing")
        # 2. clean install
        run(DEPLOY + ["--target", str(repo)])
        manifest = json.loads((repo / ".github/q-mentor/MANIFEST.json").read_text())
        skills = sorted(p.parent.name for p in (repo / ".github/skills").glob("*/SKILL.md"))
        assert len(skills) == 17 and (repo / ".github/agents/q-mentor.agent.md").exists()
        assert not any(p.is_symlink() for p in repo.rglob("*"))
        steps.append(f"install: {len(manifest['files'])} files, {len(skills)} skills, no symlinks")
        # 3. help and linter work from the repository copy (registry resolved from .github/q-mentor)
        out = run([sys.executable, str(repo / ".github/q-mentor/scripts/render_help.py"), "--all"]).stdout
        assert out.count("`/q-mentor-") == 16, out
        steps.append("help renders 16 user-facing skills from .github/q-mentor/registry")
        # 4. missing registry is a visible block, not a guess
        reg = repo / ".github/q-mentor/registry/skills.yml"
        saved = reg.read_text()
        reg.unlink()
        blocked = run([sys.executable, str(repo / ".github/q-mentor/scripts/render_help.py"), "--all"], check=False)
        assert "Status: blocked" in (blocked.stdout + blocked.stderr)
        reg.write_text(saved)
        steps.append("missing registry -> Status: blocked")
        # 5. local edit is never overwritten silently
        skill = repo / ".github/skills/q-mentor-learn/SKILL.md"
        skill.write_text(skill.read_text() + "\nlocal note\n")
        refused = run(DEPLOY + ["--target", str(repo)], check=False)
        assert refused.returncode == 1 and "CONFLICT" in refused.stdout
        skill.write_text(skill.read_text().replace("\nlocal note\n", ""))
        steps.append("changed file -> CONFLICT, nothing written")
        # 6. update from an older version keeps a backup
        mpath = repo / ".github/q-mentor/MANIFEST.json"
        old = json.loads(mpath.read_text())
        old["version"] = "0.0.0-test"
        target_rel = ".github/q-mentor/knowledge/pqc.md"
        (repo / target_rel).write_text("old pack\n")
        import hashlib
        old["files"][target_rel]["sha256"] = hashlib.sha256(b"old pack\n").hexdigest()
        mpath.write_text(json.dumps(old, indent=2))
        run(DEPLOY + ["--target", str(repo)])
        assert (repo / ".github/q-mentor/backup/0.0.0-test" / target_rel).read_text() == "old pack\n"
        assert (repo / target_rel).read_text() != "old pack\n"
        steps.append("update -> backup of the previous version")
        # 7. rollback restores the previous version and manifest
        run(DEPLOY + ["--target", str(repo), "--rollback"])
        assert (repo / target_rel).read_text() == "old pack\n"
        assert json.loads(mpath.read_text())["version"] == "0.0.0-test"
        steps.append("rollback restores files and manifest")
        # 8. re-install current version, optional Copilot CLI discovery
        run(DEPLOY + ["--target", str(repo)])
        cli = os.environ.get("QMENTOR_COPILOT_BIN")
        if cli:
            env = dict(os.environ, HOME=str(repo / ".home"))
            listed = json.loads(run([cli, "skill", "list", "--json"], cwd=repo, env=env).stdout)
            project = [s["name"] for s in listed if s["name"].startswith("q-mentor") and s.get("source") == "project"]
            assert len(project) == 17, project
            steps.append(f"copilot skill list (repository mode): {len(project)} project skills")
        else:
            steps.append("copilot CLI discovery skipped (QMENTOR_COPILOT_BIN not set)")
        # 9. removal leaves nothing behind
        run(DEPLOY + ["--target", str(repo), "--uninstall"])
        leftovers = [p for p in (repo / ".github").rglob("*") if p.is_file()] if (repo / ".github").exists() else []
        assert not leftovers, leftovers
        steps.append("uninstall removes every deployed file")
    for s in steps:
        print("PASS", s)
    print("deploy lifecycle: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
