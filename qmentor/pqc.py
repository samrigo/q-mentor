"""PQC inventory helper: locate and classify cryptographic use. Inventory only.

A text match is a CANDIDATE finding with a confidence, never a verdict that a
system is unsafe. Every finding routes to a security owner. Nothing is changed.
"""

from __future__ import annotations

import re
from pathlib import Path

# (category, quantum_exposure, pattern, confidence)
RULES = [
    ("public-key:rsa", "shor-vulnerable", r"\bRSA(?:_|-)?(?:OAEP|PSS|PKCS1|\d{3,4})?\b|\brsa\.generate|\bRSA\.generate|generate_private_key\(\s*public_exponent", "medium"),
    ("public-key:ecc", "shor-vulnerable", r"\bECDSA\b|\bECDH(?:E)?\b|\bEd25519\b|\bX25519\b|\bsecp\d{3}[rk]1\b|\bprime256v1\b|ec\.generate_private_key", "medium"),
    ("public-key:ffdh", "shor-vulnerable", r"\bDiffie[- ]?Hellman\b|\bDHE?_(?:RSA|DSS)\b|\bdh\.generate_parameters|\bDSA\b", "medium"),
    ("symmetric", "grover-margin-review", r"\bAES(?:-?(?:128|192|256))?(?:-?(?:GCM|CBC|CTR))?\b|\bChaCha20\b|\b3DES\b|\bDES\b", "medium"),
    ("hash", "grover-margin-review", r"\bSHA-?(?:1|224|256|384|512)\b|\bsha(?:1|256|512)\(|\bMD5\b|\bmd5\(", "medium"),
    ("pqc", "post-quantum", r"\bML-KEM\b|\bML-DSA\b|\bSLH-DSA\b|\bKyber\b|\bDilithium\b|\bSPHINCS\+?", "medium"),
    ("certificate", "inspect-key-type", r"-----BEGIN (?:CERTIFICATE|RSA PRIVATE KEY|EC PRIVATE KEY|PRIVATE KEY|PUBLIC KEY)-----", "high"),
]
COMMENT = re.compile(r"^\s*(#|//|\*|--)")
EXCLUDE_DIRS = {".git", "node_modules", ".venv", "__pycache__"}


def scan_text(text: str, path: str = "<text>") -> list[dict]:
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for category, exposure, pattern, confidence in RULES:
            for m in re.finditer(pattern, line, flags=re.IGNORECASE if category in {"hash"} else 0):
                conf = confidence
                if COMMENT.match(line):
                    conf = "low"
                findings.append(
                    {
                        "path": path,
                        "line": lineno,
                        "match": m.group(0),
                        "category": category,
                        "quantum_exposure": exposure,
                        "confidence": conf,
                        "evidence": line.strip()[:160],
                        "next_step": "security owner to confirm usage, key size/lifetime, data exposure, and migration plan",
                    }
                )
    return findings


def scan_paths(paths: list[str]) -> dict:
    findings = []
    for p in paths:
        root = Path(p)
        files = [root] if root.is_file() else [f for f in root.rglob("*") if f.is_file()]
        for f in files:
            if any(part in EXCLUDE_DIRS for part in f.parts):
                continue
            try:
                text = f.read_text(errors="ignore")
            except OSError:
                continue
            findings.extend(scan_text(text, str(f)))
    summary: dict[str, int] = {}
    for f in findings:
        summary[f["category"]] = summary.get(f["category"], 0) + 1
    return {
        "mode": "inventory-only",
        "changed_files": 0,
        "findings": findings,
        "summary": summary,
        "guidance": "https://csrc.nist.gov/Projects/Post-Quantum-Cryptography",
        "disclaimer": "Text matches are candidates. No system is labeled unsafe or compliant by this scan.",
    }


if __name__ == "__main__":  # pragma: no cover
    import json
    import sys

    print(json.dumps(scan_paths(sys.argv[1:] or ["."]), indent=2))
