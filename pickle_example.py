

data = {
    "users": [
        {
            "fname": "Tuyen",
            "lname": "Nguyen",
        },
        {
            "fname": "Vinh",
            "lname": "Nguyen",
        },
    ],
}

# Write binary data using pickle
with open("users.pkl", "wb") as file:
    pickle.dump(data, file)

# Read binary data using pickle
with open("users.pkl", "rb") as file:
    loaded_data = pickle.load(file)

print(loaded_data)