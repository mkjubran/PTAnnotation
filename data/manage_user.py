# manage_user.py
import sqlite3
#import bcrypt
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

def add_or_update_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # hash password and convert to string
    #password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    password_hash = generate_password_hash(password)  # default is pbkdf2:sha256

    # check if user exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        c.execute("UPDATE users SET password_hash=? WHERE username=?", (password_hash, username))
        print(f"Password updated for user '{username}'")
    else:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        print(f"User '{username}' added")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add or update a user")
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    add_or_update_user(args.username, args.password)

