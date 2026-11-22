from cryptography.fernet import Fernet
import secrets

print("FERNET_KEY=", Fernet.generate_key().decode())




print("CPF_HASH_KEY=", secrets.token_urlsafe(32))

print("SECRET_KEY=",secrets.token_hex(32))