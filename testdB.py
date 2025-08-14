import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Fetch all rows from labels table
cursor.execute("SELECT * FROM labels")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

conn.close()

