import sqlite3
import os
import csv
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
c.execute("""
CREATE TABLE IF NOT EXISTS login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT NOT NULL,
    success INTEGER NOT NULL,
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
print("users + label_events + login_logs tables ensured.")

# ==================== PRINT DATABASE CONTENT ====================

def export_table_to_csv(cursor, table_name, output_dir="csv_exports"):
    """Export table content to CSV file"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    if not columns:
        print(f"Table '{table_name}' does not exist or has no columns.")
        return None
    
    col_names = [col[1] for col in columns]
    
    # Get all rows
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Create CSV filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = os.path.join(output_dir, f"{table_name}_{timestamp}.csv")
    
    # Write to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(col_names)
        
        # Write data rows
        writer.writerows(rows)
    
    print(f"✅ Exported {len(rows)} rows to: {csv_filename}")
    return csv_filename

def print_table_content(cursor, table_name, export_csv=True):
    """Print all content from a given table and optionally export to CSV"""
    print(f"\n{'='*50}")
    print(f"TABLE: {table_name.upper()}")
    print('='*50)
    
    # Get table info (column names and types)
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    if not columns:
        print(f"Table '{table_name}' does not exist or has no columns.")
        return
    
    # Print column headers
    col_names = [col[1] for col in columns]  # col[1] is the column name
    col_types = [col[2] for col in columns]  # col[2] is the column type
    
    print("Columns:")
    for name, col_type in zip(col_names, col_types):
        print(f"  - {name} ({col_type})")
    print()
    
    # Get all rows
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if not rows:
        print("No data in this table.")
        if export_csv:
            print("⚠️  Skipping CSV export (no data)")
        return
    
    # Print header row
    header = " | ".join(f"{name:15}" for name in col_names)
    print(header)
    print("-" * len(header))
    
    # Print first 10 rows (limit console output)
    display_rows = rows[:10]
    for row in display_rows:
        row_str = " | ".join(f"{str(val):15}" for val in row)
        print(row_str)
    
    if len(rows) > 10:
        print(f"... and {len(rows) - 10} more rows (see CSV export for full data)")
    
    print(f"\nTotal rows: {len(rows)}")
    
    # Export to CSV
    if export_csv:
        export_table_to_csv(cursor, table_name)

def print_database_summary():
    """Print a summary of all tables in the database"""
    print(f"\n{'='*60}")
    print("DATABASE SUMMARY")
    print('='*60)
    
    # Get all table names
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    
    print(f"Database path: {DB_PATH}")
    print(f"Total tables: {len(tables)}")
    
    for table in tables:
        table_name = table[0]
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
        print(f"  - {table_name}: {count} rows")

# Print database summary
print_database_summary()

# Print content of each table and export to CSV
tables_to_print = ['users', 'label_events', 'login_logs']
exported_files = []

print(f"\n{'='*60}")
print("EXPORTING TABLES TO CSV")
print('='*60)

for table_name in tables_to_print:
    print_table_content(c, table_name, export_csv=True)

# Optional: Print any other tables that might exist
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [table[0] for table in c.fetchall()]
other_tables = [t for t in all_tables if t not in tables_to_print]

if other_tables:
    print(f"\n{'='*50}")
    print("OTHER TABLES FOUND:")
    print('='*50)
    for table_name in other_tables:
        print_table_content(c, table_name, export_csv=True)

print(f"\n{'='*60}")
print("EXPORT COMPLETE!")
print('='*60)
print("📁 CSV files have been saved to the 'csv_exports' folder")
print("📊 You can open these files in Excel, Google Sheets, or any CSV viewer")

conn.close()
