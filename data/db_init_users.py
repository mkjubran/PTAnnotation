import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# --- users table ---
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# --- label_events table ---
# stores one row per question/answer for a given (user, exercise, video)
c.execute("""
CREATE TABLE IF NOT EXISTS label_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise TEXT NOT NULL,
    video TEXT NOT NULL,
    question_name TEXT NOT NULL,   -- e.g., 'Q1'
    label_value INTEGER NOT NULL,  -- 0..5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# --- login_logs table ---
# stores all login attempts (success/failure)
c.execute("""
CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,              -- NULL if login failed
    username TEXT NOT NULL,
    success INTEGER NOT NULL,     -- 1 = success, 0 = failure
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()
print("users + label_events tables ensured.")

