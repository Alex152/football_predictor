import sqlite3

from src.utils.time_utils import match_already_finished
from src.core.priority_manager import get_country_priority, get_league_priority
from src.config.settings import DATABASE_PATH


def match_already_analyzed(fixture_id):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM analyzed_matches WHERE fixture_id = ?",
        (fixture_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def mark_match_analyzed(fixture_id):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO analyzed_matches (fixture_id, analyzed_at)
        VALUES (?, datetime('now'))
        """,
        (fixture_id,)
    )

    conn.commit()
    conn.close()


def get_candidate_matches():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
    fixture_id,
    date,
    time,
    league_id,
    league_name,
    country,
    home_team,
    away_team

    FROM matches

    """)

    rows = cursor.fetchall()

    conn.close()

    matches = []

    for row in rows:

        match = {

            "fixture_id": row[0],
            "date": row[1],
            "time": row[2],
            "league_id": row[3],
            "league_name": row[4],
            "country": row[5],
            "home_team": row[6],
            "away_team": row[7]

        }

        # evitar partidos ya terminados
        if match_already_finished(match["date"], match["time"]):
            continue

        # evitar partidos ya analizados
        if match_already_analyzed(match["fixture_id"]):
            continue

        country_score = get_country_priority(match["country"])

        league_score = get_league_priority(
            match["country"],
            match["league_name"]
        )

        priority_score = country_score * 10 + league_score

        match["priority"] = priority_score

        matches.append(match)

    matches.sort(key=lambda x: x["priority"])

    return matches


def select_top_matches(limit=40):

    matches = get_candidate_matches()

    return matches[:limit]