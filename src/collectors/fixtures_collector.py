from datetime import datetime, timedelta
import pytz

from src.api.football_api import get_fixtures_by_date
from src.database.db import insert_match
from src.database.db import get_last_match_date



def collect_week_fixtures():

    #today = datetime.today()
    last_date = get_last_match_date()

    if last_date:
        today = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
    else:
        today = datetime.today()
        

    ecuador = pytz.timezone("America/Guayaquil")

    for i in range(3):  # Solo saca los partidos de los 3 siguientes dias 

        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")

        data = get_fixtures_by_date(date)

        matches = data["response"]

        #print("Partidos encontrados:", len(matches))
        print("Fecha:", date, "Partidos:", len(matches))

        for m in matches:

            utc_time = datetime.fromisoformat(
                m["fixture"]["date"].replace("Z", "+00:00")
            )

            local_time = utc_time.astimezone(ecuador)

            match_data = {

                "fixture_id": m["fixture"]["id"],
                "timestamp": m["fixture"]["timestamp"],

                "date": local_time.strftime("%Y-%m-%d"),
                "time": local_time.strftime("%H:%M"),

                "league_id": m["league"]["id"],
                "league_name": m["league"]["name"],
                "country": m["league"]["country"],
                "season": m["league"]["season"],

                "home_team_id": m["teams"]["home"]["id"],
                "home_team": m["teams"]["home"]["name"],

                "away_team_id": m["teams"]["away"]["id"],
                "away_team": m["teams"]["away"]["name"],

                "status": m["fixture"]["status"]["short"]

            }

            insert_match(match_data)

            print(
                match_data["date"],
                match_data["time"],
                match_data["league_name"],
                match_data["home_team"],
                "vs",
                match_data["away_team"]
            )



def collect_fixtures_by_dates(dates):

    ecuador = pytz.timezone("America/Guayaquil")

    for date in dates:

        data = get_fixtures_by_date(date)
        matches = data["response"]

        print("Fecha:", date, "Partidos:", len(matches))

        for m in matches:

            utc_time = datetime.fromisoformat(
                m["fixture"]["date"].replace("Z", "+00:00")
            )

            local_time = utc_time.astimezone(ecuador)

            match_data = {

                "fixture_id": m["fixture"]["id"],
                "timestamp": m["fixture"]["timestamp"],

                "date": local_time.strftime("%Y-%m-%d"),
                "time": local_time.strftime("%H:%M"),

                "league_id": m["league"]["id"],
                "league_name": m["league"]["name"],
                "country": m["league"]["country"],
                "season": m["league"]["season"],

                "home_team_id": m["teams"]["home"]["id"],
                "home_team": m["teams"]["home"]["name"],

                "away_team_id": m["teams"]["away"]["id"],
                "away_team": m["teams"]["away"]["name"],

                "status": m["fixture"]["status"]["short"]
            }

            insert_match(match_data)

            print(
                match_data["date"],
                match_data["time"],
                match_data["league_name"],
                match_data["home_team"],
                "vs",
                match_data["away_team"]
            )