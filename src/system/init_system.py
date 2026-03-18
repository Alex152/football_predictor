from src.core.request_manager import init_request_table

from src.database.db import create_league_standings_history
from src.database.db import create_analyzed_matches_table
from src.database.db import create_predictions_table


def initialize_system():

    print("Inicializando sistema...")

    init_request_table()

    create_league_standings_history()
    create_analyzed_matches_table()
    create_predictions_table()

    print("Base de datos lista")