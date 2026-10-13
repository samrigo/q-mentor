"""Fixture: symmetric encryption and hashing -> separate category, not 'broken'."""
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY = AESGCM.generate_key(bit_length=128)
DIGEST = hashlib.sha256(b"synthetic").hexdigest()
