import sqlite3

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="src/web/templates")

DB = "data/football.db"


def get_matches():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT home_team, away_team, league_name, date, time, country
    FROM matches
    WHERE date >= DATE('now','-1 day')
    ORDER BY date, time
    
    """)

    rows = cursor.fetchall()
    conn.close()

    matches = []

    for r in rows:
        matches.append({
            "home": r[0],
            "away": r[1],
            "league": r[2],
            "date": r[3],
            "time": r[4],
            "country": r[5]

        })

    return matches


def get_predictions():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        m.home_team,
        m.away_team,
        p.score,
        p.created_at
    FROM predictions p
    JOIN matches m
    ON p.fixture_id = m.fixture_id
    ORDER BY p.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    predictions = []

    for r in rows:
        predictions.append({
            "home": r[0],
            "away": r[1],
            "score": r[2],
            "date": r[3]
        })

    return predictions


@app.get("/")
def home(request: Request):

    matches = get_matches()

    return templates.TemplateResponse(
        "matches.html",
        {
            "request": request,
            "matches": matches
        }
    )


@app.get("/matches")
def matches_page(request: Request):

    matches = get_matches()

    return templates.TemplateResponse(
        "matches.html",
        {
            "request": request,
            "matches": matches
        }
    )


@app.get("/predictions")
def get_predictions():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        home_team,
        away_team,
        league,
        match_date,
        score,
        result

    FROM predictions
    ORDER BY created_at DESC
    LIMIT 50

    """)

    rows = cursor.fetchall()

    conn.close()

    predictions = []

    for r in rows:

        predictions.append({
            "home": r[0],
            "away": r[1],
            "league": r[2],
            "date": r[3],
            "score": r[4],
            "result": r[5]
        })

    return predictions