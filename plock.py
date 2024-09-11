# # import pickle
# #
# # # Data to be pickled
# # data = {'name': 'John', 'age': 30, 'city': 'New York'}
# #
# # # Save the data to a file
# # with open('data.pkl', 'wb') as file:
# #     pickle.dump(data, file)
# #
# #
# # # Load the data from the file
# # with open('data.pkl', 'rb') as file:
# #     loaded_data = pickle.load(file)
# #
# # print(loaded_data)
#
# def edit_key_popup():
#     """Opens a custom pop-up window centered within the main window."""
#     popup = tk.Toplevel(window)  # Make the pop-up window a child of the main window
#     popup.title("Edit Key")
#
#     # Set the size of the pop-up window
#     popup_width = 450
#     popup_height = 300
#
#     # Get main window size and position
#     main_window_width = window.winfo_width()
#     main_window_height = window.winfo_height()
#     main_window_x = window.winfo_x()
#     main_window_y = window.winfo_y()
#
#     # Calculate position x, y to center the pop-up in the main window
#     position_x = main_window_x + (main_window_width // 2) - (popup_width // 2)
#     position_y = main_window_y + (main_window_height // 2) - (popup_height // 2)
#
#     # Set the geometry of the pop-up window
#     popup.geometry(f"{popup_width}x{popup_height}+{position_x}+{position_y}")
#
#     # Create a frame inside the pop-up
#     popup_frame = tk.Frame(popup)
#     popup_frame.pack()
#
#     # Get the selected row's Iid
#     edited_key = password_table.selection()[0]
#
#     # Get the values of the selected row
#     item_values = password_table.item(edited_key, 'values')
#
#     # Create new StringVar instances for each popup with the "popup_" prefix
#     popup_label_variable = tk.StringVar(value=item_values[1])
#     popup_username_variable = tk.StringVar(value=item_values[2])
#     popup_password_variable = tk.StringVar(value=item_values[3])
#
#     # Add widgets
#     label_popup_label = tk.Label(popup_frame, text="Label")
#     label_popup_label.grid(row=0, column=1, sticky="E")
#     label_entry = ttk.Entry(popup_frame, textvariable=popup_label_variable)
#     label_entry.config(textvariable=popup_label_variable)  # Configures the entry to use the updated variable
#     label_entry.grid(row=1, column=0, columnspan=2, sticky="WE")
#
#     label_popup_username = tk.Label(popup_frame, text="Username")
#     label_popup_username.grid(row=3, column=0, sticky="E")
#     username_entry = ttk.Entry(popup_frame, textvariable=popup_username_variable)
#     username_entry.config(textvariable=popup_username_variable)  # Configures the entry to use the updated variable
#     username_entry.grid(row=4, column=0, sticky="E")
#
#     label_popup_password = tk.Label(popup_frame, text="Password")
#     label_popup_password.grid(row=3, column=1, sticky="E")
#     password_entry = ttk.Entry(popup_frame, textvariable=popup_password_variable)
#     password_entry.config(textvariable=popup_password_variable)  # Configures the entry to use the updated variable
#     password_entry.grid(row=4, column=1, sticky="E")
