---
name: q-mentor-pqc-scan
description: "Inventory quantum-vulnerable cryptography (RSA, DH, ECC) separately from symmetric and hash use, with evidence and confidence, and hand findings to a security owner. Use when the user asks about post-quantum readiness, PQC or a crypto inventory."
license: MIT
allowed-tools: read, search
---

# Q-Mentor · PQC scan

Findings only. Never migrate, certify or call a system unsafe from a string match.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`:
registry `registry/skills.yml`, contract `templates/response-contract.md`; packs `knowledge/pqc.md`.
If the registry or contract cannot be found, answer `Status: blocked` naming the missing file. Do not guess.

## Input

Repository paths, configs or dependency manifests in scope.

## Output

Findings: location · algorithm/protocol · category (public-key Shor-exposed / symmetric / hash / unclear) · evidence line · confidence · data-lifetime exposure · next step for the security owner.
Default mode is brief (`Status`, `Result`, `Validation`, `Next`). Honor `detailed` or `machine` when asked.

## Procedure

1. Search code, configs and dependency manifests for public-key algorithms, protocols and libraries.
2. Classify; a bare text match is low confidence until the call site or config confirms it.
3. Treat AES/SHA findings as key-size or output-size review items, not breaks.
4. Note long-lived data and certificates.
5. Reference NIST FIPS 203/204/205 and the NIST PQC page; do not state migration deadlines without a live check.

## Stop when

No authorised scope; secrets found (report the location only, never the value).

## Handoffs

`q-mentor-review` and a human security owner. Never automatic migration. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
