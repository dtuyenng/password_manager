import json

class TestKey:
    def __init__(self, username, password):
        self.username = username
        self.password = password


my_key = TestKey("tuyen", "password123")
my_key_dict = my_key.__dict__

my_key_json = json.dumps(my_key_dict)


with open("key_data.json", "w") as file:
    json.dump(my_key_dict, file)

print(my_key_dict)