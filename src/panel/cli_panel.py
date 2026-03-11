from src.collectors.fixtures_collector import collect_week_fixtures
from src.core.matches_selector import select_top_matches
from src.database.db import get_last_match_date


def show_status():

    last = get_last_match_date()

    print("\nDATABASE STATUS")

    if last:
        print("Last fixtures date:", last)
    else:
        print("No fixtures downloaded")


def show_top_matches():

    try:
        limit = int(input("How many matches to select (default 40): ") or 40)
    except:
        limit = 40

    matches = select_top_matches(limit)

    print("\nTOP MATCHES SELECTED:", len(matches))
    print("--------------------------------------------------")

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
            m["league_name"],
            "|",
            m["country"]
        )


def main():

    while True:

        print("\nFOOTBALL ANALYZER PANEL")

        print("1 Download fixtures")
        print("2 Database status")
        print("3 Select top matches")
        print("4 Exit")

        option = input("Option: ")

        if option == "1":

            collect_week_fixtures()

        elif option == "2":

            show_status()

        elif option == "3":

            show_top_matches()

        elif option == "4":

            break