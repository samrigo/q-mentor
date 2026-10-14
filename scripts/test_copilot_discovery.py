"""Plugin-mode discovery with the real Copilot CLI (no login needed): install from a clean copy, list skills, check
that the custom agent ships, disable/enable, uninstall. Requires QMENTOR_COPILOT_BIN; otherwise reports `skipped`
(never `passed`)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    cli = os.environ.get("QMENTOR_COPILOT_BIN")
    if not cli:
        print("copilot discovery: skipped (QMENTOR_COPILOT_BIN not set)")
        return 0
    with tempfile.TemporaryDirectory(prefix="qm-copilot-") as tmp:
        home, copy = Path(tmp) / "home", Path(tmp) / "q-mentor"
        home.mkdir()
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv*"))
        env = dict(os.environ, HOME=str(home))

        def cop(*args):
            return subprocess.run([cli, *args], capture_output=True, text=True, env=env, cwd=tmp, timeout=180)

        version = cop("--version").stdout.strip().splitlines()[0]
        out = cop("plugin", "install", str(copy))
        assert out.returncode == 0 and "Installed 17 skills" in out.stdout, out.stdout + out.stderr
        listed = json.loads(cop("skill", "list", "--json").stdout)
        names = sorted(s["name"] for s in listed if s["name"].startswith("q-mentor") and s.get("source") == "plugin")
        assert len(names) == 17, names
        installed = next(home.rglob("q-mentor.agent.md"), None)
        assert installed is not None, "custom agent not installed"
        assert "q-mentor (v" in cop("plugin", "list").stdout
        cop("plugin", "disable", "q-mentor")
        disabled = json.loads(cop("skill", "list", "--json").stdout)
        assert not [s for s in disabled if s["name"].startswith("q-mentor") and s.get("enabled", True)]
        cop("plugin", "enable", "q-mentor")
        assert cop("plugin", "uninstall", "q-mentor").returncode == 0
        after = json.loads(cop("skill", "list", "--json").stdout)
        assert not [s for s in after if s["name"].startswith("q-mentor")]
    print(f"PASS {version}: plugin install -> 17 skills + custom agent; disable -> 0 enabled; uninstall -> 0")
    print("copilot discovery: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
