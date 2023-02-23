from dataclasses import dataclass
from datetime import datetime, timedelta

from canvasdl import client
from canvasdl.asset_types import Announcement

from .. import announ
from . import base


@dataclass
class Checker(base.Checker, announ.Checker):
    check_time: str = ""

    @classmethod
    def current_time(cls) -> str:
        return (datetime.now() - timedelta(days=365)).isoformat()

    def load_saved_content(self):
        super().load_saved_content()

    def make_item(self, item):
        item = Announcement.from_response(item)
        item.save_folder = self.save_folder
        return item

    def get_items(self):
        last_check_time: str = self.content_check_path.text or self.current_time()
        self.check_time = datetime.now().isoformat()
        announcements = client.get_announcements(
            [self.api], start_date=last_check_time, end_date=self.check_time
        )
        return announcements

    @property
    def content_check_path(self):
        return self.content_path.with_suffix(".txt")

    def after_check(self):
        self.content_check_path.text = self.check_time
