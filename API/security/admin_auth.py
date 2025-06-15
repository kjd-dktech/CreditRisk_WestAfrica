from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

MASTER_SECRET = os.getenv("MASTER_SECRET")

def verify_admin(x_admin_secret: str = Header(...)):
    if x_admin_secret != MASTER_SECRET:
        raise HTTPException(status_code=403, detail="Accès admin refusé")
    return True
