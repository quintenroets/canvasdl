from dataclasses import dataclass
from datetime import datetime

from ..utils import calendar, time
from .base import SaveItem


@dataclass
class Due(SaveItem):
    name: str
    date: datetime

    @property
    def display_title(self):
        return f"{self.name} ({time.export_datetime(self.date)})"

    def save(self):
        calendar.add_todo(self.name, self.date)

    @property
    def save_id(self):
        return self.name
