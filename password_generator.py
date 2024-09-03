import random, string

def password_generator (password_length: int) -> str:

    # Generate a random password with a specified length.
    # The password includes letters, numbers, and symbols in the ratio 3:2:1.
    #
    # Args:
    # - password_length (int): The desired length of the password.
    #
    # Returns:
    # - str: The generated password.

    letters = (string.ascii_letters.
               replace("O", "").  #removing easily misread chars
               replace("o", "").
               replace("I", "").
               replace("l", "")
               )
    numbers = string.digits.replace("0", "")
    symbols = "$%#&^*-"

    # initiate password as an empty list
    pwd = []


    # The following part proportionally allocates password length according
    # to a set ratio to number of letters, number of numbers, and
    # numbers of symbols.Any remaining number is allocated to number of letters.

    # Define the ratio
    total_ratio = 3 + 2 + 1

    # Calculate the number of each type of character
    num_letters = (password_length * 3) // total_ratio
    num_numbers = (password_length * 2) // total_ratio
    num_symbols = (password_length * 1) // total_ratio

    # Handle any remaining characters
    total_allocated = num_letters + num_numbers + num_symbols
    if password_length - total_allocated > 0:
        num_letters += (password_length - total_allocated)

    # Generate the password following the ratio
    for _ in range(0, num_letters):
        pwd.append(random.choice(letters))
    for _ in range(0, num_numbers):
        pwd.append(random.choice(numbers))
    for _ in range(0, num_symbols):
        pwd.append(random.choice(symbols))

    # Shuffle and return the password as a string
    random.shuffle(pwd)
    return "".join(pwd)