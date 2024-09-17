import json
import pickle
from encryption import encrypt, decrypt, password


class Keychain:
    def __init__(self):
        self.__password = "" #private variable
        self.key_list = []
        self.load_keychain("data.bin")

    def set_password(self, password):
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

    def load_keychain(self, path: str):
        self.remove_allkeys()  # Clear all keys
        try:
            with open(path, "rb") as file:
                data = pickle.load(file)

            decrypted_data = decrypt(data).decode("utf-8")  # Decrypt data and decode bytes into original JSON string
            data_list = json.loads(decrypted_data)  # Convert JSON string to list
            print(data_list)

            # Ensure the expected keys are in the data
            if "password" in data_list:
                print(f"Password: {data_list['password']}")
                self.set_password(data_list["password"])
            else:
                print("Password key not found in the data")

            if "key_list" in data_list:
                for key in data_list["key_list"]:
                    if "label" in key and "username" in key and "password" in key:
                        self.add_key(key["label"], key["username"], key["password"])
                    else:
                        print(f"Invalid key format: {key}")
            else:
                print("Key list not found in the data")

        except FileNotFoundError:
            print("File not found")
        except EOFError:
            print("Error: Pickle data was truncated")
        except (pickle.PickleError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # def load_keychain(self, path: str):
    #     self.remove_allkeys() #clear from all keys
    #     try:
    #         with open(path, "rb") as file:
    #             data = pickle.load(file)
    #
    #         decrypted_data = decrypt(data).decode("utf-8")  # decrypt data, then decode bytes into original json str
    #         data_list = json.loads(decrypted_data)  # convert json str to list
    #         print(f"data_list: {data_list["password"]}")
    #
    #         self.set_password(data_list["password"])
    #         for key in data_list["key_list"]:
    #             self.add_key(key["label"], key["username"], key["password"])
    #     except FileNotFoundError:
    #         print("File not found")

    # The data is first converted into a dict, then serialized as a JSON
    # then encoded. It is then encrypted and stored
    def save_keychain(self):
        data = json.dumps(self.to_dict()).encode("utf-8")
        print(f"data: {data}")
        encrypted_data = encrypt(data)
        with open("data.bin", "wb") as file:
            pickle.dump(encrypted_data, file)
        print("Keychain saved to local storage.")

    def save_keychain_to_data(self):
        data = json.dumps(self.to_dict()).encode("utf-8")
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
        self.save_keychain()
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
