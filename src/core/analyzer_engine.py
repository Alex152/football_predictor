import sqlite3

from src.config.settings import DATABASE_PATH
from src.core.matches_selector import select_top_matches
from src.analyzer.match_analyzer import analyze_match


def get_match_team_ids(fixture_id):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT
        home_team_id,
        away_team_id,
        league_id,
        season

        FROM matches
        WHERE fixture_id=?

        """,
        (fixture_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "home_team_id": row[0],
        "away_team_id": row[1],
        "league_id": row[2],
        "season": row[3]
    }


def save_prediction(fixture_id, score):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """

        INSERT INTO predictions
        (fixture_id, score, created_at)

        VALUES (?, ?, datetime('now'))

        """,
        (fixture_id, score)
    )

    conn.commit()
    conn.close()


def run_analysis(limit=40):

    matches = select_top_matches(limit)

    print("\nMATCHES TO ANALYZE:", len(matches))

    for match in matches:

        fixture_id = match["fixture_id"]

        print(
            "Analyzing:",
            match["home_team"],
            "vs",
            match["away_team"]
        )

        ids = get_match_team_ids(fixture_id)

        if not ids:
            print("Match data missing")
            continue

        score = analyze_match(
            fixture_id,
            ids["home_team_id"],
            ids["away_team_id"],
            ids["league_id"],
            ids["season"]
        )

        if score is None:
            print("Not enough stats")
            continue

        save_prediction(fixture_id, score)

        print("Prediction score:", score)