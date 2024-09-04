from importlib.metadata import files

from Keychain import *
from password_generator import password_generator
import json


# def main_loop(user):
#     commands = {
#         'd': user.print_key_list,
#         'a': lambda: user.add_key(input("Enter username: "), input("Enter password: ")),
#         'r': lambda: user.remove_key(input("Enter username to remove: ")),
#         'm': lambda: user.modify_key(input("Enter username to modify: "), input("Enter new password: "))
#     }
#
#     user_input = ""
#     while user_input != "q":
#         print("Enter input: (d)isplay keychain  (a)dd key  (r)emove key  (m)odify key  (q)uit")
#         user_input = input(">").lower()
#
#         if user_input in commands:
#             commands[user_input]()
#         elif user_input != "q":
#             print("Invalid input. Please try again.")

def main_loop(keychain):
    keychain.load_keychain()
    user_input = ""
    print("\n" * 100)
    while user_input != "q":

        print("-----------------------------------------------------------------")
        print(">: (d)isplay keychain (a)dd key (r)emove key (s)ave Keychain       (q)uit")
        user_input = input(">").lower()
        if user_input == "d":
            print("\n" * 100)
            print("Keychain: ")
            keychain.display_key_list()
        if user_input == "r":
            user_input = input("Remove key with ID: ")
            keychain.remove_key(int(user_input))
        if user_input == "s":
            keychain.save_keychain()
            keychain.delete_allkeys()
            keychain.load_keychain()
            keychain.display_key_list()
        if user_input == "g":
            password_generator(20)
            print("Generated Password: " + password_generator(20))


keychain1 = Keychain("password123")
# keychain1.add_key("Google", "dn52002@gmail.com", password_generator(20))
# keychain1.add_key("Bank of America", "dn52002@gmail.com", password_generator(20))
# keychain1.add_key("Fidelity", "dn52002@gmail.com", password_generator(20))

# main_loop(keychain1)
# keychain1.display_key_list()
# keychain1.remove_key(0)
# keychain1.display_key_list()

# keychain1.load_keychain()
# keychain1.display_key_list()

main_loop(keychain1)
