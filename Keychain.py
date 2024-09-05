import json
import uuid
from password_generator import password_generator
import pickle

class Keychain:
    def __init__(self):
        self.password = ""
        self.key_list = []
        self.next_id = 0
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

    def delete_allkeys(self):
        self.key_list = []

    def load_keychain(self):
        with open("keychain.json", "r") as file:
            data = json.load(file)
        self.password = data["password"]
        for key in data["key_list"]:
            self.add_key(key["label"], key["username"], key["password"])


    def save_keychain(self):
        with open("keychain.json", "wb") as file:
            json.dump(self.to_dict(), file)

    def display_key_list(self):
        print("Registered Keys:")
        for key in self.key_list:
            print(f"ID:{key.id}   Label: {key.label}  |   Username: {key.username}    |    Password: {key.password}")

    def add_key(self, label, username, password):
        new_key = Key(self.next_id, label, username, password)
        self.next_id += 1
        self.key_list.append(new_key)

    def remove_key(self, id):
        for key in self.key_list:
            if key.id == id:
                self.key_list.remove(key)

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
