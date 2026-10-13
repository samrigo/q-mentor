"""Reference crypto inventory used to test q-mentor-pqc-scan behaviour. Read-only.

Classifies, never judges: public-key algorithms (Shor-exposed) are migration-review
items; symmetric ciphers and hashes are key/output-size review items. A text-only
match in prose is low confidence. Output is for a human security owner.

Usage: python scripts/pqc_inventory.py PATH [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

CODE = {".py", ".js", ".ts", ".java", ".go", ".rs", ".cs", ".rb", ".kt", ".c", ".cc", ".cpp", ".h"}
CONFIG = {".conf", ".cfg", ".ini", ".yml", ".yaml", ".toml", ".json", ".xml", ".properties"}
PUBLIC_KEY = [
    ("RSA", re.compile(r"\brsa\b|RSA_|rsa\.generate|RSAPrivateKey|PKCS1", re.I)),
    ("ECC", re.compile(r"\bec\.generate_private_key|SECP\d+R1|\becdsa\b|\becdh\b|ed25519|nistp\d+|elliptic.curve", re.I)),
    ("DH", re.compile(r"diffie-hellman|\bffdhe\d*|\bDHE\b|dh\.generate_parameters", re.I)),
]
SYMMETRIC = [
    ("AES-128", re.compile(r"AES\w*\.generate_key\(bit_length=128\)|aes-?128", re.I)),
    ("AES-256", re.compile(r"AES\w*\.generate_key\(bit_length=256\)|aes-?256", re.I)),
]
HASHES = [
    ("SHA-1", re.compile(r"hashlib\.sha1\b|\bsha-?1\b", re.I)),
    ("SHA-256", re.compile(r"hashlib\.sha256\b", re.I)),
]


def classify_file(path: Path) -> List[Dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    suffix = path.suffix.lower()
    kind = "code" if suffix in CODE else "config" if suffix in CONFIG or path.name.endswith("_config") else "prose"
    findings = []

    def add(alg: str, category: str, confidence: str, line_no: int, line: str) -> None:
        findings.append({"file": path.name, "path": str(path), "line": line_no, "algorithm": alg,
                         "category": category, "confidence": confidence, "evidence": line.strip()[:160],
                         "next_step": "security owner to confirm use, data lifetime and migration plan"})

    has_import = kind == "code" and re.search(r"^\s*(from|import)\s+\S*(crypt|ssl|hashlib|jose|jwt)", text, re.M | re.I)
    seen = set()
    for no, line in enumerate(text.splitlines(), 1):
        for alg, pattern in PUBLIC_KEY:
            if pattern.search(line) and (alg, "pk") not in seen:
                seen.add((alg, "pk"))
                if kind == "prose":
                    add(alg, "unclear", "low", no, line)
                else:
                    conf = "high" if has_import else "medium"
                    add(alg, "public-key-shor-exposed", conf, no, line)
        if kind == "code":
            for alg, pattern in SYMMETRIC:
                if pattern.search(line) and (alg, "sym") not in seen:
                    seen.add((alg, "sym"))
                    add(alg, "symmetric-review-key-size", "high" if has_import else "medium", no, line)
            for alg, pattern in HASHES:
                if pattern.search(line) and (alg, "hash") not in seen:
                    seen.add((alg, "hash"))
                    add(alg, "hash-review-output-size", "high" if has_import else "medium", no, line)
    return findings


def scan(root: Path) -> List[Dict[str, str]]:
    files = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
    out: List[Dict[str, str]] = []
    for path in files:
        if path.name in {"expected.yml"}:
            continue
        out.extend(classify_file(path))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    findings = scan(Path(args.path))
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for f in findings:
            print(f"{f['confidence']:<6} {f['category']:<28} {f['algorithm']:<8} {f['path']}:{f['line']}  {f['evidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
