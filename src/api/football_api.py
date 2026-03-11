import requests
import os
from dotenv import load_dotenv

from src.core.request_manager import register_request, can_make_request

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

headers = {
    "x-apisports-key": API_KEY
}


def api_request(endpoint, params=None):

    if not can_make_request():

        print("⚠️ LIMITE DE REQUESTS ALCANZADO")
        return None

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(url, headers=headers, params=params)

    register_request()

    if response.status_code != 200:

        print("Error API:", response.status_code)
        return None

    return response.json()


def get_fixtures_by_date(date):

    params = {
        "date": date
    }

    return api_request("/fixtures", params)


def get_team_statistics(team_id, league_id, season):

    params = {
        "team": team_id,
        "league": league_id,
        "season": season
    }

    return api_request("/teams/statistics", params)