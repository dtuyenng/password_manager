import json
import pickle
import os
import sys
from importlib.metadata import PathDistribution
from data_path import *
from encryption import encrypt, decrypt, password


data_file = get_resource_path("data.bin")

class Keychain:
    def __init__(self):
        self.__password = "" #private variable
        self.key_list = []
        show_paths()
        self.load_keychain(get_resource_path("data.bin"))

    def set_password(self, password: str):
        self.__password = password

    def get_password(self):
        return self.__password


    # Convert the class object to a dictionary but since the class has a
    # key_list which itself has objects in it, we need to first iterate through
    # them and use their own to_dict method to convert to a dictionary
    # We then return the dictionary
    def to_dict(self) -> dict:
        key_list_dict= []
        for key_obj in self.key_list:
            key_list_dict.append(key_obj.to_dict())
        return {
            "password": self.get_password(),
            "key_list": key_list_dict
        }
    ######################################################
    # Load keychain from a path as string i.e "data.bin"
    def load_keychain(self, path):
        self.remove_allkeys() #clear from all keys
        try:
            with open(path, "rb") as file:
                data = pickle.load(file)

            decrypted_data = decrypt(data).decode("utf-8")  # decrypt data, then decode bytes into original json str
            data_list = json.loads(decrypted_data)  # convert json str to list
            print(f"load_keychain -> data_list: {data_list["password"]}  {data_list['key_list']}")

            self.set_password(data_list["password"])
            for key in data_list["key_list"]:
                self.add_key(key["label"], key["username"], key["password"])
        except FileNotFoundError:
            print(f"File not found. Path: {path}")

    # The data is first converted into a dict, then serialized as a JSON
    # then encoded. It is then encrypted and stored
    def save_keychain(self, path: str):
        data = json.dumps(self.to_dict()).encode("utf-8")
        print(f"save_keychain -> data: {data}")
        encrypted_data = encrypt(data)
        with open(path, "wb") as file:
            pickle.dump(encrypted_data, file)
        print(f"Keychain saved to local storage. Path {path}")

    def save_keychain_to_file(self):
        data = json.dumps(self.to_dict()).encode("utf-8")
        print(f"save_keychain_to_file -> data: {data}")
        encrypted_data = encrypt(data)
        return encrypted_data

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

    def modify_key(self, id, label, username, password):
        print(f"Debug: {self.key_list}")
        # key is minus 1 to match data in treeview
        self.key_list[id-1].label = label
        self.key_list[id-1].username = username
        self.key_list[id-1].password = password
        self.save_keychain(get_save_path("data.bin"))
        print("Key Updated successfully.")

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
