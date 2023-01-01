from datetime import datetime, time, timedelta

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar

from . import configchecker
from .config import config
from .path import Path

DAY = timedelta(days=1)


def add_todo(message, date):
    use_calendar = configchecker.google_calendar_credentials_valid()
    is_future_event = date.replace(tzinfo=None) > datetime.now()
    if use_calendar and is_future_event:
        add_event(message, date, date)


def add_event(message, start, end):
    start_time = start.time()
    full_day = start_time in (time(hour=23, minute=59), time(hour=0, minute=0))
    if full_day:
        # start quarter before midnight
        subtract_minutes = 15 if start_time.minute == 0 else 14
        start -= timedelta(hours=0, minutes=subtract_minutes)

    args = (config.google_calendar_id,) if config.google_calendar_id else ()
    calendar = GoogleCalendar(*args, credentials_path=Path.calendar_credentials)
    existing_same_events = list(
        calendar.get_events(time_min=start, time_max=start + DAY, query=message)
    )
    if not existing_same_events:
        event = Event(message, start=start, end=end, colorId=11)
        calendar.add_event(event)
