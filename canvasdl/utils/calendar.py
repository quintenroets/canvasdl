from datetime import datetime, timedelta

from gcsa.google_calendar import Event, GoogleCalendar

from .config import config
from .path import Path

DAY = timedelta(days=1)


def add_todo(message, date):
    if date.replace(tzinfo=None) > datetime.now():
        add_event(message, date, date)


def add_event(message, start, end):
    args = (config.google_calendar_id,) if config.google_calendar_id else ()
    calendar = GoogleCalendar(*args, credentials_path=Path.calendar_credentials)
    existing_same_events = list(
        calendar.get_events(time_min=start, time_max=start + DAY, query=message)
    )
    if not existing_same_events:
        event = Event(message, start=start, end=end, colorId=11)
        calendar.add_event(event)
