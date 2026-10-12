#!/usr/bin/env python3
"""Copy skills into a repository-local .github/skills/ layout for IDE agent modes."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy Q-Mentor skills repository-locally")
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd() / ".github" / "skills",
        help="Destination directory (default: ./.github/skills)",
    )
    args = parser.parse_args()

    src = ROOT / "skills"
    dest = args.target
    dest.mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(src.iterdir()):
        if not skill_dir.is_dir():
            continue
        target = dest / skill_dir.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill_dir, target)
        print(f"  deployed {skill_dir.name}")

    print(f"deploy_repo_local: skills written to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
