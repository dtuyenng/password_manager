from importlib.metadata import files
from Keychain import *
from password_generator import password_generator
from authenticate import authenticate
import json
import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import messagebox

"""

TODO:
    - Add copy function
    - scrollable treeview
    - make frame size static
    - create menu
    - convert and load from json in menu

"""


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



keychain = Keychain()

def edit_key_popup():
    """Opens a custom pop-up window centered within the main window."""
    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Edit Key")

    # Set the size of the pop-up window
    popup_width = 450
    popup_height = 300

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
    popup_frame.pack()

    # Setting up data needed
    # Get the selected row's Iid
    edited_key = password_table.selection()[0]

    # Get the values of the selected row
    # item_value returns ('6', 'Google', 'neyuttad@gmail.com', 't1^1Cg78pV%EJhi69m-k')
    item_values = password_table.item(edited_key, 'values')
    label_variable = item_values[1]
    username_variable = item_values[2]
    password_variable = item_values[3]


    # Add widgets
    label_popup_label = tk.Label(popup_frame, text="Label")
    label_popup_label.grid(row=0, column=1, sticky="E")
    label_entry = ttk.Entry(popup_frame, textvariable=label_variable)
    label_entry.delete(0, tk.END)  #first delete then insert or it will show double
    label_entry.insert(0, label_variable)
    label_entry.config(state='readonly')
    label_entry.grid(row=1, column=0, columnspan=2, sticky="WE")

    label_popup_username = tk.Label(popup_frame, text="Username")
    label_popup_username.grid(row=3, column=0, sticky="E")
    username_entry = ttk.Entry(popup_frame, textvariable=username_variable)
    username_entry.delete(0, tk.END)
    username_entry.insert(0, username_variable)
    username_entry.config(state='readonly')
    username_entry.grid(row=4, column=0, sticky="E")

    label_popup_password = tk.Label(popup_frame, text="Password")
    label_popup_password.grid(row=3, column=1, sticky="E")
    password_entry = ttk.Entry(popup_frame, textvariable=password_variable)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password_variable)
    password_entry.config(state='readonly')
    password_entry.grid(row=4, column=1, sticky="E")



def add_key_popup():
    """Opens a custom pop-up window centered within the main window."""
    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Add Key")

    # Set the size of the pop-up window
    popup_width = 450
    popup_height = 300

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
    popup_frame.pack()

    # Configure columns to make sure they expand properly
    popup_frame.grid_columnconfigure(0, weight=1)
    popup_frame.grid_columnconfigure(1, weight=1)

    # Add widgets
    label_popup_label = tk.Label(popup_frame, text="Label")
    label_popup_label.grid(row=0, column=1, sticky="E")
    label_entry = ttk.Entry(popup_frame, textvariable=label_variable)
    # label_entry.insert(0, "enter name)")
    label_entry.grid(row=1, column=0, columnspan=2, sticky="WE")

    label_popup_username = tk.Label(popup_frame, text="Username")
    label_popup_username.grid(row=3, column=0, sticky="E")
    username_entry = ttk.Entry(popup_frame, textvariable=username_variable)
    username_entry.grid(row=4, column=0, sticky="E")

    label_popup_password = tk.Label(popup_frame, text="Password")
    label_popup_password.grid(row=3, column=1, sticky="E")
    password_entry = ttk.Entry(popup_frame, textvariable=password_variable)
    password_entry.grid(row=4, column=1, sticky="E")

    # Add buttons
    add_button_popup = ttk.Button(popup_frame, text="Add Key", command= lambda: add_key_button_event(popup))
    add_button_popup.grid(row=6, column=0, sticky="WE")
    cancel_button = ttk.Button(popup_frame, text="Cancel", command=popup.destroy)
    cancel_button.grid(row=6, column=1, sticky="WE")
    generate_password_button = ttk.Button(popup_frame, text="Generate Random", width=2, command=lambda: password_variable.set(password_generator(20)))
    generate_password_button.grid(row=5, column=1, sticky="NSEW")

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

def delete_key_event():
    deleted_key = password_table.selection()[0]
    # deleted_key_values returns ('6', 'Google', 'neyuttad@gmail.com', 't1^1Cg78pV%EJhi69m-k')
    deleted_key_values = password_table.item(deleted_key, 'values')

    # remove key from treeview
    password_table.delete(deleted_key)

    #remove key from keychain key_list
    keychain.remove_key(int(deleted_key_values[0]))

def print_keychain():
    print("\n")
    for key in keychain.key_list:
        print(key.id, key.label, key.username, key.password)

window = tk.Tk()
window.title("My Password Manager")
window.geometry("800x500")

password_table = ttk.Treeview(window, columns=("id", "label", "username", "password"), show="headings")
password_table.heading("id", text="id")
password_table.heading("label", text="Label")
password_table.heading("username", text="username")
password_table.heading("password", text="password")
password_table.pack()

#column widths

password_table.column("id", width=30)
password_table.column("label", width=230)
password_table.column("username", width=250)
password_table.column("password", width=250)

# App Variables
label_variable = tk.StringVar()
username_variable = tk.StringVar()
password_variable = tk.StringVar()

delete_button = ttk.Button(window, text="Delete", command=delete_key_event)
delete_button.pack(side="right", padx=20)

edit_button = ttk.Button(window, text="Edit", command=edit_key_popup)
edit_button.pack(side="right", padx=20)

add_button = ttk.Button(window, text="Add", command=add_key_popup)
add_button.pack(side="right",  padx=20)


# debug_label = ttk.Label(window, text=f"{label_variable}")
# debug_label.pack()
# print_key = ttk.Button(window, text="Print Keys", command=print_keychain)
# print_key.pack(side="right", pady=20)


load_keys_on_startup()
window.mainloop()

# keychain.save_keychain() #Save keychain when app quits






# if __name__ == "__main__":
#     keychain = Keychain()
#     # keychain.add_key("Google", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Bank of America", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Fidelity", "dn52002@gmail.com", password_generator(20))
#     if authenticate(keychain):
#         main()
