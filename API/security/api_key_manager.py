from fastapi import Header, HTTPException
from datetime import date, datetime 
from .database import get_db_connection

DAILY_LIMIT = 50


def ensure_table_exists(cursor):
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


def verify_api_key(x_api_key: str = Header(...)):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # S'assurer que la table existe
        ensure_table_exists(cursor)

        # Vérification de la clé API
        cursor.execute("""
            SELECT id, active, requests_today, last_reset
            FROM api_keys WHERE key = ?
        """, (x_api_key,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=403, detail="❌ Clé API invalide")

        key_id, active, requests_today, last_reset = row

        if not active:
            raise HTTPException(status_code=403, detail="🔒 Clé API désactivée")

        today = str(date.today())

        if last_reset != today:
            # Reset compteur
            cursor.execute("""
                UPDATE api_keys
                SET requests_today = 0, last_reset = ?
                WHERE id = ?
            """, (today, key_id))
            requests_today = 0

        if requests_today >= DAILY_LIMIT:
            raise HTTPException(status_code=429, detail="⛔ Limite quotidienne atteinte")

        # Incrémentation
        cursor.execute("""
            UPDATE api_keys SET requests_today = requests_today + 1
            WHERE id = ?
        """, (key_id,))
        conn.commit()
