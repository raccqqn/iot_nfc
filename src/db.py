import sqlite3
import time
from pathlib import Path

# Pfad zur DB
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DB_PATH = PROJECT_ROOT / "data" / "flaschen_database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_next_free_bottle():
    """
    Returns the Flaschen_ID of the first bottle
    that has not yet been tagged.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Flaschen_ID
        FROM Flasche
        WHERE (Tagged_Date IS NULL OR Tagged_Date = 0)
          AND (has_error IS NULL OR has_error = 0)
        ORDER BY Flaschen_ID
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return row[0]


def mark_bottle_as_tagged(flaschen_id):
    """
    Sets Tagged_Date to current unix timestamp
    """
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = int(time.time())

    cursor.execute("""
        UPDATE Flasche
        SET Tagged_Date = ?
        WHERE Flaschen_ID = ?
    """, (timestamp, flaschen_id))

    conn.commit()
    conn.close()
