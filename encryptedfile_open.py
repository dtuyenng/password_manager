# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.fernet import Fernet, InvalidToken
# import base64
# import os
# import pickle
# import json
#
# password = b"stupid"
#
# # Generate a key using PBKDF2HMAC for better security
# salt = b"&fj3adslkj$39-kjhu3"
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
# )
# key = base64.urlsafe_b64encode(kdf.derive(password))
#
# fernet = Fernet(key)
#
# data = {'name': 'John', 'age': 30, 'city': 'New York'}
# data_bytes = json.dumps(data).encode()
#
#
# encrypted_data = fernet.encrypt(data_bytes)
#
# # Decrypt the message
# try:
#     decrypted_message = fernet.decrypt(encrypted_data)
#     print("Decrypted message:", decrypted_message.decode())
# except InvalidToken:
#     print("Decryption failed. The password might be incorrect or the data might be corrupted.")
# except Exception as e:
#     print(f"An error occurred: {e}")
#
#
#
# def encrypt_data():
#     pass
#
# def decrypt_data():
#     pass
#
#
#
# with open("encrypted_data.bin","wb") as file:
#     pickle.dump(data, file)
#
# with open("encrypted_data.bin","rb") as file:
#     loaded_data = pickle.load(file)