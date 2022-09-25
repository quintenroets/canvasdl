import os
from datetime import datetime, time, timedelta

from gcsa.google_calendar import Event, GoogleCalendar

from .path import Path

DAY = timedelta(days=1)


def add_todo(message, date):
    event_time = date.time()
    full_day = event_time == time(hour=23, minute=59)
    start = date - timedelta(hours=23, minutes=59) if full_day else date
    end = start + DAY if full_day else start
    if end.replace(tzinfo=None) > datetime.now():
        add_event(message, start, end)


def add_event(message, start, end):
    email = os.environ["email"]
    calendar = GoogleCalendar(email, credentials_path=Path.calendar_credentials)
    existing_same_events = list(
        calendar.get_events(time_min=start, time_max=start + DAY, query=message)
    )
    if not existing_same_events:
        event = Event(message, start=start, end=end, colorId=11)
        calendar.add_event(event)
