from fastapi import APIRouter, HTTPException, Request
import secrets, os, json, sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv
from API.config.logging_config import logger

from .database import get_db_connection

#DB_PATH = os.path.join(os.path.dirname(__file__), "api_keys.db")

router = APIRouter()

load_dotenv()

#API_KEYS_DB = {}  # Simule une base de données

MASTER_SECRET = os.getenv("MASTER_SECRET")

@router.post("/get-api-key")
def get_api_key(request: Request):

    data = request.query_params
    logger.info("🔑 Demande de clé API reçue.")

    try :
        if data.get("admin_password") != MASTER_SECRET:
            logger.error("❌ Mot de passe administrateur incorrect.")
            raise HTTPException(status_code=401, detail="Unauthorized")

        new_key = secrets.token_hex(16)        

        def ensure_table_exists():
            #conn = sqlite3.connect(DB_PATH)
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Vérifie si la table api_keys existe
                cursor.execute("""
                    SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'
                """)
                result = cursor.fetchone()
                
                # Si non, on la crée
                if result is None:
                    logger.info("⚠️ Table `api_keys` non trouvée. Création en cours...")
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
                    logger.info("✅ Table `api_keys` créée.")

        # Appel au démarrage du module
        ensure_table_exists()

        # Enregistrement dans la base de données
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_keys (key, owner, last_reset)
                VALUES (?, ?, ?)
            """, (new_key, data.get("owner", "anonymous"), datetime.now(timezone.utc).isoformat()))
        logger.success(f"✅ Nouvelle clé API générée : {new_key}")
        return {"api_key": new_key}
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération de la clé API : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
