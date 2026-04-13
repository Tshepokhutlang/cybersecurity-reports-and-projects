import time
from login_system import login

username = "admin"

with open("passwords.txt", "r") as file:
    passwords = file.readlines()

attempts = 0

for password in passwords:

    password = password.strip()
    attempts += 1

    print("Trying:", password)

    time.sleep(1)

    if login(username, password):

        print("\nPassword found:", password)
        print("Total attempts:", attempts)
        break

else:
    print("\nPassword not found")