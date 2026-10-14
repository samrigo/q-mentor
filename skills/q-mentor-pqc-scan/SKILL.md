---
name: q-mentor-pqc-scan
description: Use when the user wants a post-quantum cryptography inventory — 'scan this repo for quantum-vulnerable crypto', 'where do we use RSA or ECC', 'PQC readiness check', 'harvest-now-decrypt-later exposure', 'which certificates need migration review' — returning evidence-backed findings routed to a human security owner.
license: MIT
allowed-tools: read, search
---

# Q-Mentor · PQC scan

Inventory cryptographic use with evidence and confidence; never migrate or declare a system safe/unsafe.

## Shared files

Resolve from the plugin root (`../../` from this file) or, in repository mode, from `.github/q-mentor/`: registry `registry/skills.yml`, contract `templates/response-contract.md`, packs `knowledge/pqc.md`. If the registry is missing or invalid, answer `Status: blocked` naming the file; do not guess.

## Response template: `evidence`

For **every** user-facing answer, including clarification, error, and direct invocation, render `templates/responses/evidence.md` through `qmentor.response.v3`; preserve its lead, field order, status, uncertainty, and validation. Do not answer free-form or ask the user to invoke another skill.

## Input

Source code or configuration (public or approved).

## Output

`CryptoFindings`: file:line, algorithm, category (public-key exposure vs symmetric/hash consideration), confidence, stored-data/key-lifetime notes, NIST reference, security-owner next step. Reference scanner: `scripts/pqc_inventory.py`.

## Procedure

1. Flag RSA, finite-field DH, and elliptic-curve key exchange/signatures for migration review.
2. Treat symmetric ciphers and hashes separately (Grover-type considerations, not Shor-type breaks).
3. Separate a text match from confirmed use; mark false-positive candidates (comments, docs) with low confidence.
4. Link findings to current NIST guidance (`knowledge/pqc.md`); no compliance promise, no silent replacement.

## Stop when

Non-public code without approval; scope unclear.

## Handoffs

`q-mentor-review` and a human security owner; never automatic migration. The agent decides; do not ask the user to type another command unless approval or a material choice is needed.
