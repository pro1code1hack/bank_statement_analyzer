import hashlib

users_db = {}
current_user = None


def register(username, password):
    if username in users_db:
        raise ValueError("User already exists")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users_db[username] = hashed_password

    print("User registered successfully")


def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if users_db.get(username) != hashed_password:
        print("Invalid credentials")
        return

    global current_user
    current_user = username

    print("Login successful")


def logout():
    global current_user

    if current_user:
        print(f"User {current_user} logged out successfully")
        current_user = None
    else:
        print("No user is currently logged in")


def get_current_user():
    return current_user
