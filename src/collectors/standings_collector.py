from src.api.football_api import get_standings
from src.database.db import insert_team_stats


def collect_league_standings(league_id, season):

    data = get_standings(league_id, season)

    standings = data["response"][0]["league"]["standings"][0]

    for team in standings:

        team_id = team["team"]["id"]

        stats = {

            "team_id": team_id,
            "league_id": league_id,
            "season": season,

            "matches_played": team["all"]["played"],
            "goals_for": team["all"]["goals"]["for"],
            "goals_against": team["all"]["goals"]["against"]

        }

        insert_team_stats(stats)

        print(
            "Standings saved:",
            team["team"]["name"]
        )