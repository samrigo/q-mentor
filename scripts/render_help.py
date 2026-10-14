"""Render q-mentor-help answers from registry/skills.yml only (template `guide`).

  python scripts/render_help.py                 # best 1-3 skills for no goal -> overview
  python scripts/render_help.py --all           # every user-invocable skill, one table row each
  python scripts/render_help.py --task "convert my Pulser code to Classiq"
  python scripts/render_help.py --registry PATH # any registry file (used by tests)

There is no second, hand-maintained menu: add a skill to the registry and it appears here.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qmentor_response import render_text  # noqa: E402
from route import ROOT, select_primary  # noqa: E402


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(render_text("guide", {
            "Answer": f"The skill registry is missing, so no skill menu can be shown ({path}).",
            "When to use": "Help reads only the registry; it never guesses a menu.",
            "Next": "Reinstall the plugin or run scripts/deploy_repo_local.py to restore registry/skills.yml."},
            "blocked"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def menu_rows(registry: dict) -> list:
    rows = []
    for s in registry["skills"]:
        if not s["user_invocable"]:
            continue
        prereq = ", ".join(p.replace("q-mentor-", "") for p in s["prerequisites"]) or "none"
        rows.append(f"| `/{s['name']}` | {s['use_when']} | {prereq} | {s['output']} |")
    return rows


def render_all(registry: dict) -> str:
    rows = menu_rows(registry)
    table = "\n".join(["| skill | use when | prerequisite | output |", "|---|---|---|---|", *rows])
    return render_text("guide", {
        "Answer": f"{len(rows)} skills; state a goal and Q-Mentor chains them.\n{table}",
        "When to use": "Prerequisites run automatically.",
        "Next": "Describe your problem or paste code."}, "complete")


def render_task(registry: dict, task: str) -> str:
    by_name = {s["name"]: s for s in registry["skills"]}
    primary = select_primary(registry, task)
    if primary is None:
        return render_text("guide", {
            "Answer": "No Q-Mentor skill clearly matches that yet; start by describing the decision or code involved.",
            "When to use": "Help maps goals to skills such as learn, frame, verdict, convert, test, and review.",
            "Next": "Which outcome do you want: an explanation, a go/no-go decision, or working code?"}, "needs-input")
    chain = [p for p in by_name[primary]["prerequisites"] if p in by_name][:1] + [primary]
    lines = [f"`/{n}` - {by_name[n]['summary']} (input: "
             f"{', '.join(by_name[n]['requires'] or by_name[n].get('requires_any', [])) or 'your goal'}; "
             f"output: {by_name[n]['output']})" for n in chain]
    return render_text("guide", {
        "Answer": f"Best fit: `/{primary}`. " + " ".join(lines[-1:]),
        "When to use": f"{by_name[primary]['use_when']} Example: \"{by_name[primary]['example']}\"" +
                       (f" If needed, {lines[0]} runs first automatically." if len(chain) > 1 else ""),
        "Next": "Ask for the outcome in your own words and Q-Mentor runs these skills; no slash command needed."},
        "complete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(ROOT / "registry" / "skills.yml"))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--task")
    args = parser.parse_args()
    registry = load(Path(args.registry))
    print(render_all(registry) if args.all or not args.task else render_task(registry, args.task), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
