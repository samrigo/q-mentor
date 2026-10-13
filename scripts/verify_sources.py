"""Source-registry gate.

Offline (default): every entry has id, title, https URL, owner, type, volatility,
source_date, last_verified and verification; ids are unique; every `used_by` path
exists; volatile entries are no older than --max-age days.
--live: fetch each URL (HEAD, then GET) and report reachability. Run before releases.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["id", "title", "url", "owner", "type", "volatility", "source_date", "last_verified", "verification", "used_by"]
TYPES = {"peer-reviewed", "preprint", "vendor-documentation", "vendor-result", "secondary", "specification", "official-standard"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--max-age", type=int, default=120, help="days before a volatile source is stale")
    args = parser.parse_args()
    data = yaml.safe_load((ROOT / "knowledge" / "sources.yml").read_text())
    errors, ids = [], set()
    today = dt.date.today()
    for entry in data["sources"]:
        for key in REQUIRED:
            if key not in entry:
                errors.append(f"{entry.get('id')}: missing {key}")
        if entry["id"] in ids:
            errors.append(f"duplicate id {entry['id']}")
        ids.add(entry["id"])
        if not str(entry["url"]).startswith("https://"):
            errors.append(f"{entry['id']}: non-https url")
        if entry["type"] not in TYPES:
            errors.append(f"{entry['id']}: unknown type {entry['type']}")
        for used in entry["used_by"]:
            if not (ROOT / used).exists():
                errors.append(f"{entry['id']}: used_by path missing: {used}")
        verified = entry["last_verified"]
        verified = verified if isinstance(verified, dt.date) else dt.date.fromisoformat(str(verified))
        if entry["volatility"] == "volatile" and (today - verified).days > args.max_age:
            errors.append(f"{entry['id']}: volatile source last verified {verified}")
    if args.live:
        for entry in data["sources"]:
            req = urllib.request.Request(entry["url"], method="HEAD", headers={"User-Agent": "q-mentor-verify-sources"})
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    status = resp.status
            except Exception:
                try:
                    with urllib.request.urlopen(urllib.request.Request(entry["url"], headers={"User-Agent": "q-mentor-verify-sources"}), timeout=20) as resp:
                        status = resp.status
                except Exception as exc:  # report, do not hide
                    status = f"error: {exc.__class__.__name__}"
            print(f"{status} {entry['id']} {entry['url']}")
            if status != 200:
                errors.append(f"{entry['id']}: live check returned {status}")
    kit_only = sum(1 for e in data["sources"] if e["verification"] == "kit")
    print(f"{len(data['sources'])} sources; {kit_only} not yet live-checked (verification: kit)")
    for err in errors:
        print("FAIL", err)
    print("sources: OK" if not errors else f"sources: {len(errors)} failure(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
