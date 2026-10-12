---
name: q-mentor-pqc-scan
description: >
  Inventory quantum-vulnerable cryptographic use and request security review.
  Output findings only. Use when the user asks about post-quantum crypto readiness
  or wants a crypto inventory.
---

# q-mentor-pqc-scan

## Scope

- Identify use of RSA, ECC, DH, and other quantum-vulnerable primitives.
- Distinguish hybrid, classical, and post-quantum algorithms.
- Flag false positives (AES, hashing, etc.).
- Never change cryptography; only inventory and recommend review.

## Output

Findings table: Location | Algorithm | Vulnerability class | Recommendation | Uncertainty

Request a formal security review for any production migration.

## Knowledge links

- `knowledge/pqc.md`
