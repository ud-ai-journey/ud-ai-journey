import streamlit as st
import sqlite3
import hashlib
import json
from datetime import datetime
import os
import pandas as pd

class AuthSystem:
    def __init__(self):
        self.db_path = "user_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database with users and energy_data tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Energy data table with user_id foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                energy_level TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hour INTEGER,
                day_of_week TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_email(self, email):
        """Create a hash of email for session management"""
        return hashlib.md5(email.encode()).hexdigest()
    
    def login_user(self, email, name=None):
        """Login user and create/update session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            user_id, existing_name = user
            # Update last login
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
            name = existing_name or name
        else:
            # Create new user
            cursor.execute(
                "INSERT INTO users (email, name) VALUES (?, ?)", 
                (email, name or email.split('@')[0])
            )
            user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        # Set session state
        st.session_state['user_id'] = user_id
        st.session_state['user_email'] = email
        st.session_state['user_name'] = name
        st.session_state['is_authenticated'] = True
        
        return user_id
    
    def logout_user(self):
        """Logout user and clear session"""
        for key in ['user_id', 'user_email', 'user_name', 'is_authenticated']:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self):
        """Get current user info from session"""
        if st.session_state.get('is_authenticated'):
            return {
                'id': st.session_state.get('user_id'),
                'email': st.session_state.get('user_email'),
                'name': st.session_state.get('user_name')
            }
        return None
    
    def save_energy_record(self, energy_level, confidence):
        """Save energy record for current user"""
        user = self.get_current_user()
        if not user:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now()
        hour = timestamp.hour
        day_of_week = timestamp.strftime('%A')
        
        cursor.execute('''
            INSERT INTO energy_data (user_id, energy_level, confidence, timestamp, hour, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user['id'], energy_level, confidence, timestamp, hour, day_of_week))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_energy_data(self):
        """Get energy data for current user"""
        user = self.get_current_user()
        if not user:
            return pd.DataFrame()
        
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT energy_level, confidence, timestamp, hour, day_of_week
            FROM energy_data 
            WHERE user_id = ?
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=[user['id']])
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        return df
    
    def get_user_stats(self):
        """Get user statistics"""
        user = self.get_current_user()
        if not user:
            return {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute('''
            SELECT COUNT(*), AVG(confidence), 
                   SUM(CASE WHEN energy_level = 'High' THEN 1 ELSE 0 END) as high_count,
                   SUM(CASE WHEN energy_level = 'Medium' THEN 1 ELSE 0 END) as medium_count,
                   SUM(CASE WHEN energy_level = 'Low' THEN 1 ELSE 0 END) as low_count
            FROM energy_data 
            WHERE user_id = ?
        ''', (user['id'],))
        
        stats = cursor.fetchone()
        conn.close()
        
        if stats and stats[0] > 0:
            total, avg_confidence, high_count, medium_count, low_count = stats
            high_percentage = (high_count / total) * 100 if total > 0 else 0
            
            return {
                'total_readings': total,
                'avg_confidence': avg_confidence or 0,
                'high_energy_percentage': high_percentage,
                'high_count': high_count,
                'medium_count': medium_count,
                'low_count': low_count
            }
        
        return {} 