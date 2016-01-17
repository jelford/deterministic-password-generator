import base64
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(bytes, key):
    salt, encryption_key = generate_encryption_seed(key)
    fernet = Fernet(encryption_key)
    encrypted_bytes = fernet.encrypt(bytes)
    return salt + encrypted_bytes


def decrypt(bytes, key):
    salt = bytes[:32]
    _, encryption_key = generate_encryption_seed(key, salt=salt)
    fernet = Fernet(encryption_key)
    return fernet.decrypt(bytes[32:])


def generate_encryption_seed(encryption_key_seed, salt=None):
    salt = salt or os.urandom(32)
    encryption_key_seed = hashlib.sha512(encryption_key_seed.encode()).digest()
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
    )
    encryption_key = kdf.derive(encryption_key_seed)
    return salt, base64.urlsafe_b64encode(encryption_key)
