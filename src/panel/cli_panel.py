from src.collectors.fixtures_collector import collect_fixtures_by_dates
from src.core.matches_selector import select_top_matches
from src.core.api_cost_estimator import estimate_requests
from src.database.db import get_last_match_date, save_selected_matches
from src.core.international_selector import show_world_matches


def show_status():

    last = get_last_match_date()

    print("\nDATABASE STATUS")

    if last:
        print("Last fixtures date:", last)
    else:
        print("No fixtures downloaded")


def show_top_matches():

    start_date = input("Start date (YYYY-MM-DD): ")
    end_date = input("End date (YYYY-MM-DD): ")

    try:
        limit = int(input("How many matches to select (default 40): ") or 40)
    except:
        limit = 40

    matches = select_top_matches(limit, start_date, end_date)

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

    estimate_requests(matches)

    confirm = input("\nSave selected matches? (y/n): ")

    if confirm.lower() == "y":

        save_selected_matches(matches)

        print("Matches saved for analysis")


def show_world_menu():

    date = input("Date for international matches (YYYY-MM-DD): ")

    matches = show_world_matches(date)

    if not matches:
        print("No international matches found")
        return

    choice = input("Include all international matches? (y/n): ")

    if choice.lower() == "y":

        from src.database.db import save_selected_matches

        save_selected_matches(matches)

        print("International matches added")


def main():

    while True:

        print("\nFOOTBALL ANALYZER PANEL")

        print("1 Download fixtures")
        print("2 Database status")
        print("3 Select top matches")
        print("4 International competitions")
        print("5 Exit")

        option = input("Option: ")

        if option == "1":

            dates_input = input(
                "Enter dates separated by comma (YYYY-MM-DD): "
            )

            dates = [d.strip() for d in dates_input.split(",")]

            collect_fixtures_by_dates(dates)

        elif option == "2":

            show_status()

        elif option == "3":

            show_top_matches()

        elif option == "4":

            show_world_menu()

        elif option == "5":

            break