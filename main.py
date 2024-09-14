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
    - convert and load from json in menu
    - add a status message above button to notify user of various events such as
    saving, deleting, updating
    - add two inputs for password setting
    - after password is set, don't jsut destroy. make add button and input go away, and add a close button
    with a message that says it's ok to close
    - stylize edit key to be the same as add key (done)
    
Bugs:
    - when adding key, values of the previous add action is shown. Must clear the variables before 
    main functionality starts

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
    passwordVar = tk.StringVar()
    warning_msg = tk.StringVar()

    def set_password():
        if passwordVar.get() == "" :
            warning_msg.set("Please enter a password")
        else:
            keychain.set_password(passwordVar.get())
            print(keychain.password)
            warning_msg.set("Password Set!")
            keychain.save_keychain()
            popup.destroy()

    popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
    popup.title("Set Keychain Password")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 350
    height = 100

    # Centering window function
    center_window(popup, width, height)

    label = ttk.Label(popup, text="Enter Password")
    label.pack(side="top", expand=True)

    input = ttk.Entry(popup, textvariable=passwordVar, justify="center")
    input.pack(side="top", expand=True)

    label_error_warning = ttk.Label(popup, textvariable=warning_msg)
    label_error_warning.pack(side="top", expand=True)

    set_button = ttk.Button(popup, text="Set Password", command=set_password)
    set_button.pack(side="top", expand=True)

def edit_key_popup():

    try:
        # Setting up data needed. This will fail if nothing is selected
        edited_key = password_table.selection()[0]
        item_values = password_table.item(edited_key, 'values')

        popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
        popup.title("Edit Key")
        popup.resizable(False, False)

        # Set the size of the pop-up window
        width = 450
        height = 200

        # Center the pop-up window
        center_window(popup, width, height)

        # Create a frame inside the pop-up
        popup_frame = tk.Frame(popup)
        popup_frame.pack()

        popup_label_variable = item_values[1]
        popup_username_variable = item_values[2]
        popup_password_variable = item_values[3]

        # Add widgets
        label_label = tk.Label(popup_frame, text="Label")
        label_label.grid(row=0, column=0, columnspan=2, sticky="EW")
        label_entry = ttk.Entry(popup_frame, justify="center")
        label_entry.insert(0, popup_label_variable)
        label_entry.config(state='readonly')
        label_entry.grid(row=1, column=0, columnspan=2, sticky="EW")

        username_label = tk.Label(popup_frame, text="Username")
        username_label.grid(row=3, column=0, sticky="EW")
        username_entry = ttk.Entry(popup_frame, justify="center")
        username_entry.insert(0, popup_username_variable)
        username_entry.config(state='readonly')
        username_entry.grid(row=4, column=0, sticky="E")

        password_label = tk.Label(popup_frame, text="Password")
        password_label.grid(row=3, column=1, sticky="EW")
        password_entry = ttk.Entry(popup_frame, justify="center")
        password_entry.insert(0, popup_password_variable)
        password_entry.config(state='readonly')
        password_entry.grid(row=4, column=1, sticky="E")

        # Add buttons
        update_button = ttk.Button(popup_frame, text="Add Key", command=lambda: print("Key Updated"))
        update_button.grid(row=6, column=0, sticky="WE", pady=20)
        cancel_button = ttk.Button(popup_frame, text="Cancel", command=popup.destroy)
        cancel_button.grid(row=6, column=1, sticky="WE", pady=20)

    except IndexError:
        error_msg = "No key selected. Please select a key(row) to edit"
        error_window_popup(error_msg)
        print(error_msg)


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

    # # Configure columns to make sure they expand properly
    # popup_frame.grid_columnconfigure(0, weight=1)
    # popup_frame.grid_columnconfigure(1, weight=1)

    # Add widgets
    label_popup_label = tk.Label(popup_frame, text="Label")
    label_popup_label.grid(row=0, column=0, columnspan=2, sticky="EW")
    label_entry = ttk.Entry(popup_frame, textvariable=label_variable, justify="center")
    # label_entry.insert(0, "enter name)")
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
        error_msg = "Please fill all required field"
        error_window_popup(error_msg)

def delete_key_event():
    try:
        deleted_key = password_table.selection()[0]
        deleted_key_values = password_table.item(deleted_key, 'values')

        # remove key from treeview
        password_table.delete(deleted_key)

        # remove key from keychain key_list
        keychain.remove_key(int(deleted_key_values[0]))
    except IndexError:
        error_msg = "No key selected. Please select a key(row) to delete"
        error_window_popup(error_msg)
        print(error_msg)

def print_keychain():
    print("\n")
    for key in keychain.key_list:
        print(key.id, key.label, key.username, key.password)

# def show_context_menu(event):
#     try:
#         context_menu.post(event.x_root, event.y_root)
#     finally:
#         context_menu.grab_release()

def show_context_menu(event):
    # Identify the row where the right-click occurred
    selected_item = password_table.identify_row(event.y)

    if selected_item:
        # Select the row in the Treeview
        password_table.selection_set(selected_item)
        # Show the context menu at the right-click location
        context_menu.post(event.x_root, event.y_root)


def copy_to_clipboard(event):
    # Identify which row and column was right-clicked
    selected_item = password_table.identify_row(event.y)
    column = password_table.identify_column(event.x)
    col_index = int(column.split('#')[-1]) - 1

    if selected_item:
        # Get the text of the selected item and column
        item_text = password_table.item(selected_item, 'values')[col_index]

        # Copy the text to clipboard
        window.clipboard_clear()
        window.clipboard_append(item_text)
        window.update()  # Ensure clipboard content is updated
        messagebox.showinfo("Copied", "Text copied to clipboard")
    else:
        messagebox.showwarning("Error", "Unable to copy text.")


# def show_context_menu(event):
#     # Select the row under the cursor (right-clicked)
#     row_id = password_table.identify_row(event.y)
#     if row_id:
#         password_table.selection_set(row_id)
#         # Show context menu at the right-click location
#         context_menu.post(event.x_root, event.y_root)



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
password_table.column("label", width=230)
password_table.column("username", width=250)
password_table.column("password", width=250)

# Create context menu to handle right click copy to clipboard functionality
context_menu = tk.Menu(window, tearoff=False)
context_menu.add_command(label="Copy To Clipboard", command=lambda e: copy_to_clipboard(e))


#bind the right click (button 3) to show context menu
password_table.bind("<Button-2>", show_context_menu)

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

# if __name__ == "__main__":
#     keychain = Keychain()
#     # keychain.add_key("Google", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Bank of America", "dn52002@gmail.com", password_generator(20))
#     # keychain.add_key("Fidelity", "dn52002@gmail.com", password_generator(20))
#     if authenticate(keychain):
#         main()
