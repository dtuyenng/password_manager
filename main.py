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
    - convert and load from json in menu
    
Bugs:


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

def error_window_popup(error):
    popup = tk.Toplevel(window)
    popup.title("Error")
    popup.resizable(False, False)

    width = 450
    height = 100

    # Center the pop-up window
    center_window(popup, width, height)

    label = ttk.Label(popup, text=error)
    label.pack(side="top", expand=True)

def menu_edit_password():
    passwordVar1 = tk.StringVar()
    passwordVar2 = tk.StringVar()
    warning_msg = tk.StringVar()

    def set_password():
        if passwordVar1.get()  == "" :
            warning_msg.set("Enter a password")
        elif passwordVar2.get() == "" :
            warning_msg.set("Confirm password.")
        elif passwordVar1.get() != passwordVar2.get():
            warning_msg.set("Passwords do not match.")
        else:
            keychain.set_password(passwordVar1.get())
            keychain.save_keychain()
            messagebox.showinfo("Password Changed", "Password has been changed")
            popup.destroy()

    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Set Keychain Password")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 350
    height = 200

    # Centering window function
    center_window(popup, width, height)

    label = ttk.Label(popup, text="Enter Password")
    label.pack(side="top", expand=True)

    input1 = ttk.Entry(popup, textvariable=passwordVar1, justify="center")
    input1.pack(side="top", expand=True)
    input2 = ttk.Entry(popup, textvariable=passwordVar2, justify="center")
    input2.pack(side="top", expand=True)

    label_error_warning = ttk.Label(popup, textvariable=warning_msg)
    label_error_warning.pack(side="top", expand=True)

    set_button = ttk.Button(popup, text="Set Password", command=set_password)
    set_button.pack(side="top", expand=True)

def edit_key_popup():

    try:
        # Setting up data needed. This will fail if nothing is selected
        edited_key = password_table.selection()[0]
        item_values = password_table.item(edited_key, 'values')
        print(item_values[0])

        popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
        popup.title("Edit Key")
        popup.resizable(False, False)

        # Set the size of the pop-up window
        width = 500
        height = 250

        # Center the pop-up window
        center_window(popup, width, height)

        # Create a frame inside the pop-up
        popup_frame = tk.Frame(popup)
        popup_frame.pack(pady=20)

        # popup_label_variable = item_values[1]
        # popup_username_variable = item_values[2]
        # popup_password_variable = item_values[3]
        popup_label_variable = tk.StringVar(value=item_values[1])
        popup_username_variable = tk.StringVar(value=item_values[2])
        popup_password_variable = tk.StringVar(value=item_values[3])

        # Add widgets
        label_label = tk.Label(popup_frame, text="Label")
        label_label.grid(row=0, column=0, columnspan=2, sticky="EW")
        label_entry = ttk.Entry(popup_frame, justify="center")
        label_entry.insert(0, popup_label_variable.get())
        # label_entry.config(state='readonly')
        label_entry.grid(row=1, column=0, columnspan=2, sticky="EW")

        username_label = tk.Label(popup_frame, text="Username")
        username_label.grid(row=3, column=0, sticky="EW")
        username_entry = ttk.Entry(popup_frame, justify="center", textvariable=popup_username_variable)
        username_entry.insert(0, popup_username_variable.get())
        # username_entry.config(state='readonly')
        username_entry.grid(row=4, column=0, sticky="E")

        password_label = tk.Label(popup_frame, text="Password")
        password_label.grid(row=3, column=1, sticky="EW")
        password_entry = ttk.Entry(popup_frame, justify="center")
        password_entry.insert(0, popup_password_variable.get())
        # password_entry.config(state='readonly')
        password_entry.grid(row=4, column=1, sticky="E")

        # Add buttons
        generate_password_button = ttk.Button(popup_frame, text="Generate Random", width=2, command=lambda: password_variable.set(password_generator(20)))
        generate_password_button.grid(row=5, column=1, sticky="NSEW")

        update_button = ttk.Button(popup_frame, text="Update Key", command=update_key_event)
        update_button.grid(row=6, column=0, sticky="WE", pady=20)

        cancel_button = ttk.Button(popup_frame, text="Cancel", command=popup.destroy)
        cancel_button.grid(row=6, column=1, sticky="WE", pady=20)



    except IndexError:
        error_msg = "No Key Selected."
        messagebox.showwarning("Attention!", error_msg)
        print(error_msg)

def add_key_popup():

    #clear variables
    label_variable.set("")
    username_variable.set("")
    password_variable.set("")


    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Add Key")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 500
    height = 300

    # Centering window function
    center_window(popup, width, height)

    # Create a frame inside the pop-up
    popup_frame = tk.Frame(popup)
    popup_frame.pack(pady=40)

    # # Configure columns to make sure they expand properly
    # popup_frame.grid_columnconfigure(0, weight=1)
    # popup_frame.grid_columnconfigure(1, weight=1)

    # Add widgets
    label_popup_label = tk.Label(popup_frame, text="Label")
    label_popup_label.grid(row=0, column=0, columnspan=2, sticky="EW")
    label_entry = ttk.Entry(popup_frame, textvariable=label_variable, justify="center")
    label_entry.focus_set()
    label_entry.grid(row=1, column=0, columnspan=2, sticky="EW")

    label_popup_username = tk.Label(popup_frame, text="Username")
    label_popup_username.grid(row=3, column=0, sticky="EW")
    username_entry = ttk.Entry(popup_frame, textvariable=username_variable, justify="center")
    username_entry.grid(row=4, column=0, sticky="E")

    label_popup_password = tk.Label(popup_frame, text="Password")
    label_popup_password.grid(row=3, column=1, sticky="EW")
    password_entry = ttk.Entry(popup_frame, textvariable=password_variable, justify="center")
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

def update_key_event():
    keychain.modify_key()

def add_key_button_event(popup):
    label = label_variable.get()
    username = username_variable.get()
    password = password_variable.get() #or password_generator(20)

    if label and username and password:
        keychain.add_key(label, username, password)
        print("Key added to Keychain")

        # Get the last added key and update the table
        new_key = keychain.key_list[-1]
        password_table.insert("", "end", values=(new_key.id, new_key.label, new_key.username, new_key.password))
        popup.destroy()
    else:
        error_msg = "Please fill all required field"
        messagebox.showwarning("Attention!", error_msg)


def delete_key_event():
    try:
        deleted_key = password_table.selection()[0]
        deleted_key_values = password_table.item(deleted_key, 'values')

        # remove key from treeview
        password_table.delete(deleted_key)

        # remove key from keychain key_list
        keychain.remove_key(int(deleted_key_values[0]))
    except IndexError:
        error_msg = "No key selected."
        messagebox.showwarning("Attention!", error_msg)
        print(error_msg)

def print_keychain():
    print(keychain.key_list)
    print("\n")
    for key in keychain.key_list:
        print(key.id, key.label, key.username, key.password)

def on_copy(event):
    # Get the item and column where the right-click occurred
    item_id = password_table.identify_row(event.y)
    column_id = password_table.identify_column(event.x)

    if not item_id or not column_id:
        return

    # Get the column index (ignore the first column which is for row identifiers)
    col_index = int(column_id.split('#')[1]) - 1
    if col_index < 0:
        return

    # Get the value of the cell
    cell_value = password_table.item(item_id, 'values')[col_index]

    # Copy the cell value to the clipboard
    window.clipboard_clear()  # Clear the clipboard
    window.clipboard_append(cell_value)  # Append the copied cell value
    print(cell_value)
    # messagebox.showinfo("Copied", f"Copied: {cell_value}")

def show_context_menu(event):
    # Only show the context menu if the right-click is over a valid item
    item_id = password_table.identify_row(event.y)
    if item_id:
        context_menu.post(event.x_root, event.y_root)


window = tk.Tk()
window.title("My Password Manager")

center_window(window, 800, 500)
window.resizable(False, False)

def menu_import_keychain():
    pass

def menu_export_keychain():
    pass


# Create Menu Bar
menu = tk.Menu(window)
window.config(menu=menu)

#Create Menu Items

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Import Keychain", command = menu_import_keychain)
file_menu.add_command(label="Export Keychain...", command = menu_export_keychain)
file_menu.add_separator()
file_menu.add_command(label="Set Password...", command = menu_edit_password)
file_menu.add_separator()
file_menu.add_command(label="Debug: Print Keychain", command = print_keychain)
file_menu.add_command(label="Quit Password Manager", command = window.quit)

# about_menu = tk.Menu(menu)
# menu.add_cascade(label="Password Manager", menu=about_menu)
# about_menu.add_command(label="About Password Manager", command=menu_about)
# about_menu.add_command(label="Help", command=menu_about)


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
password_table.column("label", width=230, anchor="center")
password_table.column("username", width=250, anchor="center")
password_table.column("password", width=250, anchor="center")

# Create context menu to handle right click copy to clipboard functionality
# Create the context menu
context_menu = tk.Menu(window, tearoff=0)
context_menu.add_command(label="Copy value...")

#bind the right click (button 3) to show context menu
password_table.bind("<Button-2>", show_context_menu)

# Bind right-click to copy cell content
password_table.bind("<Button-2>", on_copy, add="+")  # Add the copy function to the context menu

# App Variables
label_variable = tk.StringVar()
username_variable = tk.StringVar()
password_variable = tk.StringVar()

#Setting bottom buttons inside a frame and center it
bottom_frame = tk.Frame(window)
bottom_frame.pack()

delete_button = ttk.Button(bottom_frame, text="Delete", command=delete_key_event)
delete_button.pack(side="right", padx=10)

edit_button = ttk.Button(bottom_frame, text="Edit", command=edit_key_popup)
edit_button.pack(side="right", padx=10)

add_button = ttk.Button(bottom_frame, text="Add", command=add_key_popup)
add_button.pack(side="right",  padx=10)


# debug_label = ttk.Label(window, text=f"{label_variable}")
# debug_label.pack()
# print_key = ttk.Button(window, text="Print Keys", command=print_keychain)
# print_key.pack(side="right", pady=20)

# # Bind the right-click (button 3) to show the context menu
# tree.bind("<Button-3>", show_context_menu)
#
# # Start the Tkinter main loop
# root.mainloop()


load_keys_on_startup()
window.mainloop()
keychain.save_keychain() #Save keychain when app quits
