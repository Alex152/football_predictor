from src.database.db import get_world_matches


def show_world_matches(date):

    matches = get_world_matches(date)

    print("\nINTERNATIONAL MATCHES")

    for i, m in enumerate(matches, start=1):

        print(

            i,
            "|",
            m["date"],
            m["time"],
            "|",
            m["home_team"],
            "vs",
            m["away_team"],
            "|",
            m["league_name"]

        )

    return matches