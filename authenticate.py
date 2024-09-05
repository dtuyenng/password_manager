def authenticate(keychain) -> bool:
    max_attempt = 3
    while max_attempt > 0:
        password_input = input("Enter Password: ")
        if password_input == keychain.password:
            return True
        else:
            max_attempt -= 1
    print("Too many attempts.")
    return False