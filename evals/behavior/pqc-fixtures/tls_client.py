"""Fixture: public-key cryptography that must be flagged (synthetic, not used anywhere)."""
from cryptography.hazmat.primitives.asymmetric import ec, rsa

SIGNING_KEY = ec.generate_private_key(ec.SECP256R1())
LEGACY_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
