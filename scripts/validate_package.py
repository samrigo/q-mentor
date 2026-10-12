#!/usr/bin/env python3
"""Validate Agent Plugins 1.0 package structure and skill frontmatter."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILLS = [
    "q-mentor-learn",
    "q-mentor-research",
    "q-mentor-brainstorm",
    "q-mentor-frame",
    "q-mentor-verdict",
    "q-mentor-design",
    "q-mentor-translate",
    "q-mentor-evaluate",
    "q-mentor-implement",
    "q-mentor-test",
    "q-mentor-review",
    "q-mentor-pqc-scan",
    "q-mentor-exec",
    "q-mentor-improve",
]


def main() -> int:
    errors: list[str] = []

    manifest_path = ROOT / "plugin.json"
    if not manifest_path.is_file():
        errors.append("missing plugin.json")
    else:
        data = json.loads(manifest_path.read_text())
        if data.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("plugin.json $schema incorrect")
        if data.get("name") != "q-mentor":
            errors.append("plugin.json name must be q-mentor")

    agent = ROOT / "com.github.copilot" / "agents" / "q-mentor.agent.md"
    if not agent.is_file():
        errors.append("missing com.github.copilot/agents/q-mentor.agent.md")

    skills_dir = ROOT / "skills"
    for name in REQUIRED_SKILLS:
        skill_md = skills_dir / name / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"missing skills/{name}/SKILL.md")
            continue
        text = skill_md.read_text()
        if not text.startswith("---"):
            errors.append(f"{name}: missing frontmatter")
            continue
        m = re.search(r"^name:\s*(\S+)", text, re.M)
        if not m or m.group(1) != name:
            errors.append(f"{name}: frontmatter name mismatch")

    if errors:
        print("validate_package: FAIL")
        for e in errors:
            print(" ", e)
        return 1

    print("validate_package: PASS")
    print(f"  skills discovered: {len(REQUIRED_SKILLS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
