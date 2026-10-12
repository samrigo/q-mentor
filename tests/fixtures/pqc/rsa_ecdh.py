# Synthetic fixture for the PQC inventory. Not real keys.
from cryptography.hazmat.primitives.asymmetric import ec, rsa

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
peer = ec.generate_private_key(ec.SECP256R1())
TLS_SUITES = ["ECDHE-RSA-AES128-GCM-SHA256"]
