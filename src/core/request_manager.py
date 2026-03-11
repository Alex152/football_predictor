import sqlite3
from datetime import datetime, timezone

DB_PATH = "data/football.db"

DAILY_LIMIT = 100


def init_request_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS api_requests (

        date TEXT PRIMARY KEY,
        requests_used INTEGER

    )

    """)

    conn.commit()
    conn.close()


def _get_today_utc():

    return datetime.now(timezone.utc).date().isoformat()


def register_request():

    today = _get_today_utc()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO api_requests (date, requests_used)
    VALUES (?, 1)

    ON CONFLICT(date)
    DO UPDATE SET requests_used = requests_used + 1

    """, (today,))

    conn.commit()
    conn.close()


def get_requests_today():

    today = _get_today_utc()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT requests_used FROM api_requests WHERE date=?",
        (today,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0


def get_requests_remaining():

    used = get_requests_today()

    remaining = DAILY_LIMIT - used

    if remaining < 0:
        remaining = 0

    return remaining


def can_make_request():

    remaining = get_requests_remaining()

    return remaining > 0


def print_request_status():

    used = get_requests_today()
    remaining = get_requests_remaining()

    print("API REQUEST STATUS")
    print("Requests used today:", used)
    print("Requests remaining:", remaining)