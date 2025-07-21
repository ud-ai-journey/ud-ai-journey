import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

class DataManager:
    def __init__(self, db_path="energy_lens.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create energy_records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                energy_level TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'auto'
            )
        ''')
        
        # Create productivity_events table for future calendar integration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productivity_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_name TEXT,
                start_time DATETIME,
                end_time DATETIME,
                energy_before REAL,
                energy_after REAL,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_energy_record(self, energy_level, confidence, source="auto"):
        """Save an energy record to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO energy_records (energy_level, confidence, source)
            VALUES (?, ?, ?)
        ''', (energy_level, confidence, source))
        
        conn.commit()
        conn.close()
    
    def get_energy_data(self, days=30):
        """Get energy data for the last N days"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT energy_level, confidence, timestamp, source
            FROM energy_records
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
        
        return df
    
    def get_today_data(self):
        """Get energy data for today"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT energy_level, confidence, timestamp, source
            FROM energy_records
            WHERE date(timestamp) = date('now')
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def get_weekly_data(self):
        """Get energy data for the current week"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT energy_level, confidence, timestamp, source
            FROM energy_records
            WHERE timestamp >= datetime('now', '-7 days')
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            df['day_of_week'] = df['timestamp'].dt.day_name()
        
        return df
    
    def get_energy_stats(self, days=30):
        """Get statistical summary of energy data"""
        df = self.get_energy_data(days)
        
        if df.empty:
            return {}
        
        stats = {
            'total_records': len(df),
            'avg_confidence': df['confidence'].mean(),
            'energy_distribution': df['energy_level'].value_counts().to_dict(),
            'most_common_energy': df['energy_level'].mode().iloc[0] if not df.empty else None,
            'high_energy_percentage': (df['energy_level'] == 'High').mean() * 100,
            'low_energy_percentage': (df['energy_level'] == 'Low').mean() * 100
        }
        
        return stats
    
    def get_hourly_patterns(self):
        """Get energy patterns by hour of day"""
        df = self.get_energy_data(7)  # Last 7 days
        
        if df.empty:
            return pd.DataFrame()
        
        hourly_patterns = df.groupby(['hour', 'energy_level']).size().unstack(fill_value=0)
        return hourly_patterns
    
    def get_weekly_patterns(self):
        """Get energy patterns by day of week"""
        df = self.get_energy_data(30)  # Last 30 days
        
        if df.empty:
            return pd.DataFrame()
        
        weekly_patterns = df.groupby(['day_of_week', 'energy_level']).size().unstack(fill_value=0)
        return weekly_patterns
    
    def delete_old_records(self, days=90):
        """Delete records older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM energy_records
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def export_data(self, format='csv'):
        """Export energy data"""
        df = self.get_energy_data()
        
        if df.empty:
            return None
        
        if format == 'csv':
            filename = f"energy_lens_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            return filename
        elif format == 'json':
            filename = f"energy_lens_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            df.to_json(filename, orient='records', date_format='iso')
            return filename
        
        return None 