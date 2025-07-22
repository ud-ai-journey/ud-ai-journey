import sqlite3
import pandas as pd
from datetime import datetime

def test_database():
    """Test if database is working properly"""
    
    # Test database connection
    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {tables}")
        
        # Check users table
        cursor.execute("SELECT * FROM users LIMIT 5")
        users = cursor.fetchall()
        print(f"Users: {users}")
        
        # Check energy_data table
        cursor.execute("SELECT * FROM energy_data LIMIT 5")
        energy_data = cursor.fetchall()
        print(f"Energy data: {energy_data}")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False

if __name__ == "__main__":
    test_database() 