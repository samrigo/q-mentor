"""Deploy Q-Mentor into a repository for cloud agent / IDE agent mode.

  .github/skills/<skill>/SKILL.md      (canonical skills)
  .github/agents/q-mentor.agent.md     (custom agent)
  .github/q-mentor/...                 (registry, schemas, templates, selected knowledge and domain packs)
  .github/q-mentor/scripts/...         (help renderer, routers, response linter: same code as the plugin)
  .github/q-mentor/MANIFEST.json       (versions + SHA-256 of every copied file)

Refuses to overwrite files changed since the last deployment (unless --force), supports --dry-run, --uninstall
and --rollback (an update first saves the replaced files under .github/q-mentor/backup/<previous version>/),
never creates symlinks. Execution-target and hardware packs are selectable.
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
CORE_PACKS = ["INDEX.md", "quantum-basics.md", "optimization-math.md", "quantum-fit.md", "research-method.md",
              "recent-research.md", "pqc.md", "sources.yml", "hardware-index.md", "conversion-atlas.md"]
HARDWARE_PACKS = {
    "superconducting": "hardware-superconducting.md",
    "ions-atoms": "hardware-ions-atoms.md",
    "photonic-spin": "hardware-photonic-spin.md",
    "nmr-helium": "hardware-nmr-helium.md",
}
SCRIPTS = ["qmentor_response.py", "render_help.py", "route.py", "route_conversion.py"]
BACKUP = ".github/q-mentor/backup"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plugin_version() -> str:
    return json.loads((ROOT / "plugin.json").read_text())["version"]


def plan(targets: List[str], domains: List[str], hardware: List[str] | None = None) -> List[Tuple[Path, str]]:
    hardware = list(HARDWARE_PACKS) if hardware is None else hardware
    items: List[Tuple[Path, str]] = []
    for skill in sorted((ROOT / "skills").iterdir()):
        if (skill / "SKILL.md").exists():
            items.append((skill / "SKILL.md", f".github/skills/{skill.name}/SKILL.md"))
    items.append((ROOT / "com.github.copilot/agents/q-mentor.agent.md", ".github/agents/q-mentor.agent.md"))
    for folder in ("registry", "schemas", "templates"):
        for f in sorted(p for p in (ROOT / folder).rglob("*") if p.is_file()):
            items.append((f, f".github/q-mentor/{f.relative_to(ROOT)}"))
    for name in SCRIPTS:
        items.append((ROOT / "scripts" / name, f".github/q-mentor/scripts/{name}"))
    for name in CORE_PACKS + [TARGET_PACKS[t] for t in targets] + [HARDWARE_PACKS[h] for h in hardware]:
        items.append((ROOT / "knowledge" / name, f".github/q-mentor/knowledge/{name}"))
    for domain in domains:
        for f in sorted((ROOT / "domains" / domain).iterdir()):
            items.append((f, f".github/q-mentor/domains/{domain}/{f.name}"))
    return items


def load_manifest(target: Path) -> Dict[str, dict]:
    path = target / ".github/q-mentor/MANIFEST.json"
    return json.loads(path.read_text())["files"] if path.exists() else {}


def manifest_doc(target: Path) -> dict:
    path = target / ".github/q-mentor/MANIFEST.json"
    return json.loads(path.read_text()) if path.exists() else {}


def deploy(target: Path, targets: List[str], domains: List[str], dry_run: bool, force: bool,
           hardware: List[str] | None = None) -> int:
    manifest = load_manifest(target)
    previous = manifest_doc(target)
    new_manifest: Dict[str, dict] = {}
    conflicts, actions = [], []
    for src, rel in plan(targets, domains, hardware):
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
    if previous and previous.get("version") != plugin_version():
        backup = target / BACKUP / previous["version"]
        for rel in previous["files"]:
            if (target / rel).exists():
                (backup / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(target / rel, backup / rel)
        (backup / "MANIFEST.json").write_text(json.dumps(previous, indent=2) + "\n")
        print(f"backup    {BACKUP}/{previous['version']} ({len(previous['files'])} files)")
    for src, rel in plan(targets, domains, hardware):
        if rel in new_manifest:
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    for rel in set(manifest) - set(new_manifest):  # files the new version no longer ships
        if (target / rel).exists() and sha256(target / rel) == manifest[rel]["sha256"]:
            (target / rel).unlink()
            print(f"retire    {rel}")
    manifest_path = target / ".github/q-mentor/MANIFEST.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps({"plugin": "q-mentor", "version": plugin_version(),
                                         "targets": targets, "domains": domains,
                                         "hardware": list(HARDWARE_PACKS) if hardware is None else hardware,
                                         "files": new_manifest},
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
        if (target / BACKUP).exists():
            shutil.rmtree(target / BACKUP)
        for cache in (target / ".github/q-mentor").rglob("__pycache__"):  # created by running the copied scripts
            shutil.rmtree(cache)
        qm = target / ".github/q-mentor"
        for folder in sorted((p for p in qm.rglob("*") if p.is_dir()), key=lambda p: -len(p.parts)) if qm.exists() else []:
            if not any(folder.iterdir()):
                folder.rmdir()
        if qm.exists() and not any(qm.iterdir()):
            qm.rmdir()
    return 0


def rollback(target: Path, dry_run: bool) -> int:
    root = target / BACKUP
    versions = sorted(p.name for p in root.iterdir()) if root.exists() else []
    if not versions:
        print("no backup found; nothing to roll back")
        return 1
    version = versions[-1]
    saved = json.loads((root / version / "MANIFEST.json").read_text())
    current = load_manifest(target)
    for rel in current:
        if rel not in saved["files"] and (target / rel).exists():
            print(f"remove    {rel}")
            if not dry_run:
                (target / rel).unlink()
    for rel in saved["files"]:
        print(f"restore   {rel}")
        if not dry_run:
            (target / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / version / rel, target / rel)
    if not dry_run:
        (target / ".github/q-mentor/MANIFEST.json").write_text(json.dumps(saved, indent=2) + "\n")
        shutil.rmtree(root / version)
        if not any(root.iterdir()):
            root.rmdir()
    print(f"rolled back to {version}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--targets", nargs="*", default=list(TARGET_PACKS), choices=list(TARGET_PACKS))
    parser.add_argument("--domains", nargs="*", default=["finance"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--hardware", nargs="*", default=list(HARDWARE_PACKS), choices=list(HARDWARE_PACKS))
    args = parser.parse_args()
    if not args.target.is_dir():
        print(f"target is not a directory: {args.target}")
        return 1
    if args.uninstall:
        return uninstall(args.target.resolve(), args.dry_run)
    if args.rollback:
        return rollback(args.target.resolve(), args.dry_run)
    return deploy(args.target.resolve(), args.targets, args.domains, args.dry_run, args.force, args.hardware)


if __name__ == "__main__":
    sys.exit(main())
