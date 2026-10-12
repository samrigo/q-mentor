#!/usr/bin/env python3
"""Deploy Q-Mentor into another repository for repository-local Copilot use.

    python scripts/deploy_repo_local.py TARGET_REPO [--domains finance] \
        [--targets qiskit,pennylane,dwave,classiq,pasqal-pulser] [--dry-run] [--force]

Copies (never symlinks):
  skills/*            -> TARGET/.github/skills/
  agent               -> TARGET/.github/agents/q-mentor.agent.md
  knowledge, domains, templates, schemas -> TARGET/.github/q-mentor/
Skill links ``../../knowledge/`` etc. are rewritten to ``../../q-mentor/knowledge/``.

Refuses to overwrite a file that changed since the last deployment (hash in
TARGET/.github/q-mentor/MANIFEST.json) or that it did not create, unless --force.
Writes MANIFEST.json listing every copied file, its sha256, and the plugin version.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_PACKS = {
    "qiskit": "providers-qiskit.md",
    "classiq": "providers-classiq.md",
    "dwave": "providers-dwave.md",
    "pasqal-pulser": "providers-pasqal-pulser.md",
    "pennylane": "framework-pennylane.md",
}
SHARED_DIRS = ("templates", "schemas")
REWRITE = {f"../../{d}/": f"../../q-mentor/{d}/" for d in ("knowledge", "domains", "templates", "schemas")}
REWRITE["](../../schemas/)"] = "](../../q-mentor/schemas/)"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def plan(domains: list[str], targets: list[str]) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        for old, new in REWRITE.items():
            text = text.replace(old, new)
        files[f".github/skills/{skill.parent.name}/SKILL.md"] = text.encode()
    agent = ROOT / "com.github.copilot" / "agents" / "q-mentor.agent.md"
    files[".github/agents/q-mentor.agent.md"] = agent.read_bytes()
    skip = {v for k, v in TARGET_PACKS.items() if k not in targets}
    for f in sorted((ROOT / "knowledge").iterdir()):
        if f.is_file() and f.name not in skip:
            files[f".github/q-mentor/knowledge/{f.name}"] = f.read_bytes()
    for d in domains:
        src = ROOT / "domains" / d
        if not src.is_dir():
            raise SystemExit(f"unknown domain pack: {d}")
        for f in sorted(src.rglob("*")):
            if f.is_file():
                files[f".github/q-mentor/domains/{d}/{f.relative_to(src).as_posix()}"] = f.read_bytes()
    for d in SHARED_DIRS:
        for f in sorted((ROOT / d).iterdir()):
            if f.is_file():
                files[f".github/q-mentor/{d}/{f.name}"] = f.read_bytes()
    return files


def deploy(target: Path, domains: list[str], targets: list[str], dry_run: bool, force: bool) -> dict:
    unknown = set(targets) - TARGET_PACKS.keys()
    if unknown:
        raise SystemExit(f"unknown execution targets: {sorted(unknown)}")
    if not target.is_dir():
        raise SystemExit(f"target repository not found: {target}")
    manifest_path = target / ".github" / "q-mentor" / "MANIFEST.json"
    previous = json.loads(manifest_path.read_text())["files"] if manifest_path.exists() else {}
    files = plan(domains, targets)
    actions, conflicts = [], []
    for rel, data in files.items():
        dest = target / rel
        if dest.exists():
            current = sha(dest.read_bytes())
            if current == sha(data):
                actions.append(("unchanged", rel))
                continue
            if previous.get(rel) != current and not force:
                conflicts.append(rel)
                continue
            actions.append(("update", rel))
        else:
            actions.append(("create", rel))
    if conflicts:
        for c in conflicts:
            print(f"REFUSE  {c} (changed locally or not created by q-mentor; use --force after review)")
        raise SystemExit(2)
    for act, rel in actions:
        print(f"{'DRY-RUN ' if dry_run else ''}{act:9} {rel}")
    if dry_run:
        return {"dry_run": True, "actions": actions}
    for act, rel in actions:
        if act == "unchanged":
            continue
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(files[rel])
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    manifest = {
        "plugin": "q-mentor",
        "version": version,
        "deployed": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "domains": domains,
        "targets": targets,
        "files": {rel: sha(data) for rel, data in files.items()},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"deployed q-mentor {version}: {len(files)} files -> {target}")
    return manifest


def remove(target: Path, dry_run: bool) -> None:
    manifest_path = target / ".github" / "q-mentor" / "MANIFEST.json"
    if not manifest_path.exists():
        raise SystemExit("no q-mentor deployment manifest found")
    files = json.loads(manifest_path.read_text())["files"]
    for rel, digest in files.items():
        p = target / rel
        if not p.exists():
            continue
        if sha(p.read_bytes()) != digest:
            print(f"KEEP     {rel} (changed locally)")
            continue
        print(f"{'DRY-RUN ' if dry_run else ''}remove    {rel}")
        if not dry_run:
            p.unlink()
    if not dry_run:
        manifest_path.unlink()
        for d in sorted({(target / r).parent for r in files}, key=lambda x: len(x.parts), reverse=True):
            if d.exists() and not any(d.iterdir()):
                d.rmdir()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--domains", default="finance")
    ap.add_argument("--targets", default=",".join(TARGET_PACKS))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--remove", action="store_true", help="remove a previous deployment (keeps locally changed files)")
    a = ap.parse_args()
    target = Path(a.target).resolve()
    if a.remove:
        remove(target, a.dry_run)
        return 0
    deploy(target, [d for d in a.domains.split(",") if d], [t for t in a.targets.split(",") if t], a.dry_run, a.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
