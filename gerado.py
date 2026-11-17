from cryptography.fernet import Fernet

print("FERNET_KEY =", Fernet.generate_key().decode())


import secrets

print("CPF_HASH_KEY =", secrets.token_urlsafe(32))