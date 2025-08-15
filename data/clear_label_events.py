#!/usr/bin/env python3
"""
Simple script to clean annotation data while preserving users
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

def clean_data():
    """Clean annotation data, preserve users"""
    
    if not os.path.exists(DB_PATH):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Get counts before cleaning
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM label_events")
        event_count = c.fetchone()[0]
        
        print(f"🔍 Found: {user_count} users, {event_count} annotations")
        
        # Clear only annotation data
        c.execute("DELETE FROM label_events")
        c.execute("DELETE FROM sqlite_sequence WHERE name='label_events'")
        
        conn.commit()
        
        # Verify results
        c.execute("SELECT COUNT(*) FROM users")
        remaining_users = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM label_events")
        remaining_events = c.fetchone()[0]
        
        print(f"✅ Cleaned: {event_count} annotations removed")
        print(f"🔒 Preserved: {remaining_users} users")
        print("✨ Data cleaning complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clean_data()
