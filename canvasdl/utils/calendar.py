import os
from datetime import datetime

from gcsa.google_calendar import Event, GoogleCalendar

from .path import Path


def add_todo(message, date):
    if date.replace(tzinfo=None) > datetime.now():
        add_event(message, date, date)


def add_event(message, start, end):
    email = os.environ["email"]
    calendar = GoogleCalendar(email, credentials_path=Path.calendar_credentials)
    existing_same_events = list(
        calendar.get_events(time_min=start, time_max=start + DAY, query=message)
    )
    if not existing_same_events:
        event = Event(message, start=start, end=end, colorId=11)
        calendar.add_event(event)
