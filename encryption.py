from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import pickle

password = b"my_super_secret_password"
salt = b"&fj3adslkj$39-kjhu3"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
fernet = Fernet(key)

def encrypt(message: bytes) -> bytes:
    return fernet.encrypt(message)

def decrypt(message:bytes) -> bytes:
    try:
        decrypted_message = fernet.decrypt(message)
        return decrypted_message
    except InvalidToken:
        print("Decryption failed. The password might be incorrect or the data might be corrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")