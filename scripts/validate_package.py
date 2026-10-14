"""Package gate: manifest, agent, skills, registry graph, schemas, artifacts, packs, coverage, PQC fixtures."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
errors: list = []

# Lifecycle coverage (README-08): skill -> schema or template that holds its durable output
# (in addition to its mandatory response template from the registry).
COVERAGE = {
    "q-mentor-orchestrate": "registry/skills.yml",
    "q-mentor-help": "scripts/render_help.py",
    "q-mentor-learn": "knowledge/INDEX.md",
    "q-mentor-research": "templates/evidence-card.md",
    "q-mentor-brainstorm": "templates/responses/options.md",
    "q-mentor-frame": "schemas/canonical-problem.schema.json",
    "q-mentor-verdict": "templates/verdict.md",
    "q-mentor-design": "templates/provider-design.md",
    "q-mentor-translate": "schemas/translation-record.schema.json",
    "q-mentor-convert": "schemas/optimization-record.schema.json",
    "q-mentor-evaluate": "templates/experiment-record.md",
    "q-mentor-implement": "examples/README.md",
    "q-mentor-test": "schemas/result-record.schema.json",
    "q-mentor-review": "templates/responses/review.md",
    "q-mentor-pqc-scan": "knowledge/pqc.md",
    "q-mentor-exec": "templates/executive-brief.md",
    "q-mentor-improve": "templates/conversation-lesson.md",
}
MANDATORY = ("For **every** user-facing answer, including clarification, error, and direct invocation, render "
             "`templates/responses/{tid}.md` through `qmentor.response.v3`; preserve its lead, field order, status, "
             "uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.")
FORBIDDEN_TOOLS = {"shell", "bash", "execute", "powershell", "*"}
PATH_REF = re.compile(r"`((?:registry|schemas|templates|knowledge|domains|examples|scripts|evals|demo)/[A-Za-z0-9_./-]+)`")


def err(msg: str) -> None:
    errors.append(msg)


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        err(f"{path}: missing YAML frontmatter")
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def check_manifest(live: bool) -> None:
    manifest = json.loads((ROOT / "plugin.json").read_text())
    schema_path = ROOT / "schemas/vendor/agent-plugins-1.0.0.plugin.schema.json"
    schema = json.loads(schema_path.read_text())
    if live:
        with urllib.request.urlopen(manifest["$schema"], timeout=20) as resp:
            schema = json.loads(resp.read())
    for e in Draft202012Validator(schema).iter_errors(manifest):
        err(f"plugin.json: {e.message}")
    for legacy in ("skills", "agents", "hooks", "mcpServers", "commands"):
        if legacy in manifest:
            err(f"plugin.json: legacy component field {legacy!r} not allowed with Agent Plugins")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        err("plugin.json: version must be semver")


def check_agent() -> None:
    agents = list((ROOT / "com.github.copilot" / "agents").glob("*.agent.md"))
    if len(agents) != 1:
        err(f"expected exactly one agent, found {len(agents)}")
    for agent in agents:
        fm, body = frontmatter(agent)
        if not fm.get("description"):
            err(f"{agent.name}: description required")
        tools = fm.get("tools")
        if not isinstance(tools, list) or "*" in tools:
            err(f"{agent.name}: tools must be an explicit list")
        if "registry/skills.yml" not in body:
            err(f"{agent.name}: agent must consult the registry")


def check_skills(registry: dict) -> None:
    reg = {s["name"]: s for s in registry["skills"]}
    dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    names = [d.name for d in dirs]
    if sorted(names) != sorted(reg):
        err(f"skill dirs {names} != registry {sorted(reg)}")
    for d in dirs:
        path = d / "SKILL.md"
        if not path.exists():
            err(f"{d.name}: missing SKILL.md")
            continue
        fm, body = frontmatter(path)
        lines = path.read_text().count("\n")
        if fm.get("name") != d.name:
            err(f"{d.name}: frontmatter name {fm.get('name')!r} != directory")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", d.name):
            err(f"{d.name}: invalid skill name")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            err(f"{d.name}: description missing or > 1024 chars")
        if lines >= 120:
            err(f"{d.name}: {lines} lines (limit 120)")
        tools = {t.strip() for t in str(fm.get("allowed-tools", "")).split(",") if t.strip()}
        if tools & FORBIDDEN_TOOLS:
            err(f"{d.name}: allowed-tools pre-approves {tools & FORBIDDEN_TOOLS}")
        spec = reg.get(d.name, {})
        if spec.get("side_effects") == "none" and tools & {"edit", "write"}:
            err(f"{d.name}: read-only skill pre-approves edit")
        if "web" in tools and d.name != "q-mentor-research":
            err(f"{d.name}: only q-mentor-research may use web")
        if (fm.get("user-invocable") is False) != (spec.get("user_invocable") is False):
            err(f"{d.name}: user-invocable mismatch with registry")
        for section in ("## Response template", "## Input", "## Output", "## Procedure", "## Stop when", "## Handoffs", "## Shared files"):
            if section not in body:
                err(f"{d.name}: missing section {section}")
        refs = set(PATH_REF.findall(body))
        for ref in refs:
            if not (ROOT / ref).exists() and "*" not in ref and "<" not in ref:
                err(f"{d.name}: broken reference {ref}")
        packs = {r for r in refs if r.startswith(("knowledge/", "domains/")) and r.endswith(".md")
                 and r not in ("knowledge/INDEX.md",)}
        if len(packs) > 3:
            err(f"{d.name}: links {len(packs)} packs (max 3)")
        if not packs <= set(spec.get("packs", [])):
            err(f"{d.name}: packs {packs - set(spec.get('packs', []))} not declared in registry")
        if "templates/response-contract.md" not in body:
            err(f"{d.name}: must link the response contract")
        tid = spec.get("template_id")
        if tid:
            if MANDATORY.format(tid=tid) not in body:
                err(f"{d.name}: missing the mandatory template instruction for {tid!r}")
            if f"## Response template: `{tid}`" not in body:
                err(f"{d.name}: Response template section must name {tid!r}")
        elif spec:
            if "## Response template: none (internal)" not in body:
                err(f"{d.name}: internal skill must declare no template")
        if d.name in ("q-mentor-orchestrate", "q-mentor-help") and fm.get("disable-model-invocation") is not False:
            err(f"{d.name}: must set disable-model-invocation: false")


def check_templates(registry: dict) -> None:
    from qmentor_response import templates
    tpl = templates()
    want = {"guide", "options", "evidence", "frame", "decision", "design", "mapping", "evaluation", "conversion",
            "code", "review", "improvement"}
    if set(tpl) != want:
        err(f"templates/responses: expected {sorted(want)}, found {sorted(tpl)}")
    used = set()
    for s in registry["skills"]:
        tid = s["template_id"]
        if s["user_invocable"] and not tid:
            err(f"registry: user-facing skill {s['name']} has no template_id")
        if tid:
            used.add(tid)
            if tid not in tpl:
                err(f"registry: {s['name']} template {tid} has no file")
            elif s["name"] not in tpl[tid]["skills"]:
                err(f"templates/responses/{tid}.md does not list {s['name']}")
    for tid, spec in tpl.items():
        for name in spec["skills"]:
            owner = next((x for x in registry["skills"] if x["name"] == name), None)
            if not owner or owner["template_id"] != tid:
                err(f"templates/responses/{tid}.md lists {name}, but the registry assigns {owner and owner['template_id']}")
        for key in ("lead", "fields", "cap_words", "machine", "must_carry", "contract"):
            if key not in spec:
                err(f"templates/responses/{tid}.md: frontmatter missing {key}")
        if spec.get("contract") != "qmentor.response.v3":
            err(f"templates/responses/{tid}.md: contract must be qmentor.response.v3")
        if set(spec.get("machine", {})) != {spec["lead"], *spec["fields"]}:
            err(f"templates/responses/{tid}.md: machine map must cover every field")
    if used != want:
        err(f"templates not assigned to any skill: {sorted(want - used)}")


def check_help(registry: dict) -> None:
    """Every user-invocable skill appears exactly once; a newly added skill appears without editing help."""
    import copy
    import tempfile
    import subprocess
    reg_path = ROOT / "registry" / "skills.yml"
    out = subprocess.run([sys.executable, str(ROOT / "scripts/render_help.py"), "--all", "--registry", str(reg_path)],
                         capture_output=True, text=True, check=False).stdout
    for s in registry["skills"]:
        n = out.count(f"`/{s['name']}`")
        if s["user_invocable"] and n != 1:
            err(f"help: {s['name']} appears {n} times")
        if not s["user_invocable"] and n:
            err(f"help: internal skill {s['name']} is listed")
    extra = copy.deepcopy(registry)
    new = copy.deepcopy(next(s for s in registry["skills"] if s["name"] == "q-mentor-learn"))
    new.update(name="q-mentor-zz-probe", summary="Probe skill added only by the help test.")
    extra["skills"].append(new)
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as handle:
        yaml.safe_dump(extra, handle)
    out2 = subprocess.run([sys.executable, str(ROOT / "scripts/render_help.py"), "--all", "--registry", handle.name],
                          capture_output=True, text=True, check=False).stdout
    Path(handle.name).unlink()
    if out2.count("`/q-mentor-zz-probe`") != 1:
        err("help: a newly registered skill does not appear automatically")
    from qmentor_response import lint_text
    problems = lint_text(out, "guide", "business")
    if problems:
        err(f"help: full menu violates the guide template: {problems}")


def check_registry() -> dict:
    registry = yaml.safe_load((ROOT / "registry/skills.yml").read_text())
    schema = json.loads((ROOT / "schemas/skill-registry.schema.json").read_text())
    for e in Draft202012Validator(schema).iter_errors(registry):
        err(f"registry: {e.message}")
    names = [s["name"] for s in registry["skills"]]
    if len(names) != len(set(names)):
        err("registry: duplicate skill")
    known = set(names)
    produced = {a for s in registry["skills"] for a in s["produces"]}
    supplied = set(registry["user_supplied_artifacts"]) | {"ConsentRecord"}
    graph = {}
    for s in registry["skills"]:
        for ref in s["prerequisites"] + s["follow_ons"]:
            if ref not in known:
                err(f"registry: {s['name']} references unknown skill {ref}")
        if len(s["follow_ons"]) != len(set(s["follow_ons"])) or len(s["prerequisites"]) != len(set(s["prerequisites"])):
            err(f"registry: duplicate edge in {s['name']}")
        for art in s["requires"] + s.get("requires_any", []):
            if art not in produced and art not in supplied:
                err(f"registry: {s['name']} requires {art}, which no skill produces")
        for pack in s["packs"]:
            if not (ROOT / pack).exists():
                err(f"registry: {s['name']} pack missing {pack}")
        graph[s["name"]] = s["prerequisites"]
    check_templates(registry)
    state = {}

    def visit(node, stack):
        if state.get(node) == 1:
            err(f"registry: prerequisite cycle {' -> '.join(stack + [node])}")
            return 0
        if state.get(node) == 2:
            return depth[node]
        state[node] = 1
        d = 1 + max([visit(p, stack + [node]) for p in graph.get(node, [])] or [0])
        state[node] = 2
        depth[node] = d
        return d

    depth: dict = {}
    for n in graph:
        if visit(n, []) > registry["max_chain_depth"]:
            err(f"registry: prerequisite depth of {n} exceeds max_chain_depth")
    return registry


def check_schemas_and_artifacts() -> None:
    schemas = {}
    for path in sorted((ROOT / "schemas").glob("*.json")):
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)
        schemas[path.name] = schema
    instances = [
        ("canonical-problem.schema.json", "demo/bond-selection/problem.json"),
        ("canonical-problem.schema.json", "examples/conversion/pulser-to-classiq/canonical_problem.json"),
        ("program-ir.schema.json", "examples/conversion/pulser-to-classiq/program_ir.json"),
        ("translation-record.schema.json", "examples/conversion/pulser-to-classiq/translation_record.json"),
        ("capability-report.schema.json", "examples/bond-selection/pasqal-pulser/capability_report.json"),
        ("canonical-problem.schema.json", "examples/conversion/pulser-to-classiq-qaoa/canonical_problem.json"),
        ("program-ir.schema.json", "examples/conversion/pulser-to-classiq-qaoa/program_ir.json"),
        ("translation-record.schema.json", "examples/conversion/pulser-to-classiq-qaoa/translation_record.json"),
        ("optimization-record.schema.json", "examples/conversion/pulser-to-classiq-qaoa/optimization_record.json"),
        ("result-record.schema.json", "examples/conversion/pulser-to-classiq-qaoa/source_result.json"),
    ]
    instances += [("result-record.schema.json", str(p.relative_to(ROOT)))
                  for p in sorted((ROOT / "demo/bond-selection/result-records").glob("*.json"))]
    for schema_name, rel in instances:
        data = json.loads((ROOT / rel).read_text())
        for e in Draft202012Validator(schemas[schema_name]).iter_errors(data):
            err(f"{rel}: {e.message}")


def as_json(data):
    return json.loads(json.dumps(data, default=str))


def fixture_exists(ref: str) -> bool:
    path, _, anchor = ref.replace("::", "#").partition("#")
    target = ROOT / path
    if not target.exists():
        return False
    if anchor and target.suffix in (".yml", ".yaml"):
        data = yaml.safe_load(target.read_text())
        return any(c.get("id") == anchor for c in data.get("cases", []))
    if anchor and target.suffix == ".py":
        return f"def {anchor}(" in target.read_text()
    return True


def check_backends() -> None:
    data = as_json(yaml.safe_load((ROOT / "registry/backends.yml").read_text()))
    schema = json.loads((ROOT / "schemas/backend-capability.schema.json").read_text())
    for e in Draft202012Validator(schema).iter_errors(data):
        err(f"backends.yml: {list(e.path)[:3]} {e.message[:120]}")
    ids = [b["id"] for b in data["backends"]]
    if len(ids) != len(set(ids)):
        err("backends.yml: duplicate id")
    families = set(data["families"])
    seen = {b["physical_family"] for b in data["backends"]}
    if families != seen:
        err(f"backends.yml: families without a backend: {sorted(families - seen)}")
    hw = yaml.safe_load((ROOT / "evals/hardware/cases.yml").read_text())
    hw_ids = {c["id"] for c in hw["cases"]}
    for b in data["backends"]:
        lvl = b["support_level"]
        if lvl == "tested-local":
            ex = ROOT / b["example"]
            for f in ("README.md", "requirements.in", "requirements.lock", "main.py", "test_example.py", "expected.json"):
                if not (ex / f).exists():
                    err(f"backends.yml: {b['id']} tested-local example lacks {b['example']}/{f}")
        else:
            if not fixture_exists(b["fixture"]):
                err(f"backends.yml: {b['id']} fixture missing: {b['fixture']}")
        if lvl != "tested-local" and b["id"] not in hw_ids:
            err(f"evals/hardware/cases.yml: no case for {lvl} backend {b['id']}")
    tested = {b["id"] for b in data["backends"] if b["support_level"] == "tested-local"}
    want = {"qiskit-local", "cirq-local", "pennylane-default-qubit", "classiq-local", "dwave-local", "pulser-local",
            "bloqade-local", "pytket-local", "perceval-local"}
    if tested != want:
        err(f"backends.yml: tested-local set {sorted(tested)} != README-11 minimum {sorted(want)}")


def check_edges() -> None:
    data = as_json(yaml.safe_load((ROOT / "registry/conversion-edges.yml").read_text()))
    schema = json.loads((ROOT / "schemas/conversion-edge.schema.json").read_text())
    for e in Draft202012Validator(schema).iter_errors(data):
        err(f"conversion-edges.yml: {list(e.path)[:3]} {e.message[:120]}")
    models = ["gate", "rydberg-analog", "anneal", "photonic-DV", "photonic-CV", "research-only"]
    if set(data["model_matrix"]) != set(models) or any(set(r) != set(models) for r in data["model_matrix"].values()):
        err("conversion-edges.yml: model_matrix must cover every model pair")
    for edge in data["edges"]:
        for key in ("proof_fixture", "negative_fixture"):
            if edge.get(key) and not fixture_exists(edge[key]):
                err(f"conversion-edges.yml: {edge['id']} {key} missing: {edge[key]}")
        candidate = data["model_matrix"][edge["source"]["model"]][edge["target"]["model"]]
        if edge["classification"] != "U" and edge["classification"] not in candidate:
            err(f"conversion-edges.yml: {edge['id']} class {edge['classification']} not allowed by matrix {candidate}")
        if edge["classification"] != "U" and edge["maintained_bridge"]["status"] in ("unmaintained", "archived"):
            err(f"conversion-edges.yml: {edge['id']} uses an unmaintained bridge for a supported class")
        if edge["classification"] in ("E", "C", "R", "A") and edge["validation_state"] in ("draft", "negative-tested"):
            err(f"conversion-edges.yml: {edge['id']} claims {edge['classification']} without execution")
    for cls in ("E", "C", "R", "U"):
        if not any(e["classification"] == cls for e in data["edges"]):
            err(f"conversion-edges.yml: no shipped edge with class {cls}")
    pairs = {(e["source"]["model"], e["target"]["model"]) for e in data["edges"]}
    for need in [("gate", "gate"), ("gate", "photonic-DV"), ("rydberg-analog", "rydberg-analog"), ("anneal", "gate"),
                 ("rydberg-analog", "gate")]:
        if need not in pairs:
            err(f"conversion-edges.yml: representative route {need} has no fixture")


def check_compatibility() -> None:
    """Every pin in registry/compatibility.yml appears with the same version in the folder's requirements.lock."""
    data = yaml.safe_load((ROOT / "registry/compatibility.yml").read_text())
    rows = [(r["example"], r["pins"]) for r in data["targets"]] + \
           [(r["fixture"], r["pins"]) for r in data["conversion_environments"]]
    for folder, pins in rows:
        locks = list((ROOT / folder).rglob("requirements.lock"))
        if not locks:
            err(f"compatibility: {folder} has no requirements.lock")
            continue
        text = "\n".join(lock.read_text() for lock in locks)
        for name, version in pins.items():
            if not re.search(rf"(?m)^{re.escape(name)}(\[[^\]]*\])?=={re.escape(str(version))}\b", text):
                err(f"compatibility: {folder} lock does not pin {name}=={version}")
    targets = {r["target"] for r in data["targets"]}
    if len(targets) != 9:
        err(f"compatibility: expected nine tested-local targets, found {sorted(targets)}")


def check_packs() -> None:
    for pack in list((ROOT / "knowledge").glob("*.md")) + list((ROOT / "domains").rglob("*.md")):
        words = len(pack.read_text().split())
        if words > 750:
            err(f"{pack.relative_to(ROOT)}: {words} words (target < ~1,000 tokens)")
    text = (ROOT / "knowledge/sources.yml").read_text()
    for ref in re.findall(r"`([a-z0-9-]+)`", " ".join(p.read_text() for p in (ROOT / "knowledge").glob("*.md"))):
        if "-" in ref and ref.startswith(("rr-", "nist", "fips", "nccoe", "pulser-", "hoefler", "egger", "markowitz", "preskill", "deutsch", "lucas", "farhi", "copilot-", "hw-", "sdk-")):
            if f"id: {ref}\n" not in text:
                err(f"knowledge cites unknown source id {ref}")


def check_coverage(registry: dict) -> None:
    routing = (ROOT / "evals/routing/cases.yml").read_text()
    behaviour = (ROOT / "evals/behavior/cases.yml").read_text()
    for s in registry["skills"]:
        artifact = COVERAGE.get(s["name"])
        if not artifact or not (ROOT / artifact).exists():
            err(f"coverage: {s['name']} has no template/schema")
        if s["name"] != "q-mentor-orchestrate" and s["name"] not in routing:
            err(f"coverage: {s['name']} has no routing eval")
    for needed in ("classical-only", "prompt-injection", "prohibited-data", "pulser", "pennylane", "pqc", "machine-mode", "remote-execution"):
        if needed not in behaviour:
            err(f"coverage: behaviour eval category {needed} missing")


def check_pqc_fixture() -> None:
    from pqc_inventory import scan
    found = {(f["file"], f["algorithm"], f["category"], f["confidence"]) for f in scan(ROOT / "evals/behavior/pqc-fixtures")}
    expected = yaml.safe_load((ROOT / "evals/behavior/pqc-fixtures/expected.yml").read_text())["findings"]
    exp = {(e["file"], e["algorithm"], e["category"], e["confidence"]) for e in expected}
    if found != exp:
        err(f"pqc fixture mismatch: missing {exp - found}, unexpected {found - exp}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-schema", action="store_true")
    args = parser.parse_args()
    check_manifest(args.live_schema)
    check_agent()
    registry = check_registry()
    check_skills(registry)
    check_schemas_and_artifacts()
    check_packs()
    check_help(registry)
    check_backends()
    check_edges()
    check_compatibility()
    check_coverage(registry)
    check_pqc_fixture()
    for e in errors:
        print("FAIL", e)
    print("package: OK" if not errors else f"package: {len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
