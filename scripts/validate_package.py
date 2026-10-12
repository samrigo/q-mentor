#!/usr/bin/env python3
"""Validate the Agent Plugins package: manifest, agent, skills, packs, sources, schemas, secrets.

    python scripts/validate_package.py [--root PATH]

Exit code 0 only when every check passes. Rules mirror the Agent Plugins 1.0
schema (https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and the
GitHub Copilot skill and plugin references, as verified on 2026-10-12.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

SCHEMA_URLS = {
    "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "https://agent-plugins.org/schemas/1.1.0/plugin.schema.json",
}
MANIFEST_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository",
                 "license", "keywords", "extensions"}
AUTHOR_KEYS = {"name", "email", "url"}
NAME_RE = re.compile(r"^(?!.*--)(?!.*\.\.)[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
EXPECTED_SKILLS = {f"q-mentor-{s}" for s in (
    "learn research brainstorm frame verdict design translate evaluate implement test review pqc-scan exec improve"
).split()}
MAX_SKILL_LINES = 120
MAX_PACK_TOKENS = 1000
SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\n[A-Za-z0-9+/=]{40,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{24,}['\"]"),
]


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    _, fm, body = text.split("---\n", 2)
    return yaml.safe_load(fm) or {}, body


def approx_tokens(text: str) -> int:
    return max(len(text) // 4, int(len(text.split()) * 1.3))


def check(root: Path) -> list[str]:
    errs: list[str] = []
    e = errs.append

    # Manifest -------------------------------------------------------------
    mpath = root / "plugin.json"
    if not mpath.exists():
        return ["plugin.json missing at plugin root"]
    m = json.loads(mpath.read_text())
    if m.get("$schema") not in SCHEMA_URLS:
        e(f"plugin.json: $schema must be one of {sorted(SCHEMA_URLS)}")
    if not isinstance(m.get("name"), str) or not NAME_RE.match(m["name"]):
        e("plugin.json: invalid name")
    extra = set(m) - MANIFEST_KEYS
    if extra:
        e(f"plugin.json: unknown top-level keys {sorted(extra)}")
    if "author" in m and (not isinstance(m["author"], dict) or set(m["author"]) - AUTHOR_KEYS):
        e("plugin.json: author must be an object with name/email/url only")
    if "keywords" in m and not all(isinstance(k, str) for k in m["keywords"]):
        e("plugin.json: keywords must be strings")
    if "version" in m and not re.match(r"^\d+\.\d+\.\d+", m["version"]):
        e("plugin.json: version should be semver")
    mk = root / ".github" / "plugin" / "marketplace.json"
    if mk.exists():
        mj = json.loads(mk.read_text())
        entry = next((pl for pl in mj.get("plugins", []) if pl.get("name") == m.get("name")), None)
        if not entry:
            e("marketplace.json: no entry for this plugin")
        elif entry.get("version") != m.get("version"):
            e("marketplace.json: version differs from plugin.json")
    changelog = root / "CHANGELOG.md"
    if changelog.exists() and m.get("version") and f"[{m['version']}]" not in changelog.read_text():
        e(f"CHANGELOG.md has no entry for version {m['version']}")

    # Agent ----------------------------------------------------------------
    agents = list((root / "com.github.copilot" / "agents").glob("*.agent.md"))
    if not agents:
        e("no Copilot agent under com.github.copilot/agents/")
    for a in agents:
        fm, body = frontmatter(a)
        for k in ("name", "description"):
            if not fm.get(k):
                e(f"{a.name}: frontmatter '{k}' missing")
        if not isinstance(fm.get("tools", []), list):
            e(f"{a.name}: tools must be a list")
        for s in EXPECTED_SKILLS:
            if f"`{s}`" not in body:
                e(f"{a.name}: does not route to {s}")
        if re.search(r"\]\(\.\./\.\./knowledge", body):
            e(f"{a.name}: agent must not link knowledge packs (router only)")

    # Skills ---------------------------------------------------------------
    sdir = root / "skills"
    found = {d.name for d in sdir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()} if sdir.exists() else set()
    if found != EXPECTED_SKILLS:
        e(f"skills mismatch: missing {sorted(EXPECTED_SKILLS - found)}, unexpected {sorted(found - EXPECTED_SKILLS)}")
    for name in sorted(found):
        p = sdir / name / "SKILL.md"
        fm, body = frontmatter(p)
        if fm.get("name") != name:
            e(f"{name}: frontmatter name '{fm.get('name')}' != directory")
        if not SKILL_NAME_RE.match(str(fm.get("name", ""))):
            e(f"{name}: name must be lowercase with hyphens")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            e(f"{name}: description missing or > 1024 chars")
        if "allowed-tools" in fm and re.search(r"\b(shell|bash)\b", str(fm["allowed-tools"])):
            e(f"{name}: must not pre-approve shell/bash")
        lines = p.read_text().count("\n")
        if lines > MAX_SKILL_LINES:
            e(f"{name}: {lines} lines > {MAX_SKILL_LINES}")
        for section in ("## Output contract", "## Stop conditions", "## Always"):
            if section not in body:
                e(f"{name}: missing section '{section}'")
        packs = set()
        for link in LINK_RE.findall(body):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            target = (p.parent / link).resolve()
            if not target.exists():
                e(f"{name}: broken link {link}")
            rel = target.relative_to(root.resolve()).as_posix() if target.is_relative_to(root.resolve()) else link
            if rel.startswith(("knowledge/", "domains/")) and not rel.endswith("INDEX.md"):
                packs.add(rel)
        if len(packs) > 3:
            e(f"{name}: links {len(packs)} knowledge packs (> 3): {sorted(packs)}")

    # Knowledge packs and sources -----------------------------------------
    reg = yaml.safe_load((root / "knowledge" / "sources.yml").read_text())["sources"]
    ids = set()
    for s in reg:
        for k in ("id", "title", "url", "owner", "status", "last_verified"):
            if not s.get(k):
                e(f"sources.yml: {s.get('id', '?')} missing {k}")
        if s.get("status") not in {"peer-reviewed", "preprint", "official-documentation", "vendor-result", "secondary"}:
            e(f"sources.yml: {s.get('id')} has invalid status")
        if not str(s.get("url", "")).startswith("https://"):
            e(f"sources.yml: {s.get('id')} url must be https")
        if s.get("id") in ids:
            e(f"sources.yml: duplicate id {s['id']}")
        ids.add(s.get("id"))
    for pack in sorted(list((root / "knowledge").glob("*.md")) + list((root / "domains").rglob("*.md"))):
        text = pack.read_text()
        rel = pack.relative_to(root)
        if approx_tokens(text) > MAX_PACK_TOKENS:
            e(f"{rel}: ~{approx_tokens(text)} tokens > {MAX_PACK_TOKENS}")
        if pack.name != "INDEX.md":
            if "last_verified:" not in text:
                e(f"{rel}: missing last_verified")
            if "## Operational rule" not in text:
                e(f"{rel}: must lead with '## Operational rule'")
            cited = re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text.split("\n", 3)[2] if text.count("\n") > 2 else "")
            for cid in cited:
                if cid not in ids:
                    e(f"{rel}: cites unknown source id {cid}")
        for link in LINK_RE.findall(text):
            if not link.startswith("http") and not (pack.parent / link).resolve().exists():
                e(f"{rel}: broken link {link}")

    # Templates and schemas ------------------------------------------------
    for t in ("frame", "verdict", "provider-design", "evidence-card", "experiment-record",
              "conversation-lesson", "executive-brief"):
        if not (root / "templates" / f"{t}.md").exists():
            e(f"templates/{t}.md missing")
    try:
        import jsonschema
        for sch in (root / "schemas").glob("*.json"):
            jsonschema.Draft202012Validator.check_schema(json.loads(sch.read_text()))
        ps = json.loads((root / "schemas" / "problem-spec.schema.json").read_text())
        jsonschema.validate(json.loads((root / "demo/bond-selection/problem.json").read_text()), ps)
    except ImportError:
        e("jsonschema not installed: pip install -e .[dev]")
    except Exception as exc:  # noqa: BLE001
        e(f"schema check failed: {exc}")

    # Repository-wide instructions stay small ------------------------------
    ci = root / ".github" / "copilot-instructions.md"
    if ci.exists() and ci.read_text().count("\n") > 40:
        e(".github/copilot-instructions.md should stay under 40 lines (domain detail belongs in skills)")

    # Secret scan ----------------------------------------------------------
    for f in root.rglob("*"):
        if not f.is_file() or any(p in f.parts for p in (".git", "__pycache__", ".pytest_cache")):
            continue
        if f.suffix not in {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".cfg", ".ini", ""}:
            continue
        text = f.read_text(errors="ignore")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                e(f"possible secret in {f.relative_to(root)} ({pat.pattern[:30]}...)")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    root = Path(ap.parse_args().root).resolve()
    errs = check(root)
    for err in errs:
        print(f"FAIL  {err}")
    n_skills = len([d for d in (root / "skills").iterdir() if (d / "SKILL.md").exists()])
    print(f"{'OK' if not errs else 'FAILED'}: plugin '{json.loads((root / 'plugin.json').read_text())['name']}', "
          f"{n_skills} skills, {len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
