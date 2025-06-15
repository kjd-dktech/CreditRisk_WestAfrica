from fastapi import APIRouter, HTTPException, Depends
from API.security.database import get_db_connection
from API.security.admin_auth import verify_admin
import secrets
from datetime import date

router = APIRouter()

@router.post("/create-key")
def create_api_key(admin: bool = Depends(verify_admin)):
    key = secrets.token_hex(16)
    today = str(date.today())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO api_keys (key, active, requests_today, last_reset)
            VALUES (?, ?, ?, ?)
        """, (key, True, 0, today))
        conn.commit()
    return {"message": "✅ Clé API générée", "api_key": key}


@router.post("/disable-key")
def disable_key(key: str, admin: bool = Depends(verify_admin)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM api_keys WHERE key = ?", (key,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Clé non trouvée")
        
        cursor.execute("UPDATE api_keys SET active = 0 WHERE key = ?", (key,))
        conn.commit()
    return {"message": "🔒 Clé désactivée avec succès", "disabled_key": key}
