import json
import uuid
from password_generator import password_generator
import pickle
from encryption import encrypt, decrypt

class Keychain:
    def __init__(self):
        self.password = "123"
        self.key_list = []
        self.load_keychain()

    # Convert the class object to a dictionary but since the class has a
    # key_list which itself has objects in it, we need to first iterate through
    # them and use their own to_dict method to convert to a dictionary
    # We then return the dictionary

    def to_dict(self) -> dict:
        key_list_dict= []
        for key_obj in self.key_list:
            key_list_dict.append(key_obj.to_dict())
        return {
            "password": self.password,
            "key_list": key_list_dict
        }

    def load_keychain(self):
        self.remove_allkeys() #clear from all keys

        with open("data.bin", "rb") as file:
            data = pickle.load(file)

        decrypted_data = decrypt(data).decode("utf-8")  # decrypt data, then decode bytes into original json str
        data_list = json.loads(decrypted_data)          # convert json str to list

        self.password = data_list["password"]
        for key in data_list["key_list"]:
            self.add_key(key["label"], key["username"], key["password"])

    # The data is first converted into a dict, then serialized as a JSON
    # then encoded. It is then encrypted and stored
    def save_keychain(self):
        data = json.dumps(self.to_dict()).encode("utf-8")
        encrypted_data = encrypt(data)
        with open("data.bin", "wb") as file:
            pickle.dump(encrypted_data, file)
        print("Keychain saved to local storage.")

    def display_keys(self):
        print("Registered Keys:")
        for key in self.key_list:
            print(f"ID:{key.id}   Label: {key.label}  |   Username: {key.username}    |    Password: {key.password}")

    def add_key(self, label, username, password):
        new_index = len(self.key_list) + 1
        new_key = Key(new_index, label, username, password)
        self.key_list.append(new_key)

    def remove_key(self, id):
        for key in self.key_list:
            if key.id == id:
                self.key_list.remove(key)
                print(f"Key {key.label} {key.username} removed successfully.")


    def remove_allkeys(self):
        self.key_list = []

    def modify_key(self):
        print("Key modified")

class Key:
    def __init__(self, key_id, key_label: str, username: str, password: str):
        self.id = key_id
        self.label = key_label
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "username": self.username,
            "password": self.password,
        }
