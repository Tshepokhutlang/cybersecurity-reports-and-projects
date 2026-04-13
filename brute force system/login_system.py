# Simple Test Login System (Local Only)

USERNAME = "admin"
PASSWORD = "tshepo123"

def login(username, password):
    if username == USERNAME and password == PASSWORD:
        return True
    else:
        return False