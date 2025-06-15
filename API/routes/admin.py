from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends
from API.config.logging_config import logger
from API.security.database import get_db_connection
from API.security.admin_auth import verify_admin

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
def dashboard_html(admin: bool = Depends(verify_admin)):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, key, active, requests_today, last_reset FROM api_keys")
        rows = cursor.fetchall()

    html_rows = ""
    for id_, key, active, reqs, reset in rows:
        status = "🟢" if active else "🔴"
        html_rows += f"""
            <tr>
                <td>{id_}</td>
                <td>{key}</td>
                <td>{status}</td>
                <td>{reqs}</td>
                <td>{reset}</td>
            </tr>
        """

    html = f"""
    <html>
        <head>
            <title>Admin Dashboard - Clés API</title>
            <style>
                body {{ font-family: sans-serif; padding: 1rem; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>🔐 Dashboard Clés API</h1>
            <table>
                <tr>
                    <th>ID</th><th>Clé</th><th>Statut</th><th>Requêtes aujourd'hui</th><th>Dernier reset</th>
                </tr>
                {html_rows}
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
