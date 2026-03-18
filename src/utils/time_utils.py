from datetime import datetime, timedelta
import pytz
from src.config.settings import TIMEZONE

ecuador = pytz.timezone(TIMEZONE)


def match_already_finished(match_date, match_time):

    now = datetime.now(ecuador)

    match_datetime = datetime.strptime(
        match_date + " " + match_time,
        "%Y-%m-%d %H:%M"
    )

    match_datetime = ecuador.localize(match_datetime)

    # asumimos duración máxima del partido 2 horas
    match_end = match_datetime + timedelta(hours=2)

    return match_end < now