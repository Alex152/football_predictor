import json


PRIORITY_FILE = "src/config/priority.json"


def load_priorities():

    with open(PRIORITY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_country_priority(country):

    priorities = load_priorities()

    countries = priorities["countries_priority"]

    if country in countries:
        return countries.index(country)

    return len(countries) + 10


def get_league_priority(country, league):

    priorities = load_priorities()

    leagues = priorities["leagues_priority"].get(country, [])

    if league in leagues:
        return leagues.index(league)

    return len(leagues) + 10