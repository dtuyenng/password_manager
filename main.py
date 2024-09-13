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
    - scrollable treeview (done)
    - make frame size static (done)
    - create menu
    - convert and load from json in menu
    
Bugs:
    - When no item is selected (i.e during start up) and user presses edit, we get IndexError
    - Scrollbar doesn't have little arrows

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

def center_window(window, width, height):
    """Center the window on the screen."""
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position x, y
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the window size and position
    window.geometry(f"{width}x{height}+{x}+{y}")


# def center_pop(popup, width, height):
#     """Centers the given window on the main window."""
#     popup.update_idletasks()  # Ensure the window is updated with current size info
#
#     # Calculate the position to center the window
#     x = window.winfo_x() + (window.winfo_width() // 2) - (width // 2)
#     y = window.winfo_y() + (window.winfo_height() // 2) - (height // 2)
#
#     # Set the geometry of the pop-up window
#     popup.geometry(f"{width}x{height}+{x}+{y}")


def edit_key_popup():
    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Edit Key")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 350
    height = 300

    # Center the pop-up window
    center_window(popup, width, height)

    # Create a frame inside the pop-up
    popup_frame = tk.Frame(popup)
    popup_frame.pack(padx=10, pady=10, fill="x")

    # Setting up data needed
    edited_key = password_table.selection()[0]
    item_values = password_table.item(edited_key, 'values')

    popup_label_variable = item_values[1]
    popup_username_variable = item_values[2]
    popup_password_variable = item_values[3]

    # Add widgets
    tk.Label(popup_frame, text="Label").grid(row=0, column=0, sticky="E")
    label_entry = ttk.Entry(popup_frame)
    label_entry.insert(0, popup_label_variable)
    label_entry.config(state='readonly')
    label_entry.grid(row=0, column=1, sticky="WE", padx=5, pady=5)

    tk.Label(popup_frame, text="Username").grid(row=1, column=0, sticky="E")
    username_entry = ttk.Entry(popup_frame)
    username_entry.insert(0, popup_username_variable)
    username_entry.config(state='readonly')
    username_entry.grid(row=1, column=1, sticky="WE", padx=5, pady=5)

    tk.Label(popup_frame, text="Password").grid(row=2, column=0, sticky="E")
    password_entry = ttk.Entry(popup_frame)
    password_entry.insert(0, popup_password_variable)
    password_entry.config(state='readonly')
    password_entry.grid(row=2, column=1, sticky="WE", padx=5, pady=5)


def add_key_popup():
    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Add Key")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 450
    height = 200

    # Centering window function
    center_window(popup, width, height)

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
    add_button_popup.grid(row=6, column=0,  sticky="WE", pady=20)
    cancel_button = ttk.Button(popup_frame, text="Cancel", command=popup.destroy)
    cancel_button.grid(row=6, column=1, sticky="WE", pady=20)
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

center_window(window, 800, 500)
window.resizable(False, False)


main_frame = tk.Frame(window)
main_frame.pack(pady=20)

#Scroll bar for the TreeView
scroll_bar = tk.Scrollbar(main_frame, orient="vertical")
scroll_bar.grid(row=0, column=1, sticky="NS")

password_table = ttk.Treeview(main_frame, yscrollcommand= scroll_bar.set ,
                              # columns=("id", "label", "username", "password"),
                              columns=("id", "label", "username", "password"),
                              show="headings", height=20)
password_table.grid(row=0, column=0, sticky="NSEW")

scroll_bar.config(command=password_table.yview)

password_table.heading("id", text="id")
password_table.heading("label", text="Label")
password_table.heading("username", text="username")
password_table.heading("password", text="password")


#column widths
password_table.column("id", width=0, stretch=False) #hide column from user
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
