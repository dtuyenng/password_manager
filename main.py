from importlib.metadata import files
from Keychain import *
from password_generator import password_generator
from authenticate import authenticate
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


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

def main():
    # print("\n" * 100)
    keychain.display_keys()
    while True:
        print("(d)isplay keychain (a)dd key (r)emove key (s)ave Keychain       (q)uit")
        user_input = input(">").lower()
        if user_input == "d":
            print("\n" * 100)
            keychain.display_keys()
        if user_input == "r":
            user_input = input("Remove key with ID: ")
            keychain.remove_key(int(user_input))
        if user_input == "s":
            keychain.save_keychain()
        if user_input == "g":
            password_generator(20)
            print("Generated Password: " + password_generator(20))
        if user_input == "q":
            break


# if __name__ == "__main__":
#     keychain = Keychain()
#     # keychain.add_key("Google", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Bank of America", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Fidelity", "dn52002@gmail.com", password_generator(20))
#     if authenticate(keychain):
#         main()

keychain = Keychain()

def open_add_key_popup():
    """Opens a custom pop-up window centered within the main window."""
    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Custom Pop-up")

    # Set the size of the pop-up window
    popup_width = 300
    popup_height = 200

    # Get main window size and position
    main_window_width = window.winfo_width()
    main_window_height = window.winfo_height()
    main_window_x = window.winfo_x()
    main_window_y = window.winfo_y()

    # Calculate position x, y to center the pop-up in the main window
    position_x = main_window_x + (main_window_width // 2) - (popup_width // 2)
    position_y = main_window_y + (main_window_height // 2) - (popup_height // 2)

    # Set the geometry of the pop-up window
    popup.geometry(f"{popup_width}x{popup_height}+{position_x}+{position_y}")

    # Create a frame inside the pop-up
    popup_frame = tk.Frame(popup)
    popup_frame.pack(padx=10, pady=10)

    # Add entries inside the frame
    label_entry = ttk.Entry(popup_frame, textvariable=label_variable)
    label_entry.pack()
    username_entry = ttk.Entry(popup_frame, textvariable=username_variable)
    username_entry.pack()
    password_entry = ttk.Entry(popup_frame, textvariable=password_variable)
    password_entry.pack()

    # Add buttons
    add_button_popup = ttk.Button(popup_frame, text="Add Key", command= lambda: add_key_button_event(popup))
    add_button_popup.pack()
    close_button = ttk.Button(popup_frame, text="Cancel", command=popup.destroy)
    close_button.pack(pady=10)

def load_keys_on_startup():
    for key in keychain.key_list:
        new_key = (key.id, key.label, key.username, key.password)
        password_table.insert(parent="", index=key.id, values=new_key)

def add_key_button_event(popup):
    label = label_variable.get()
    username = username_variable.get()
    password = password_variable.get() or password_generator(20)

    if label and username:
        keychain.add_key(label, username, password)
        print("Key added to Keychain")

        # Get the last added key and update the table
        new_key = keychain.key_list[-1]
        password_table.insert("", "end", values=(new_key.id, new_key.label, new_key.username, new_key.password))
        popup.destroy()
    else:
        print("Please fill in the label and username fields.")

window = tk.Tk()
window.title("My Password Manager")
window.geometry("600x500")

password_table = ttk.Treeview(window, columns=("id", "Label", "Username", "Password"), show="headings")
password_table.heading("id", text="id")
password_table.heading("Label", text="Label")
password_table.heading("Username", text="username")
password_table.heading("Password", text="password")
password_table.pack()

frame3 = tk.Frame(window)
frame3.pack()
label_label = tk.Label(frame3, text="Label")
label_label.pack(side="left")
label_username = tk.Label(frame3, text="Username")
label_username.pack(side="left")
label_password = tk.Label(frame3, text="Password")
label_password.pack(side="left")

frame1 = tk.Frame(window)
frame1.pack()

# App Variables
label_variable = tk.StringVar()
username_variable = tk.StringVar()
password_variable = tk.StringVar()

frame2 = tk.Frame(window)
frame2.pack()
add_button = ttk.Button(frame2, text="Add Key", command=open_add_key_popup)
add_button.pack(side="left")

edit_button = ttk.Button(frame2, text="Edit Key", command=lambda: print("Key Edited"))
edit_button.pack(side="left")


delete_button = ttk.Button(frame2, text="Delete Key", command=lambda: print("Key Deleted"))
delete_button.pack(side="left")

load_keys_on_startup()

window.mainloop()











