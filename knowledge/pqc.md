# Post-Quantum Cryptography Inventory

## Quantum-vulnerable

- RSA, ECC (ECDSA, ECDH), finite-field DH, and similar public-key schemes based on factoring or discrete log.

## Generally not quantum-vulnerable in the same way

- AES (symmetric), SHA-family hashing, most MACs (key-size considerations still apply).

## Rules

- Inventory only; never change cryptography.
- Flag false positives.
- Recommend formal security review for any production migration path.
- Prefer NIST PQC standards when advising.
