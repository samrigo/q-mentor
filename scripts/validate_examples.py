"""Example and conversion gates.

Static (always): example contract files, exact pins in every lock, syntax, undefined
names (pyflakes), placeholders, stale APIs from registry/compatibility.yml, ungated
remote calls, network calls, and the conversion fixtures in evals/conversion.

Dynamic (default; skip with --static): for each target, a FRESH virtual environment is
created from requirements.lock, then compileall + pytest run inside it. Uses `uv` when
available, else `python -m venv` + pip. No credentials, no network beyond package install.
"""
from __future__ import annotations

import argparse
import ast
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

import yaml
from jsonschema import Draft202012Validator
from pyflakes import api as flakes_api
from pyflakes import reporter as flakes_reporter

ROOT = Path(__file__).resolve().parents[1]
# Every folder under examples/ with a requirements.lock is a target; nothing is hand-listed.
TARGETS = sorted(str(p.parent.relative_to(ROOT)) for p in (ROOT / "examples").rglob("requirements.lock"))
CONTRACT_FILES = ["README.md", "requirements.in", "requirements.lock", "main.py", "adapter.py", "test_example.py", "expected.json"]
REMOTE_CALLS = re.compile(r"\b(synthesize\(|ExecutionSession\(|DWaveSampler\(|LeapHybrid\w*\(|QPUBackend\(|QiskitRuntimeService\()")
NETWORK = re.compile(r"\b(requests\.(get|post)|urllib\.request|http\.client|socket\.socket)\b")
PLACEHOLDER = re.compile(r"^\s*\.\.\.\s*(#.*)?$|\bTODO\b|\bFIXME\b|<your[-_ ]", re.M)


def stale_patterns() -> list:
    return yaml.safe_load((ROOT / "registry" / "compatibility.yml").read_text())["stale_apis"]


def undefined_names(path: Path) -> List[str]:
    class Collect(flakes_reporter.Reporter):
        def __init__(self):
            self.messages = []

        def flake(self, message):
            self.messages.append(str(message))

        def syntaxError(self, filename, msg, lineno, offset, text):
            self.messages.append(f"syntax error: {msg}")

        def unexpectedError(self, filename, msg):
            self.messages.append(f"error: {msg}")

    rep = Collect()
    flakes_api.checkPath(str(path), rep)
    return [m for m in rep.messages if "undefined name" in m or "syntax error" in m or "may be undefined" in m]


def scan_python(path: Path) -> List[str]:
    reasons = []
    text = path.read_text(encoding="utf-8")
    try:
        ast.parse(text)
    except SyntaxError:
        return ["syntax"]
    if undefined_names(path):
        reasons.append("undefined-name")
    if PLACEHOLDER.search(text):
        reasons.append("placeholder")
    for stale in stale_patterns():
        if stale["pattern"] in text:
            reasons.append("stale-api")
            break
    if REMOTE_CALLS.search(text) and "QMENTOR_ALLOW_REMOTE" not in text:
        reasons.append("ungated-remote")
    if NETWORK.search(text):
        reasons.append("network-call")
    return reasons


def check_lock(lock: Path) -> List[str]:
    bad = []
    for line in lock.read_text().splitlines():
        line = line.split("#")[0].strip()
        if not line or line.startswith("-"):
            continue
        if not re.fullmatch(r"[A-Za-z0-9_.\-\[\],]+==[A-Za-z0-9_.+\-!]+(\s*;.*)?", line):
            bad.append(line)
    return bad


def static_examples() -> List[str]:
    errors = []
    for target in TARGETS:
        folder = ROOT / target
        for name in CONTRACT_FILES:
            if not (folder / name).exists():
                errors.append(f"{target}: missing {name}")
        if (folder / "requirements.lock").exists():
            for line in check_lock(folder / "requirements.lock"):
                errors.append(f"{target}: unpinned lock line {line!r}")
        for py in sorted(folder.glob("*.py")):
            reasons = scan_python(py)
            if reasons:
                errors.append(f"{py.relative_to(ROOT)}: {reasons}")
    extra = [p for p in (ROOT / "examples").rglob("*.py") if not any(str(p).startswith(str(ROOT / t) + "/") for t in TARGETS)]
    for py in sorted((ROOT / "scripts").glob("*.py")) + [ROOT / "demo" / "bond-selection" / "canonical.py"] + sorted(extra):
        # Maintainer scripts: network use is allowed only behind explicit --live flags; the
        # validator itself contains the placeholder patterns it searches for.
        ignore = {"network-call"} | ({"placeholder"} if py.name == "validate_examples.py" else set())
        reasons = [r for r in scan_python(py) if r not in ignore]
        if reasons:
            errors.append(f"{py.relative_to(ROOT)}: {reasons}")
    return errors


def route_claim_reasons(case: dict, rc) -> List[str]:
    """Why a claimed conversion must be refused (README-14), or [] if the claim is supported by the registries."""
    if "edge" in case:
        edge = next(e for e in rc.edges()["edges"] if e["id"] == case["edge"])
        if case.get("claimed_default") and edge["maintained_bridge"]["status"] in ("unmaintained", "archived", "experimental"):
            return ["unmaintained-bridge"]
        return []
    route = rc.classify(case["source"], case["target"])
    target = rc.backends()[case["target"]]
    reasons = []
    if target["support_level"] == "research-only":
        reasons.append("research-only-target")
    if case.get("emits_code") and not route.may_emit_code:
        reasons.append("profiled-target-no-code" if target["support_level"] == "profiled" else "no-shipped-edge")
    if case["claimed_class"] != route.classification and "research-only-target" not in reasons:
        reasons.append("class-mismatch")
    return reasons


def conversion_fixtures() -> List[str]:
    sys.path.insert(0, str(ROOT / "demo" / "bond-selection"))
    sys.path.insert(0, str(ROOT / "scripts"))
    import canonical

    import route_conversion

    base = ROOT / "evals" / "conversion"
    errors = []
    for case in yaml.safe_load((base / "cases.yml").read_text())["cases"]:
        if case["kind"] == "route-claim":
            reasons = route_claim_reasons(case, route_conversion)
            ok = (not reasons) if case["expect"] == "accept" else case["reason"] in reasons
            print(f"{'PASS' if ok else 'FAIL'} route {case['id']}: {reasons or 'accepted'}")
            if not ok:
                errors.append(f"route claim {case['id']}: got {reasons}")
            continue
        path = (base / case["file"]).resolve()
        if case["kind"] in ("source", "target"):
            reasons = scan_python(path)
        elif case["kind"] == "energy-expression":
            problem = canonical.load_problem()
            const = canonical.to_qubo(problem)[2]
            expr = path.read_text().strip()
            reasons = []
            for x in itertools.product((0, 1), repeat=6):
                value = eval(expr, {"__builtins__": {}}, {"x": list(x)}) + const  # noqa: S307 - numeric fixture
                if abs(value - canonical.direct_energy(x, problem)) > 1e-9:
                    reasons = ["energy-mismatch"]
                    break
        elif case["kind"] == "translation-record":
            schema = json.loads((ROOT / "schemas" / "translation-record.schema.json").read_text())
            reasons = ["schema"] if list(Draft202012Validator(schema).iter_errors(json.loads(path.read_text()))) else []
        else:
            reasons = ["unknown-kind"]
        ok = (not reasons) if case["expect"] == "accept" else case["reason"] in reasons
        print(f"{'PASS' if ok else 'FAIL'} conversion {case['file']}: {reasons or 'accepted'}")
        if not ok:
            errors.append(f"conversion fixture {case['file']}: got {reasons}")
    return errors


def make_env(folder: Path, workdir: Path) -> Path:
    env_dir = workdir / folder.name
    uv = shutil.which("uv")
    if uv:
        subprocess.run([uv, "venv", "-q", "--python", "3.13", str(env_dir)], check=True)
        subprocess.run([uv, "pip", "sync", "-q", "--python", str(env_dir / "bin" / "python"),
                        str(folder / "requirements.lock")], check=True)
    else:
        subprocess.run([sys.executable, "-m", "venv", str(env_dir)], check=True)
        subprocess.run([str(env_dir / "bin" / "pip"), "install", "-q", "-r", str(folder / "requirements.lock")], check=True)
    return env_dir / "bin" / "python"


def dynamic_examples(only: List[str]) -> List[str]:
    errors = []
    with tempfile.TemporaryDirectory(prefix="qmentor-envs-") as tmp:
        for target in TARGETS:
            if only and not any(o in target for o in only):
                continue
            folder = ROOT / target
            print(f"== {target}: fresh environment from requirements.lock", flush=True)
            try:
                python = make_env(folder, Path(tmp) / target.replace("/", "_"))
                env = {k: v for k, v in os.environ.items() if not k.startswith("QMENTOR_")}
                subprocess.run([str(python), "-m", "compileall", "-q", "."], cwd=folder, check=True, env=env)
                subprocess.run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=folder, check=True, env=env)
            except subprocess.CalledProcessError as err:
                errors.append(f"{target}: {err.cmd[2] if len(err.cmd) > 2 else err.cmd} failed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", action="store_true", help="static scan and conversion fixtures only")
    parser.add_argument("--only", nargs="*", default=[], help="substring filter for target folders")
    args = parser.parse_args()
    errors = static_examples() + conversion_fixtures()
    if not args.static:
        errors += dynamic_examples(args.only)
    for err in errors:
        print("FAIL", err)
    print("examples: OK" if not errors else f"examples: {len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
