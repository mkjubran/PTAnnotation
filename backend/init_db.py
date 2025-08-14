import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# Drop the table if it exists
cursor.execute("DROP TABLE IF EXISTS labels")

# Create table with the correct schema
cursor.execute("""
CREATE TABLE labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    question TEXT NOT NULL
)
""")

# Insert Q1 to Q10
labels = [
    ("Q1", "Is the primary objective of the exercise achieved (i.e., extension of the upper limbs, trunk rotation with upper limbs elevated to 90◦ , squatting, etc.) ?"),
    ("Q2", "Is the exercise repeated in a constant manner?"),
    ("Q3", "Is the amplitude of the movement complete?"),
    ("Q4", "Is the posture of the head correct?"),
    ("Q5", "Is the posture of the right arm correct?"),
    ("Q6", "Is the posture of the left arm correct?"),
    ("Q7", "Is the posture of the trunk correct?"),
    ("Q8", "Is the posture of the pelvis correct?"),
    ("Q9", "Is the posture of the right leg correct?"),
    ("Q10", "Is the posture of the left leg correct?")
]
cursor.executemany(
    "INSERT INTO labels (name, question) VALUES (?, ?)",
    labels
)

conn.commit()
conn.close()
print("Database initialized successfully.")

