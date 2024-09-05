from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import pickle


# Your password
password = b"my_super_secret_password"


################### UNSALTED #######################
# # Hash the password to generate a key
# digest = hashes.Hash(hashes.SHA256())
# digest.update(password)
# key = base64.urlsafe_b64encode(digest.finalize())
################### UNSALTED #######################

# Generate a key using PBKDF2HMAC for better security
salt = b"&fj3adslkj$39-kjhu3"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Create a Fernet instance with the derived key
fernet = Fernet(key)

# Encrypt a message

message = b"1234 is the nuclear code"
encrypted_message = fernet.encrypt(message)
print("Encrypted message:", encrypted_message)


# Decrypt the message
try:
    decrypted_message = fernet.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message.decode())
except InvalidToken:
    print("Decryption failed. The password might be incorrect or the data might be corrupted.")
except Exception as e:
    print(f"An error occurred: {e}")