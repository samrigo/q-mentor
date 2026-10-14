"""Source-registry gate (README-07, README-11, README-12).

Offline (default):
  * every entry has id, title, https URL, owner, type, kind, volatility, source_date, last_verified, verification,
    link_status, used_by; ids unique; used_by paths exist; volatile entries younger than --max-age days;
  * papers carry a DOI, arXiv id, or publisher URL; corrections point at an existing entry;
  * repository entries that were checked carry a 40-hex head_sha;
  * every DOI and arXiv link in brief/README-*.md is present (nothing in the brief is left unregistered).
--live: re-check links and write docs/SOURCE-CHECK.md. DOIs through Crossref (one request per DOI, polite delay),
  arXiv through the abstract page, GitHub through `git ls-remote`, everything else with HEAD/GET.
  HTTP 401/403/429 are recorded as blocked-by-publisher / rate-limited, never as broken.
--report: regenerate docs/SOURCE-CHECK.md from the registry without network access.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "knowledge" / "sources.yml"
REPORT = ROOT / "docs" / "SOURCE-CHECK.md"
REQUIRED = ["id", "title", "url", "owner", "type", "kind", "volatility", "source_date", "last_verified",
            "verification", "link_status", "used_by"]
TYPES = {"peer-reviewed", "preprint", "vendor-documentation", "vendor-result", "secondary", "specification",
         "official-standard", "repository", "commentary"}
KINDS = {"paper", "docs", "repository", "commits", "issues", "example"}
STATUSES = {"not-checked", "reachable", "repository-reachable", "metadata-only", "blocked-by-publisher", "rate-limited",
            "moved", "broken"}
UA = {"User-Agent": "q-mentor-verify-sources (+https://github.com/samrigo/q-mentor)"}


def load() -> tuple[str, dict]:
    text = REGISTRY.read_text(encoding="utf-8")
    return text.split("contract_version", 1)[0], yaml.safe_load(text)


def offline(data: dict, max_age: int) -> list:
    errors, ids = [], set()
    today = dt.date.today()
    for e in data["sources"]:
        for key in REQUIRED:
            if key not in e:
                errors.append(f"{e.get('id')}: missing {key}")
        if e["id"] in ids:
            errors.append(f"duplicate id {e['id']}")
        ids.add(e["id"])
        if not str(e["url"]).startswith("https://"):
            errors.append(f"{e['id']}: non-https url")
        if e.get("type") not in TYPES:
            errors.append(f"{e['id']}: unknown type {e.get('type')}")
        if e.get("kind") not in KINDS:
            errors.append(f"{e['id']}: unknown kind {e.get('kind')}")
        if e.get("link_status") not in STATUSES:
            errors.append(f"{e['id']}: unknown link_status {e.get('link_status')}")
        for used in e.get("used_by", []):
            if not (ROOT / used).exists():
                errors.append(f"{e['id']}: used_by path missing: {used}")
        verified = e["last_verified"]
        verified = verified if isinstance(verified, dt.date) else dt.date.fromisoformat(str(verified))
        if e["volatility"] == "volatile" and (today - verified).days > max_age:
            errors.append(f"{e['id']}: volatile source last verified {verified}")
        if e.get("kind") == "paper" and not (e.get("doi") or e.get("arxiv") or e["url"]):
            errors.append(f"{e['id']}: paper without DOI/arXiv/URL")
        if e.get("head_sha") and not re.fullmatch(r"[0-9a-f]{40}", e["head_sha"]):
            errors.append(f"{e['id']}: head_sha is not a full commit SHA")
        if e.get("kind") == "repository" and e.get("link_status") == "reachable" and not e.get("head_sha"):
            errors.append(f"{e['id']}: reachable repository without head_sha")
    for e in data["sources"]:
        if e.get("correction_of") and e["correction_of"] not in ids:
            errors.append(f"{e['id']}: correction_of unknown id {e['correction_of']}")
    urls = {e["url"].rstrip("/") for e in data["sources"]}
    for f in sorted((ROOT / "brief").glob("README*.md")):
        for url in re.findall(r"\]\((https?://[^)\s]+)\)", f.read_text()):
            if ("doi.org" in url or "arxiv.org" in url) and url.rstrip("/") not in urls:
                errors.append(f"{f.name}: paper link not in registry: {url}")
    return errors


def http_status(url: str, method: str = "HEAD") -> int | str:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method=method, headers=UA), timeout=25) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:  # network failure is reported, not hidden
        return f"error:{exc.__class__.__name__}"


def classify_http(code) -> str:
    if code == 200:
        return "reachable"
    if code in (401, 403):
        return "blocked-by-publisher"
    if code == 429:
        return "rate-limited"
    if code in (301, 302, 307, 308):
        return "moved"
    return "broken" if isinstance(code, int) else "not-checked"


def check_doi(doi: str) -> tuple[str, dict]:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as resp:
            msg = json.loads(resp.read())["message"]
    except urllib.error.HTTPError as exc:
        return classify_http(exc.code), {}
    except Exception:
        return "not-checked", {}
    year = (msg.get("published") or msg.get("issued") or {}).get("date-parts", [[None]])[0][0]
    updates = [f"{u.get('type')}:{u.get('DOI')}" for u in msg.get("update-to", [])]
    return "metadata-only", {"observed_title": (msg.get("title") or [""])[0], "observed_date": str(year),
                             **({"check_note": "updates " + ", ".join(updates)} if updates else {})}


def check_repo(repo: str) -> tuple[str, dict]:
    proc = subprocess.run(["git", "ls-remote", f"https://github.com/{repo}", "HEAD"], capture_output=True, text=True,
                          timeout=90, check=False)
    sha = proc.stdout.split()[0] if proc.returncode == 0 and proc.stdout else None
    return ("reachable", {"head_sha": sha}) if sha else ("broken", {})


def live(data: dict) -> None:
    today = dt.date.today().isoformat()
    repo_cache: dict = {}
    for e in data["sources"]:
        extra: dict = {}
        if e.get("doi"):
            status, extra = check_doi(e["doi"])
            time.sleep(1.0)
        elif e.get("repo"):
            if e["repo"] not in repo_cache:
                repo_cache[e["repo"]] = check_repo(e["repo"])
            status, extra = repo_cache[e["repo"]]
            if e.get("kind") != "repository" and status == "reachable":
                status = "repository-reachable"
        else:
            status = classify_http(http_status(e["url"]))
            if status in ("broken", "moved"):
                status = classify_http(http_status(e["url"], "GET"))
        e.update(extra)
        e["link_status"], e["checked_at"] = status, today
        print(f"{status:22} {e['id']}")


def write_report(data: dict) -> None:
    srcs = data["sources"]
    by_status = collections.Counter(e["link_status"] for e in srcs)
    papers = [e for e in srcs if e.get("kind") == "paper"]
    lines = ["# Source and link check", "",
             f"Generated from `knowledge/sources.yml` by `scripts/verify_sources.py`. {len(srcs)} sources; "
             f"{len(papers)} papers; {len({e['repo'] for e in srcs if e.get('repo')})} repositories.", "",
             "| link_status | count |", "|---|---:|", *[f"| {k} | {v} |" for k, v in sorted(by_status.items())], "",
             "## Papers", "", "| id | type | checked | observed title / date | note |", "|---|---|---|---|---|"]
    for e in sorted(papers, key=lambda x: x["id"]):
        obs = f"{e.get('observed_title', '')} ({e.get('observed_date', '')})" if e.get("observed_title") else ""
        lines.append(f"| `{e['id']}` | {e['type']} | {e['link_status']} | {obs} | {e.get('check_note', '')} |")
    lines += ["", "## Repositories (HEAD at check time)", "", "| repository | head_sha | checked |", "|---|---|---|"]
    seen = set()
    for e in sorted(srcs, key=lambda x: x.get("repo") or ""):
        if e.get("repo") and e["repo"] not in seen and e.get("head_sha"):
            seen.add(e["repo"])
            lines.append(f"| {e['repo']} | `{e['head_sha']}` | {e.get('checked_at', '')} |")
    lines += ["", "`not-checked` means the build session could not read the page (publisher rate limit, robots policy, or "
              "an unanswered fetch permission); it is not evidence that the link is broken. Re-run "
              "`python scripts/verify_sources.py --live` before every release.", ""]
    REPORT.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--max-age", type=int, default=120, help="days before a volatile source is stale")
    args = parser.parse_args()
    header, data = load()
    if args.live:
        live(data)
        REGISTRY.write_text(header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=200))
    if args.live or args.report:
        write_report(data)
    errors = offline(data, args.max_age)
    counts = collections.Counter(e["link_status"] for e in data["sources"])
    print(f"{len(data['sources'])} sources; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for err in errors:
        print("FAIL", err)
    print("sources: OK" if not errors else f"sources: {len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
