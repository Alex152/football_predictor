from datetime import datetime
import pytz

from src.config.settings import TIMEZONE

ecuador = pytz.timezone(TIMEZONE)


def match_already_finished(match_date, match_time):

    now = datetime.now(ecuador)

    match_datetime = datetime.strptime(
        match_date + " " + match_time,
        "%Y-%m-%d %H:%M"
    )

    return match_datetime < now