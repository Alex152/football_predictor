from src.api.football_api import get_team_statistics
from src.database.db import insert_team_stats
import sqlite3


def collect_team_stats():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT DISTINCT
    home_team_id,
    league_id,
    season

    FROM matches

    """)

    teams = cursor.fetchall()

    print("Equipos a analizar:", len(teams))

    for team_id, league_id, season in teams:

        data = get_team_statistics(team_id, league_id, season)

        stats = data["response"]

        matches_played = stats["fixtures"]["played"]["total"]
        goals_for = stats["goals"]["for"]["total"]["total"]
        goals_against = stats["goals"]["against"]["total"]["total"]

        team_stats = {

            "team_id": team_id,
            "league_id": league_id,
            "season": season,

            "matches_played": matches_played,
            "goals_for": goals_for,
            "goals_against": goals_against

        }

        insert_team_stats(team_stats)

        print(
            "Team:",
            team_id,
            "GF:",
            goals_for,
            "GA:",
            goals_against
        )