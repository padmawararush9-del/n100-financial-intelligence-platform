from fastapi import APIRouter
from ..database import get_connection
import time

router = APIRouter()

START_TIME = time.time()


@router.get("/health")
def health():
    """Health check endpoint."""

    conn = get_connection()

    cursor = conn.cursor()

    tables = cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()

    counts = {}

    for table in tables:
        table_name = table["name"]

        counts[table_name] = cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

    conn.close()

    return {
        "status": "ok",
        "db_row_counts": counts,
        "uptime_seconds": round(
            time.time() - START_TIME,
            2,
        ),
        "version": "1.0.0",
    }