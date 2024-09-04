import json

data = {
    "users" : [
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

################ WRITE DATA TO JSON FILE ###################

with open("output.json", "w") as file:
    json.dump(data, file)



################ LOAD DATA FROM JSON FILE ##################

with open("names.json", "r") as file:
    data = json.load(file)
