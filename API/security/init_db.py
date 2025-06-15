import sqlite3

conn = sqlite3.connect("API/security/api_keys.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    owner TEXT,
    active INTEGER DEFAULT 1,
    requests_today INTEGER DEFAULT 0,
    last_reset TEXT
)
""")

conn.commit()
conn.close()

print("✅ Table `api_keys` créée avec succès.")
