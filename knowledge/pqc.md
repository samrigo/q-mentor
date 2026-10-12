# Post-quantum cryptography

`last_verified: 2026-10-12` · sources: `shor-1994`, `grover-1996`, `nist-pqc`, `fips-203`, `fips-204`, `fips-205`, `nccoe-migration`

## Operational rule

Inventory and classify; never replace algorithms, label a system "unsafe" from a text match, or promise compliance. Every finding has evidence, confidence, and a security-owner next step.

## Exposure classes

| Class | Examples | Quantum impact | Action |
|---|---|---|---|
| Public-key | RSA, finite-field DH, DSA, ECDH, ECDSA, Ed25519, X25519 | Broken by Shor's algorithm on a cryptographically relevant quantum computer | Migration review |
| Symmetric | AES, ChaCha20 | Grover gives at most a quadratic speedup; larger keys (e.g. AES-256) keep margin | Key-size review |
| Hash | SHA-2, SHA-3 | Grover/collision effects reduce margin modestly | Output-size review; MD5/SHA-1 are already weak classically |
| PQC | ML-KEM, ML-DSA, SLH-DSA | Designed to resist known quantum attacks | Verify implementation and parameters |

## NIST standards (finalized August 2024)

- FIPS 203 **ML-KEM** (key encapsulation, from CRYSTALS-Kyber).
- FIPS 204 **ML-DSA** (signatures, from CRYSTALS-Dilithium).
- FIPS 205 **SLH-DSA** (stateless hash-based signatures, from SPHINCS+).

Check the NIST PQC project page for later standards and transition timelines; status changes.

## Why it is not only a future concern

Harvest-now-decrypt-later: long-lived confidential data encrypted today with RSA/ECC key exchange can be recorded now and decrypted later. Key lifetime and data-retention period drive priority.

## What to capture per finding

Location, library and protocol, algorithm and key size, certificate chain, key lifetime, data exposure and retention, confidence, owner.

## Limits of a text scan

Names in comments, docs, or unrelated words create false positives; dynamic configuration and TLS negotiation are invisible to static search. Confirm with configuration review and the security owner.
