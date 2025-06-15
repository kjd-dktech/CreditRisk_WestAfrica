import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

def send_email_alert(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = os.getenv("EMAIL_RECEIVER")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        logger.warning(f"Email alert failed: {e}")
