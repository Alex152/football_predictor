import requests
import sqlite3
from datetime import datetime

from src.config.settings import API_KEY


BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def get_selected_leagues():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT DISTINCT m.league_id

    FROM matches m
    INNER JOIN selected_matches s
    ON m.fixture_id = s.fixture_id

    """)

    leagues = [row[0] for row in cursor.fetchall()]

    conn.close()

    return leagues


def standings_exist(league_id, season):

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT 1 FROM league_standings_history
    WHERE league_id=? AND season=?
    LIMIT 1

    """, (league_id, season))

    result = cursor.fetchone()

    conn.close()

    return result is not None


def fetch_standings(league_id, season):

    url = f"{BASE_URL}/standings"

    params = {
        "league": league_id,
        "season": season
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Error API:", response.status_code)
        return []

    data = response.json()

    try:
        table = data["response"][0]["league"]["standings"][0]
    except:
        return []

    rows = []

    for team in table:

        rows.append((
            league_id,
            season,
            team["team"]["id"],
            team["rank"],
            team["points"],
            team["all"]["played"],
            team["all"]["win"],
            team["all"]["draw"],
            team["all"]["lose"],
            team["all"]["goals"]["for"],
            team["all"]["goals"]["against"]
        ))

    return rows


def save_standings(rows):

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.executemany("""

    INSERT OR REPLACE INTO league_standings_history (
        league_id, season, team_id,
        position, points, played,
        wins, draws, losses,
        goals_for, goals_against
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, rows)

    conn.commit()
    conn.close()


def run():

    print("=== STANDINGS COLLECTOR ===")

    leagues = get_selected_leagues()

    if not leagues:
        print("No selected matches")
        return

    current_year = datetime.now().year

    seasons = [
        current_year,
        current_year - 1,
        current_year - 2
    ]

    for league_id in leagues:

        print("\nLeague:", league_id)

        for season in seasons:

            if standings_exist(league_id, season):
                print("Already exists:", season)
                continue

            print("Downloading:", season)

            rows = fetch_standings(league_id, season)

            if rows:
                save_standings(rows)
                print("Saved:", season)
            else:
                print("No data:", season)


if __name__ == "__main__":
    run()