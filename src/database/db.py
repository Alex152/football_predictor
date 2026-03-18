import sqlite3

from datetime import datetime

conn = sqlite3.connect("data/football.db")
cursor = conn.cursor()


# -------------------------
# TABLA DE PARTIDOS
# -------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS matches (

fixture_id INTEGER PRIMARY KEY,

timestamp INTEGER,

date TEXT,
time TEXT,

league_id INTEGER,
league_name TEXT,
country TEXT,
season INTEGER,

home_team_id INTEGER,
home_team TEXT,

away_team_id INTEGER,
away_team TEXT,

status TEXT

)

""")

# -------------------------
# TABLA DE ESTADISTICAS DE EQUIPOS
# -------------------------
cursor.execute("""

CREATE TABLE IF NOT EXISTS team_stats (

team_id INTEGER,
league_id INTEGER,
season INTEGER,

position INTEGER,
points INTEGER,

matches_played INTEGER,

goals_for INTEGER,
goals_against INTEGER,

PRIMARY KEY (team_id, league_id, season)

)

""")


# -------------------------
# TABLA DE PARTIDOS SELECCIONADOS
# -------------------------
cursor.execute("""

CREATE TABLE IF NOT EXISTS selected_matches (

fixture_id INTEGER PRIMARY KEY,
selected_date TEXT

)

""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS api_usage (

date TEXT PRIMARY KEY,
requests_used INTEGER

)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS league_standings_history (

id INTEGER PRIMARY KEY AUTOINCREMENT,

league_id INTEGER,
season INTEGER,

team_id INTEGER,
position INTEGER,
points INTEGER,
played INTEGER,
wins INTEGER,
draws INTEGER,
losses INTEGER,
goals_for INTEGER,
goals_against INTEGER,

UNIQUE(league_id, season, team_id)

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_requests (

date TEXT PRIMARY KEY,
requests_used INTEGER

)
""")


conn.commit()



def insert_match(match):

    cursor.execute("""

    INSERT OR IGNORE INTO matches
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        match["fixture_id"],
        match["timestamp"],

        match["date"],
        match["time"],

        match["league_id"],
        match["league_name"],
        match["country"],
        match["season"],

        match["home_team_id"],
        match["home_team"],

        match["away_team_id"],
        match["away_team"],

        match["status"]

    ))

    conn.commit()


def insert_team_stats(stats):

    cursor.execute("""

    INSERT OR REPLACE INTO team_stats
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        stats["team_id"],
        stats["league_id"],
        stats["season"],

        stats["position"],
        stats["points"],

        stats["matches_played"],
        stats["goals_for"],
        stats["goals_against"]

    ))

    conn.commit()


def get_last_match_date():

    import sqlite3

    conn = sqlite3.connect("data/football.db")
    cur = conn.cursor()

    cur.execute("SELECT MAX(date) FROM matches")

    result = cur.fetchone()

    conn.close()

    if result and result[0]:
        return result[0]

    return None


def create_league_standings_history():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS league_standings_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        league_id INTEGER,
        season INTEGER,
        team_id INTEGER,

        position INTEGER,
        points INTEGER,
        played INTEGER,
        wins INTEGER,
        draws INTEGER,
        losses INTEGER,

        goals_for INTEGER,
        goals_against INTEGER,

        UNIQUE(league_id, season, team_id)

    )

    """)

    conn.commit()
    conn.close()


def create_analyzed_matches_table():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS analyzed_matches (

        fixture_id INTEGER PRIMARY KEY,
        analyzed_at TEXT

    )

    """)

    conn.commit()
    conn.close()



def create_predictions_table():

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""
    
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fixture_id INTEGER,

        home_team TEXT,
        away_team TEXT,
        league TEXT,

        match_date TEXT,

        score REAL,

        result TEXT,
        correct INTEGER,

        created_at TEXT

    )

    """)

    conn.commit()
    conn.close()




def save_prediction(match, score):

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO predictions (

        fixture_id,
        home_team,
        away_team,
        league,
        match_date,
        score,
        created_at

    )

    VALUES (?,?,?,?,?,?,?)

    """, (

        match["fixture_id"],
        match["home_team"],
        match["away_team"],
        match["league_name"],
        match["date"],
        score,
        datetime.now().isoformat()

    ))

    conn.commit()
    conn.close()


def save_selected_matches(matches):

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    for m in matches:

        cursor.execute("""

        INSERT OR IGNORE INTO selected_matches
        (fixture_id, selected_at, analysis_status, priority_score)

        VALUES (?, datetime('now'), 'pending', ?)

        """, (m["fixture_id"], m["priority"]))

    conn.commit()
    conn.close()



def get_world_matches(date):

    conn = sqlite3.connect("data/football.db")
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
    fixture_id,
    date,
    time,
    league_name,
    home_team,
    away_team

    FROM matches

    WHERE date = ?
    AND country = 'World'

    """, (date,))

    rows = cursor.fetchall()

    conn.close()

    matches = []

    for r in rows:

        matches.append({

            "fixture_id": r[0],
            "date": r[1],
            "time": r[2],
            "league_name": r[3],
            "home_team": r[4],
            "away_team": r[5]

        })

    return matches





# -------------------------
# INITIALIZE TABLES
# -------------------------

create_league_standings_history()
create_analyzed_matches_table()
create_predictions_table()

print("Database tables verified/created successfully")