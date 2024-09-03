import uuid
from password_generator import password_generator

class Keychain:
    def __init__(self, pwd):
        self.pwd = pwd
        self.key_list = []
        self.next_id = 0

    def display_key_list(self):
        print("Printing Keychain")
        for key in self.key_list:
            print(f"ID:{key.key_id}   Label: {key.key_label}  |   Username: {key.username}    |    Password: {key.password}")

    def add_key(self, label, username, password):
        new_key = Key(self.next_id, label, username, password)
        self.next_id += 1
        self.key_list.append(new_key)
        print("Key added")

    def remove_key(self, key_id):
        for key in self.key_list:
            if key.key_id == key_id:
                self.key_list.remove(key)


    def modify_key(self):
        print("Key modified")


class Key:
    def __init__(self, key_id, key_label: str, username: str, password: str):
        self.key_id = key_id
        self.key_label = key_label
        self.username = username
        self.password = password

