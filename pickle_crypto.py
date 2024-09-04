import pickle
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

data = {
    "users": [
        {
            "fname": "Tuyen",
            "lname": "Nguyen",
        },
        {
            "fname": "Vinh",
            "lname": "Nguyen",
        },
    ],
}

#Serialize data
pickled_data = pickle.dumps(data)

#Encrypt data
encrypted_data = cipher_suite.encrypt(pickled_data)

with open("users.bin", "wb") as file:
    file.write(encrypted_data)

# Decrypt the data
pickled_data = cipher_suite.decrypt(encrypted_data)

# Deserialize the data using pickle
data = pickle.loads(pickled_data)

print(data)