import sqlite3
from pathlib import Path

DB_PATH = Path("API/security/api_keys.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            owner TEXT,
            active BOOLEAN DEFAULT 1,
            requests_today INTEGER DEFAULT 0,
            last_reset TEXT
        )
        """)
        conn.commit()
