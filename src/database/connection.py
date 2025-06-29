'''
Database Manager - Stores all the security events
Like a filing cabinet that remembers everything!
'''

import sqlite3
import time
import json
from pathlib import Path
from utils.logger import setup_logger

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('DatabaseManager')
        self.db_path = config['path']
        
        # Create database directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.init_database()
        
    def init_database(self):
        '''Initialize the database with required tables'''
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        event_type TEXT NOT NULL,
                        event_data TEXT NOT NULL,
                        threat_score REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Alerts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_id INTEGER,
                        alert_type TEXT NOT NULL,
                        message TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        resolved BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (event_id) REFERENCES events (id)
                    )
                ''')
                
                # Agents table (for multi-agent deployments)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS agents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        agent_name TEXT UNIQUE NOT NULL,
                        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'active'
                    )
                ''')
                
                conn.commit()
                self.logger.info("✅ Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"❌ Error initializing database: {e}")
    
    def store_event(self, event_data, threat_score):
        '''Store an event in the database'''
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO events (timestamp, event_type, event_data, threat_score)
                    VALUES (?, ?, ?, ?)
                ''', (
                    event_data.get('timestamp', time.time()),
                    event_data.get('type', 'unknown'),
                    json.dumps(event_data),
                    threat_score
                ))
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            self.logger.error(f"❌ Error storing event: {e}")
            return None
    
    def store_alert(self, event_id, alert_type, message, severity='medium'):
        '''Store an alert in the database'''
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alerts (event_id, alert_type, message, severity)
                    VALUES (?, ?, ?, ?)
                ''', (event_id, alert_type, message, severity))
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            self.logger.error(f"❌ Error storing alert: {e}")
            return None
    
    def get_recent_events(self, limit=100):
        '''Get recent events from database'''
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM events 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                events = []
                for row in cursor.fetchall():
                    events.append({
                        'id': row[0],
                        'timestamp': row[1],
                        'event_type': row[2],
                        'event_data': json.loads(row[3]),
                        'threat_score': row[4],
                        'created_at': row[5]
                    })
                
                return events
                
        except Exception as e:
            self.logger.error(f"❌ Error getting events: {e}")
            return []
    
    def get_high_threat_events(self, threshold=0.7, limit=50):
        '''Get high-threat events'''
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM events 
                    WHERE threat_score > ?
                    ORDER BY threat_score DESC, timestamp DESC
                    LIMIT ?
                ''', (threshold, limit))
                
                events = []
                for row in cursor.fetchall():
                    events.append({
                        'id': row[0],
                        'timestamp': row[1],
                        'event_type': row[2],
                        'event_data': json.loads(row[3]),
                        'threat_score': row[4],
                        'created_at': row[5]  
                    })
                
                return events
                
        except Exception as e:
            self.logger.error(f"❌ Error getting high-threat events: {e}")
            return []