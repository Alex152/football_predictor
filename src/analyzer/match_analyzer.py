import sqlite3

from src.config.settings import DATABASE_PATH
from src.core.matches_selector import mark_match_analyzed


def analyze_match(fixture_id, home_team_id, away_team_id, league_id, season):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT goals_for, goals_against, matches_played
        FROM team_stats
        WHERE team_id=? AND league_id=? AND season=?

        """,
        (home_team_id, league_id, season)
    )

    home = cursor.fetchone()

    cursor.execute(
        """

        SELECT goals_for, goals_against, matches_played
        FROM team_stats
        WHERE team_id=? AND league_id=? AND season=?

        """,
        (away_team_id, league_id, season)
    )

    away = cursor.fetchone()

    conn.close()

    if not home or not away:
        return None

    home_attack = home[0] / home[2]
    away_attack = away[0] / away[2]

    home_def = home[1] / home[2]
    away_def = away[1] / away[2]

    score = (home_attack - away_def) - (away_attack - home_def)

    # marcar partido como analizado
    mark_match_analyzed(fixture_id)

    return score