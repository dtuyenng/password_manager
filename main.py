from Keychain import *
from password_generator import password_generator
import tkinter as tk
from data_path import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

"""

TODO:
    - change name of the app using pyinstaller --windowed --name="My Password Manager" main.py
    - implement separator in Treeview using blank rows
    - implement reordering single row using two buttons on the side of the Treeview
    - the encryption password and salt are hard-coded. Take them out
    
Optimization:   
    - load_key on startup could use some refinements, could for example rename it so it isn't implied to be 
    only used during startup
    - import/export reusing multiple code fragments, need to clean that up
    

Bugs:
    - pyinstaller using --onefile not working, keys arent saved. Something with the paths
    --windowed works though. Some reasons, in mac, pyinstaller STILL create a single file executable s
    that's ok...
    
"""

def close_app():
    root.destroy()
    messagebox.showinfo("Timed Out", "App timed out due to inactivity.")

def reset_timer(event=None):
    root.after_cancel(timer)
    start_timer()

def start_timer():
    global timer
    timer = root.after(60000, close_app)

def load_file():
    file_path = filedialog.askopenfilename(
        title="Choose Keychain  File",
        filetypes=[("Binary", "*.bin"), ("All Files", "*.*")]
    )
    print(file_path)

    if file_path:
        print(f"Selected file: {file_path}")

        try:
            # Open and read the binary file
            with open(file_path, 'rb') as file:
                binary_data = file.read()
                decrypted_data = json.loads(decrypt(binary_data).decode("utf-8"))

                keychain.remove_allkeys()
                keychain.set_password(decrypted_data["password"])
                for key in decrypted_data["key_list"]:
                    keychain.add_key(key["label"], key["username"], key["password"])
            load_keys_on_startup()
        except Exception as e:
            print(f"Error loading file: {e}")

def save_file():
    try:
        file = filedialog.asksaveasfile(mode="wb", defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        file.write(keychain.save_keychain_to_file())
        file.close()
    except AttributeError:
        print("AttributeError")

def authenticate_user(window):

    allowed_tries = tk.IntVar(value=3)

    # If no password is set, prompt user to set new password
    if keychain.get_password() == "":
        # print("Debug: No Password Was Set")
        load_keys_on_startup()
        main_frame.pack(pady=20)
        bottom_frame.pack()
        menu_edit_password()
        return

    authenticate_window = tk.Tk()
    authenticate_window.title("Authenticate User")
    authenticate_window.resizable(False, False)

    # Set the size of the pop-up window
    width = 350
    height = 210

    # Center the pop-up window
    center_window(authenticate_window, width, height)

    def check_authentication():
        entered_password = input_password.get()

        if allowed_tries.get() > 0:

            if allowed_tries.get() > 1:
                warning_label.config(text=f"Tries Left: {allowed_tries.get()}")
            else:
                warning_label.config(text="Last Chance Before Keychain Destruction.")
            allowed_tries.set(allowed_tries.get() - 1)
            input_password.delete(0, tk.END)
            input_password.focus()

            if entered_password == keychain.get_password():
                print("User Authenticated")
                emoji_label.destroy()
                load_keys_on_startup()
                keychain.save_keychain(get_save_path("data.bin"))
                authenticate_window.destroy()
                main_frame.pack(pady=20)
                bottom_frame.pack()
                start_timer() # timer to auto close up after a certain time
        else:
            print("Authentication Failed")

            # Resetting Password and Destroying Keychain
            keychain.key_list = []
            keychain.set_password("")
            keychain.save_keychain(get_save_path("data.bin"))

            root.destroy()
            authenticate_window.destroy()



    # Set the widgets
    emoji_label = tk.Label(authenticate_window, text="🔐", font=("Arial", 50), fg="white")
    emoji_label.pack()

    label = ttk.Label(authenticate_window, text="Enter Password", anchor="center")
    label.pack(side="top", fill="x", padx=5)

    input_password = ttk.Entry(authenticate_window, justify="center", show="*")
    input_password.pack(side="top", fill="x", padx=5)
    input_password.focus()  # Set focus on the entry widget

    button = ttk.Button(authenticate_window, text="Submit", command=check_authentication)
    button.pack(side="top", fill="x", padx=5)

    warning_label = ttk.Label(authenticate_window, text="")
    warning_label.pack()


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
            keychain.save_keychain(get_save_path("data.bin"))
            messagebox.showinfo("Password Changed", "Password has been changed")
            popup.destroy()

    popup = tk.Toplevel(root)  # Make the pop-up window a child of the main window
    popup.title("Set Keychain Password")
    popup.resizable(False, False)

    # Set the size of the pop-up window
    width = 350
    height = 200

    # Centering window function
    center_window(popup, width, height)

    label = ttk.Label(popup, text="Enter Password")
    label.pack(side="top", expand=True, )

    input1 = ttk.Entry(popup, textvariable=passwordVar1, justify="center", show="*")
    input1.pack(side="top", expand=True)
    input2 = ttk.Entry(popup, textvariable=passwordVar2, justify="center", show="*")
    input2.pack(side="top", expand=True)

    label_error_warning = ttk.Label(popup, textvariable=warning_msg)
    label_error_warning.pack(side="top", expand=True)

    set_button = ttk.Button(popup, text="Set Password", command=set_password)
    set_button.pack(side="top", expand=True)

def edit_key_popup():

    """
    Strange bug issue, the StringVar varibles won't display in entry unless one of the button calls their
    get() methods in the command: parameters

    """
    try:
        # Setting up data needed. This will fail if nothing is selected
        edited_key = password_table.selection()[0]
        item_values = password_table.item(edited_key, 'values')

        popup = tk.Toplevel(root)  # Make the pop-up window a child of the main window
        popup.title("Edit Key")
        popup.resizable(False, False)

        # Set the size of the pop-up window
        width = 600
        height = 350

        # Center the pop-up window
        center_window(popup, width, height)

        # Create a frame inside the pop-up
        popup_frame = tk.Frame(popup)
        popup_frame.pack(pady=20)

        new_id = int(item_values[0])
        popup_label_variable = tk.StringVar(value=item_values[1])
        popup_username_variable = tk.StringVar(value=item_values[2])
        popup_password_variable = tk.StringVar(value=item_values[3])

        def keychain_password_update():
            # Note: for some reasons, without these prints, the StringVars don't display properly
            print(f"id: {new_id}")
            print(f"Label: {popup_label_variable.get()}")
            print(f"Username: {popup_username_variable.get()}")
            print(f"Password: {popup_password_variable.get()}")

            result = messagebox.askyesno("Confirm", "Update Key?")
            if result:
                keychain.modify_key(id=new_id, label=popup_label_variable.get(), username=popup_username_variable.get(), password=popup_password_variable.get())
                password_table.item(edited_key, values=(new_id, popup_label_variable.get(), popup_username_variable.get(), popup_password_variable.get()))

                print("Password has been changed")
                # reload_treeview(password_table)
                popup.destroy()

        # # Debugging: Check if the variables hold correct values
        # print(f"Label: {popup_label_variable.get()}")
        # print(f"Username: {popup_username_variable.get()}")
        # print(f"Password: {popup_password_variable.get()}")


        # Add widgets
        label_label = tk.Label(popup_frame, text="Label")
        label_label.grid(row=0, column=0, columnspan=2, sticky="EW")
        label_entry = ttk.Entry(popup_frame, justify="center", textvariable=popup_label_variable)
        # label_entry.insert(0, popup_label_variable.get())
        label_entry.grid(row=1, column=0, columnspan=2, sticky="EW")
        print(popup_label_variable.get())

        username_label = tk.Label(popup_frame, text="Username")
        username_label.grid(row=3, column=0, sticky="EW")
        username_entry = ttk.Entry(popup_frame, justify="center", textvariable=popup_username_variable)
        # username_entry.insert(0, popup_username_variable.get())
        username_entry.grid(row=4, column=0, sticky="E")

        password_label = tk.Label(popup_frame, text="Password")
        password_label.grid(row=3, column=1, sticky="EW")
        password_entry = ttk.Entry(popup_frame, justify="center", textvariable=popup_password_variable)
        # password_entry.insert(0, popup_password_variable.get())
        password_entry.grid(row=4, column=1, sticky="E")

        # Add buttons
        generate_password_button = ttk.Button(popup_frame, text="Generate Random", width=2, command=lambda: popup_password_variable.set(password_generator(20)))
        generate_password_button.grid(row=5, column=1, sticky="NSEW")

        update_button = ttk.Button(popup_frame, text="Update Key", command=keychain_password_update)
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


    popup = tk.Toplevel(root)  # Make the pop-up window a child of the main window
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
    # Delete all items in the Treeview
    for item in password_table.get_children():
        password_table.delete(item)

    for key in keychain.key_list:
        new_key = (key.id, key.label, key.username, key.password)
        password_table.insert(parent="", index=key.id, values=new_key)

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

        result = messagebox.askokcancel("Delete Key", "Are you sure you want to delete this key?")
        if result:
            # remove key from treeview
            password_table.delete(deleted_key)

            # remove key from keychain key_list using the id of the key
            keychain.remove_key(int(deleted_key_values[0]))

    except IndexError:
        error_msg = "No key selected."
        messagebox.showwarning("Attention!", error_msg)
        print(error_msg)

def print_keychain():
    print(keychain.key_list)
    print("\n")
    print(keychain.get_password())
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
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(cell_value)  # Append the copied cell value
    print(cell_value)
    # messagebox.showinfo("Copied", f"Copied: {cell_value}")

def show_context_menu(event):
    # Only show the context menu if the right-click is over a valid item
    item_id = password_table.identify_row(event.y)
    if item_id:
        context_menu.post(event.x_root, event.y_root)

################################# TKINTER ##################################

keychain = Keychain()


root = tk.Tk()
root.title("My Password Manager")
center_window(root, 800, 500)
root.resizable(False, False)

# Bind key and mouse events to reset the inactivity timer
root.bind_all("<KeyPress>", reset_timer)
root.bind_all("<Motion>", reset_timer)

emoji_label = tk.Label(root, text="🔐")

################################# Menu ##################################

# Create Menu Bar
menu = tk.Menu(root)
root.config(menu=menu)

#Create Menu Items

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Import Keychain", command = load_file)
file_menu.add_command(label="Export Keychain...", command = save_file)
file_menu.add_separator()
file_menu.add_command(label="Set Password...", command = menu_edit_password)
file_menu.add_separator()
file_menu.add_command(label="Debug: Print Keychain", command = print_keychain)
file_menu.add_command(label="Quit Password Manager", command = root.quit)
# main_frame.pack(pady=20)

############################## MAIN FRAME #################################

main_frame = tk.Frame(root)
# main_frame.pack(pady=20) #packing it during authentication

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
context_menu = tk.Menu(root, tearoff=0)
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
bottom_frame = tk.Frame(root)
# bottom_frame.pack() # packing in during authentication

delete_button = ttk.Button(bottom_frame, text="Delete", command=delete_key_event)
delete_button.pack(side="right", padx=10)

edit_button = ttk.Button(bottom_frame, text="Edit", command=edit_key_popup)
edit_button.pack(side="right", padx=10)

add_button = ttk.Button(bottom_frame, text="Add", command=add_key_popup)
add_button.pack(side="right",  padx=10)

authenticate_user(root)
root.mainloop()
keychain.save_keychain(get_save_path("data.bin")) #Save keychain when app quits
