# Post-quantum cryptography inventory

**Rule:** inventory and classify; never migrate, never certify, always hand off to a security owner.

## What to flag
- Public-key, Shor-exposed: RSA, finite-field Diffie–Hellman, elliptic-curve key exchange and signatures (ECDH, ECDSA, Ed25519).
- Symmetric and hashes are a separate category: Grover gives at most a quadratic speed-up; review key and output sizes (e.g. AES-128 vs AES-256) rather than labelling them broken.
- Context that changes priority: protocol (TLS, SSH, JWT, S/MIME), library and version, certificate chains, key lifetimes, long-lived stored data ("harvest now, decrypt later").

## NIST standards (final, August 2024)
FIPS 203 ML-KEM (key encapsulation), FIPS 204 ML-DSA (signatures), FIPS 205 SLH-DSA (hash-based signatures). Check the NIST PQC project page for current status before stating timelines.

## Finding format
Location · algorithm/protocol · evidence (code or config line) · confidence (high/medium/low; a text match alone is low) · exposure · next step for the security owner.

## Do not
Replace algorithms, call a system "unsafe" from a string match, promise compliance, or say migration is only a future concern.

## Sources
`nist-pqc`, `fips-203`, `fips-204`, `fips-205`, `nccoe-pqc` in `sources.yml`.
