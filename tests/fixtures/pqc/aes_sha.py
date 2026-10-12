# Synthetic fixture: symmetric and hash usage only.
import hashlib

cipher_name = "AES-256-GCM"
digest = hashlib.sha256(b"synthetic").hexdigest()
