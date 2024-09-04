import json

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

# Convert the dictionary to a JSON string
json_str = json.dumps(data)

# Encode the JSON string to bytes
byte_data = json_str.encode()

# Write the bytes to a binary file
with open("password.bin", "wb") as file:
    file.write(byte_data)

print(byte_data)
