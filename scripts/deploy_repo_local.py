"""Deploy Q-Mentor into a repository for cloud agent / IDE agent mode.

  .github/skills/<skill>/SKILL.md      (canonical skills)
  .github/agents/q-mentor.agent.md     (custom agent)
  .github/q-mentor/...                 (registry, schemas, templates, selected knowledge and domain packs)
  .github/q-mentor/MANIFEST.json       (versions + SHA-256 of every copied file)

Refuses to overwrite files changed since the last deployment (unless --force), supports
--dry-run and --uninstall, never creates symlinks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
TARGET_PACKS = {
    "qiskit": "providers-qiskit.md",
    "classiq": "providers-classiq.md",
    "dwave": "providers-dwave.md",
    "pasqal-pulser": "providers-pasqal-pulser.md",
    "pennylane": "framework-pennylane.md",
}
CORE_PACKS = ["INDEX.md", "quantum-basics.md", "optimization-math.md", "quantum-fit.md",
              "research-method.md", "recent-research.md", "pqc.md", "sources.yml"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plugin_version() -> str:
    return json.loads((ROOT / "plugin.json").read_text())["version"]


def plan(targets: List[str], domains: List[str]) -> List[Tuple[Path, str]]:
    items: List[Tuple[Path, str]] = []
    for skill in sorted((ROOT / "skills").iterdir()):
        if (skill / "SKILL.md").exists():
            items.append((skill / "SKILL.md", f".github/skills/{skill.name}/SKILL.md"))
    items.append((ROOT / "com.github.copilot/agents/q-mentor.agent.md", ".github/agents/q-mentor.agent.md"))
    for folder in ("registry", "schemas", "templates"):
        for f in sorted((ROOT / folder).iterdir()):
            items.append((f, f".github/q-mentor/{folder}/{f.name}"))
    for name in CORE_PACKS + [TARGET_PACKS[t] for t in targets]:
        items.append((ROOT / "knowledge" / name, f".github/q-mentor/knowledge/{name}"))
    for domain in domains:
        for f in sorted((ROOT / "domains" / domain).iterdir()):
            items.append((f, f".github/q-mentor/domains/{domain}/{f.name}"))
    return items


def load_manifest(target: Path) -> Dict[str, dict]:
    path = target / ".github/q-mentor/MANIFEST.json"
    return json.loads(path.read_text())["files"] if path.exists() else {}


def deploy(target: Path, targets: List[str], domains: List[str], dry_run: bool, force: bool) -> int:
    manifest = load_manifest(target)
    new_manifest: Dict[str, dict] = {}
    conflicts, actions = [], []
    for src, rel in plan(targets, domains):
        dest = target / rel
        digest = sha256(src)
        if dest.exists():
            current = sha256(dest)
            recorded = manifest.get(rel, {}).get("sha256")
            if current == digest:
                actions.append(("unchanged", rel))
            elif recorded == current or force:
                actions.append(("update", rel))
            else:
                conflicts.append(rel)
                continue
        else:
            actions.append(("create", rel))
        new_manifest[rel] = {"sha256": digest, "source": str(src.relative_to(ROOT))}
    for action, rel in actions:
        print(f"{action:<9} {rel}")
    for rel in conflicts:
        print(f"CONFLICT  {rel} (changed locally; use --force to replace)")
    if conflicts and not force:
        print("No files written: resolve conflicts first.")
        return 1
    if dry_run:
        print("dry run: nothing written")
        return 0
    for src, rel in plan(targets, domains):
        if rel in new_manifest:
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    manifest_path = target / ".github/q-mentor/MANIFEST.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps({"plugin": "q-mentor", "version": plugin_version(),
                                         "targets": targets, "domains": domains, "files": new_manifest},
                                        indent=2) + "\n")
    print(f"deployed {len(new_manifest)} files; manifest at {manifest_path.relative_to(target)}")
    return 0


def uninstall(target: Path, dry_run: bool) -> int:
    manifest = load_manifest(target)
    if not manifest:
        print("no manifest found; nothing to remove")
        return 1
    kept = 0
    for rel, info in manifest.items():
        dest = target / rel
        if not dest.exists():
            continue
        if sha256(dest) != info["sha256"]:
            print(f"keep      {rel} (changed locally)")
            kept += 1
            continue
        print(f"remove    {rel}")
        if not dry_run:
            dest.unlink()
    if not dry_run and not kept:
        (target / ".github/q-mentor/MANIFEST.json").unlink()
        for folder in sorted({(target / r).parent for r in manifest}, key=lambda p: -len(p.parts)):
            if folder.exists() and not any(folder.iterdir()):
                folder.rmdir()
        qm = target / ".github/q-mentor"
        if qm.exists() and not any(qm.iterdir()):
            qm.rmdir()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--targets", nargs="*", default=list(TARGET_PACKS), choices=list(TARGET_PACKS))
    parser.add_argument("--domains", nargs="*", default=["finance"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    if not args.target.is_dir():
        print(f"target is not a directory: {args.target}")
        return 1
    if args.uninstall:
        return uninstall(args.target.resolve(), args.dry_run)
    return deploy(args.target.resolve(), args.targets, args.domains, args.dry_run, args.force)


if __name__ == "__main__":
    sys.exit(main())
