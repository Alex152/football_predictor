import json

PRIORITY_FILE = "src/config/priority.json"


def load_priorities():

    with open(PRIORITY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_country_priority(country):

    priorities = load_priorities()

    countries = priorities.get("country_priority", {})

    # devolver prioridad del país
    return countries.get(country, 50)


def get_league_priority(country, league):

    priorities = load_priorities()

    leagues = priorities.get("leagues_priority", {}).get(country, {})

    return leagues.get(league, 10)