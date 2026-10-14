"""Renderer and linter for qmentor.response.v3.

Template definitions are data: the YAML frontmatter of templates/responses/<id>.md.
Registry `template_id`s come from registry/skills.yml. Nothing here hard-codes a template.

  render_text(template_id, fields, status, audience="technical", mode="brief") -> str
  render_machine(template_id, fields, status, meta) -> dict
  lint_text(text, template_id, audience, mode) -> [problem codes]
  lint_machine(text, expected_template=None) -> [problem codes]
  lint_code_only(text, template_id) -> [problem codes]

CLI:
  python scripts/qmentor_response.py lint FILE --template decision [--audience business] [--mode brief]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "qmentor.response.v3"
STATUSES = ("complete", "needs-input", "blocked", "unsupported", "unverified")
ROUTE_CLASSES = ("exact", "conditional", "reimplementation", "approximate", "unsupported")
VALIDATION_STATES = ("not-applicable", "not-run", "draft", "syntax-checked", "imported", "locally-executed",
                     "target-validated", "unverified", "failed")

PRAISE = re.compile(r"\b(great question|excellent question|good question|happy to help|i hope this helps|"
                    r"hope this helps|absolutely!|certainly!|glad you asked)", re.I)
NARRATION = re.compile(r"\b(let me (walk|start|first|now|explain)|i first (read|loaded|ran)|then i (loaded|read|ran)|"
                       r"i will now|here's what i did|i('ve| have) (analy[sz]ed|reviewed) your)\b", re.I)
CONCLUSION = re.compile(r"\b(in summary|to summari[sz]e|in conclusion|to conclude|overall, )", re.I)
VAGUE = re.compile(r"\b(let me know|feel free|happy to|if you have any (other )?questions)\b", re.I)
ADVANTAGE = re.compile(r"[^.\n]*\b(quantum advantage|quantum speed-?up|outperforms classical|faster than classical|"
                       r"beats classical)\b[^.\n]*", re.I)
NEGATION = re.compile(r"\b(not|no|never|without|isn't|is not|cannot|unsupported|unproven|does not|doesn't)\b", re.I)
OPTIMIZED = re.compile(r"(?<![-\w])(?<!not )(?<!un)optimi[sz]ed\b", re.I)
PLACEHOLDER = re.compile(r"^\s*\.\.\.\s*$|^\s*#\s*\.\.\.|\bTODO\b|\bFIXME\b|<your[- _]|\bpass\s+#\s*implement", re.M)
SOURCE_MARK = re.compile(r"(https?://|doi\.org|arXiv|\bdoi:|`[a-z0-9]+(-[a-z0-9]+)+`|\b(rr|sdk|hw|ref)-[a-z0-9-]+)", re.I)
SOURCE_TYPE = re.compile(r"\b(peer-reviewed|preprint|vendor documentation|vendor result|commentary|official doc|"
                         r"repository|local computation|standard)\b", re.I)
URL = re.compile(r"https?://\S+")
ACRONYMS = {
    "QUBO": r"quadratic unconstrained binary optimi[sz]ation",
    "QAOA": r"quantum approximate optimi[sz]ation",
    "BQM": r"binary quadratic model",
    "CVaR": r"conditional value[- ]at[- ]risk",
    "PQC": r"post-quantum",
    "QPU": r"quantum process(ing unit|or)",
    "AHS": r"analog hamiltonian simulation",
    "VQE": r"variational quantum eigensolver",
}


# --------------------------------------------------------------------------- templates


@lru_cache(maxsize=None)
def templates() -> Dict[str, dict]:
    out = {}
    for path in sorted((ROOT / "templates" / "responses").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            raise ValueError(f"{path}: missing frontmatter")
        spec = yaml.safe_load(m.group(1))
        spec["path"] = str(path.relative_to(ROOT))
        out[spec["id"]] = spec
    return out


def labels(template_id: str) -> List[str]:
    spec = templates()[template_id]
    return [spec["lead"], *spec["fields"]]


@lru_cache(maxsize=None)
def registry_templates() -> Dict[str, str]:
    reg = yaml.safe_load((ROOT / "registry" / "skills.yml").read_text())
    return {s["name"]: s.get("template_id") for s in reg["skills"]}


# --------------------------------------------------------------------------- render


def render_text(template_id: str, fields: Dict[str, str], status: str, audience: str = "technical",
                mode: str = "brief", appendix: str = "") -> str:
    spec = templates()[template_id]
    if status not in STATUSES:
        raise ValueError(f"bad status {status}")
    blocks = []
    order = labels(template_id)
    for label in order:
        if label not in fields:
            if label in spec.get("optional", []):
                continue
            raise ValueError(f"{template_id}: missing field {label}")
        blocks.append(f"**{label}:** {fields[label].strip()}")
        if label == spec["lead"]:
            blocks.append(f"Status: {status}")
    text = "\n\n".join(blocks)
    if appendix:
        text += "\n\n" + appendix.strip()
    return text + "\n"


def _artifacts(value: str) -> List[str]:
    if not value or value.strip().lower().startswith("none"):
        return []
    ticks = re.findall(r"`([^`]+)`", value)
    items = ticks or [v.strip() for v in re.split(r"[,;]", value) if v.strip()]
    return [i for i in items if "/" in i or "." in i]


def render_machine(template_id: str, fields: Dict[str, str], status: str, *, audience: str,
                   skills_used: List[str], validation_state: str, next_action: Optional[str] = None) -> dict:
    spec = templates()[template_id]
    out = {"contract_version": CONTRACT, "status": status, "mode": "machine", "template_id": template_id,
           "audience": audience, "result": "", "evidence": [], "uncertainty": [],
           "validation": {"state": validation_state, "detail": ""}, "artifacts": [],
           "skills_used": skills_used, "next_action": next_action or ""}
    for label in labels(template_id):
        if label not in fields:
            continue
        key, value = spec["machine"][label], fields[label].strip()
        if key == "result":
            out["result"] = value
        elif key in ("evidence", "uncertainty"):
            out[key].append(f"{label}: {value}")
        elif key == "validation":
            out["validation"]["detail"] = value
        elif key == "artifacts":
            out["artifacts"] = _artifacts(value)
            out["evidence"].append(f"{label}: {value}")
        elif key == "next_action":
            out["next_action"] = value
    if not out["next_action"]:
        raise ValueError(f"{template_id}: next_action required (pass next_action=...)")
    return out


def render_code_only(template_id: str, status: str, files: List[str], checks: str, next_action: str,
                     code: Dict[str, Tuple[str, str]]) -> str:
    manifest = (f"# {CONTRACT} template={template_id} status={status}\n# files: {', '.join(files)}\n"
                f"# checks: {checks}\n# next: {next_action}")
    parts = [f"```text\n{manifest}\n```"]
    for path, (lang, body) in code.items():
        parts.append(f"```{lang}\n# {path}\n{body.rstrip()}\n```")
    return "\n\n".join(parts) + "\n"


# --------------------------------------------------------------------------- parse


FIELD_LINE = re.compile(r"^\s*(?:[-*]\s+)?\*{0,2}([A-Z][A-Za-z /]+?)\*{0,2}\s*:\*{0,2}\s*(.*)$")


def parse(text: str, template_id: str) -> Tuple[List[Tuple[str, str]], List[str], List[str]]:
    """Return ([(label, prose)], [code blocks], [stray lines before the first field]).

    Markdown headings outside code are collected as stray entries prefixed with '#'."""
    known = set(labels(template_id)) | {"Status"}
    entries: List[Tuple[str, str]] = []
    code: List[str] = []
    stray: List[str] = []
    in_code = False
    buf: List[str] = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_code:
                code.append("\n".join(buf))
                buf = []
            in_code = not in_code
            continue
        if in_code:
            buf.append(line)
            continue
        if re.match(r"^\s*#{1,6}\s", line):
            stray.append("#heading " + line.strip())
            continue
        m = FIELD_LINE.match(line)
        if m and m.group(1).strip() in known:
            entries.append((m.group(1).strip(), m.group(2).strip()))
        elif line.strip():
            if entries:
                label, value = entries[-1]
                entries[-1] = (label, (value + "\n" + line.strip()).strip())
            else:
                stray.append(line.strip())
    if in_code:
        code.append("\n".join(buf) + "\n<<UNCLOSED>>")
    return entries, code, stray


def _prose_words(value: str) -> int:
    lines = [ln for ln in value.splitlines() if not ln.strip().startswith("|")]
    joined = URL.sub("", " ".join(lines))
    joined = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", joined)
    return len(joined.split())


# --------------------------------------------------------------------------- lint


def lint_text(text: str, template_id: str, audience: str = "technical", mode: str = "brief") -> List[str]:
    spec = templates()[template_id]
    problems: List[str] = []
    entries, code, stray = parse(text, template_id)
    headings = [s for s in stray if s.startswith("#heading ")]
    stray = [s for s in stray if not s.startswith("#heading ")]
    if stray:
        problems.append("lead-first")
    if headings:
        problems.append("unstable-heading")
    if not entries:
        return ["lead-first", "no-fields"]
    seq = [label for label, _ in entries]
    values = dict()
    for label, value in entries:
        values.setdefault(label, value)
    if seq[0] != spec["lead"]:
        problems.append("lead-first")
    if len(seq) < 2 or seq[1] != "Status":
        problems.append("status-line")
    if seq.count("Status") != 1:
        problems.append("status-line")
    status = values.get("Status", "").strip().strip("`*")
    if status not in STATUSES:
        problems.append("status-enum")
    body = [s for s in seq if s != "Status"]
    order = labels(template_id)
    expected_once = [lbl for lbl in order if lbl in values or lbl not in spec.get("optional", [])]
    if spec.get("repeatable"):
        reps = len(body) // len(expected_once) if expected_once else 0
        if reps < 1 or body != expected_once * reps:
            problems.append("field-order")
        if reps > spec.get("max_repeats", 1):
            problems.append("too-many-findings")
    elif body != expected_once:
        problems.append("field-order")
    for label, value in entries:
        if not value.strip():
            problems.append("empty-field")
    prose = "\n".join(v for _, v in entries)
    prose_all = "\n".join(stray + [prose])
    words = sum(_prose_words(v) for lbl, v in entries if lbl != "Status")
    cap = spec["cap_words"]
    table_rows = [ln for ln in prose.splitlines() if ln.strip().startswith("|") and not set(ln.strip()) <= set("|-: ")]
    if template_id == "guide" and table_rows:
        total = len(" ".join(v for _, v in entries).split())
        if len(table_rows) - 1 > 20 or total > spec.get("full_menu_cap_words", cap):
            problems.append("too-long")
    elif words > (cap * 3 if mode == "detailed" else cap):
        problems.append("too-long")
    if PRAISE.search(prose_all) or NARRATION.search(prose_all):
        problems.append("praise-or-narration")
    if CONCLUSION.search(prose):
        problems.append("repeated-conclusion")
    sentences = [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+|\n+", prose) if len(s.split()) >= 5]
    if len(sentences) != len(set(sentences)):
        problems.append("duplicate-sentence")
    for match in ADVANTAGE.finditer(prose):
        if not NEGATION.search(match.group(0)):
            problems.append("unsupported-advantage")
            break
    if OPTIMIZED.search(prose):
        opt = values.get("Optimization", "")
        if template_id != "conversion" or "improved" not in opt.lower() or "not improved" in opt.lower() \
                or "not-improved" in opt.lower() or not re.search(r"(?i)optimi[sz]ation[_ -]?record", text):
            problems.append("unsupported-optimized-claim")
    for block in code:
        if "<<UNCLOSED>>" in block:
            problems.append("truncated-code")
        if PLACEHOLDER.search(block):
            problems.append("placeholder-code")
    if len(URL.findall(prose)) > 3:
        problems.append("too-many-citations")
    last_label = expected_once[-1] if expected_once else ""
    last = values.get(last_label, "")
    if VAGUE.search(prose):
        problems.append("vague-next")
    if status == "needs-input":
        q_total = prose.count("?")
        q_ok = "?" in values.get(spec["lead"], "") or "?" in last
        if q_total != 1 or not q_ok:
            problems.append("needs-one-question")
    gate = values.get("Validation", "") if template_id == "conversion" else last
    if status == "blocked" and len(gate.split()) < 3:
        problems.append("blocked-without-gate")
    # template-specific obligations
    if template_id in ("conversion", "mapping"):
        route = values.get("Route", "")
        if not any(c in route.lower() for c in ROUTE_CLASSES):
            problems.append("route-class-missing")
    if template_id == "code" and status == "complete":
        if not re.search(r"(?i)\b(\d+ passed|passed|failed|locally-executed|imported|syntax-checked|target-validated)\b",
                         values.get("Checks", "")):
            problems.append("checks-not-observed")
    if template_id == "conversion" and status == "complete":
        if not re.search(r"(?i)\b(passed|locally-executed|imported|syntax-checked|target-validated)\b",
                         values.get("Validation", "")):
            problems.append("checks-not-observed")
    if template_id in ("decision", "options") and status in ("complete", "unverified"):
        if not re.search(r"(?i)classical", prose):
            problems.append("no-classical-baseline")
    if template_id == "evidence" and status == "complete":
        ev = values.get("Evidence", "")
        if not SOURCE_MARK.search(ev) or not SOURCE_TYPE.search(ev):
            problems.append("evidence-without-source")
    if template_id == "review":
        for label, value in entries:
            if label == "Finding" and not re.match(r"(?i)(\[(critical|high|medium|low|info)\]|no findings)", value):
                problems.append("finding-without-severity")
                break
    if audience == "business":
        for acro, expansion in ACRONYMS.items():
            if re.search(rf"\b{acro}\b", prose) and not re.search(expansion, prose, re.I):
                problems.append("business-jargon")
                break
    return sorted(set(problems))


def lint_machine(text: str, expected_template: Optional[str] = None) -> List[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return ["invalid-json"]
    schema = json.loads((ROOT / "schemas" / "response-v3.schema.json").read_text())
    problems = []
    if list(Draft202012Validator(schema).iter_errors(data)):
        problems.append("schema")
        return problems
    if expected_template and data["template_id"] != expected_template:
        problems.append("template-mismatch")
    terminal = data["skills_used"][-1]
    reg = registry_templates()
    if terminal not in reg:
        problems.append("unknown-skill")
    elif reg[terminal] != data["template_id"]:
        problems.append("template-mismatch")
    flat = " ".join([data["result"], *data["evidence"], *data["uncertainty"], data["next_action"]])
    if PRAISE.search(flat) or NARRATION.search(flat):
        problems.append("praise-or-narration")
    for match in ADVANTAGE.finditer(flat):
        if not NEGATION.search(match.group(0)):
            problems.append("unsupported-advantage")
            break
    if data["status"] == "complete" and data["template_id"] in ("code", "conversion") and \
            data["validation"]["state"] in ("not-run", "draft", "unverified", "failed"):
        problems.append("checks-not-observed")
    return sorted(set(problems))


def lint_code_only(text: str, template_id: str) -> List[str]:
    problems = []
    outside, inside, blocks, buf = [], False, [], []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if inside:
                blocks.append("\n".join(buf))
                buf = []
            inside = not inside
            continue
        (buf if inside else outside).append(line)
    if inside:
        problems.append("truncated-code")
    if any(ln.strip() for ln in outside):
        problems.append("prose-in-code-only")
    if not blocks or not re.search(rf"{CONTRACT} template={template_id} status=({'|'.join(STATUSES)})", blocks[0]):
        problems.append("manifest-missing")
    elif not all(k in blocks[0] for k in ("# files:", "# checks:", "# next:")):
        problems.append("manifest-missing")
    for block in blocks[1:]:
        if PLACEHOLDER.search(block):
            problems.append("placeholder-code")
    return sorted(set(problems))


def lint(text: str, template_id: str, audience: str = "technical", mode: str = "brief") -> List[str]:
    if mode == "machine":
        return lint_machine(text, template_id)
    if mode == "code-only":
        return lint_code_only(text, template_id)
    return lint_text(text, template_id, audience, mode)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lint")
    p.add_argument("file")
    p.add_argument("--template", required=True, choices=sorted(templates()))
    p.add_argument("--audience", default="technical", choices=["business", "technical"])
    p.add_argument("--mode", default="brief", choices=["brief", "detailed", "machine", "code-only"])
    args = parser.parse_args()
    problems = lint(Path(args.file).read_text(encoding="utf-8"), args.template, args.audience, args.mode)
    print("OK" if not problems else " ".join(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
