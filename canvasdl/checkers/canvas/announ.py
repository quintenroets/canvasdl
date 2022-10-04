from dataclasses import dataclass
from datetime import datetime, timedelta

from canvasdl import client
from canvasdl.asset_types import Announcement

from .. import announ
from . import base


@dataclass
class Checker(base.Checker, announ.Checker):
    last_check_time: str = ""
    check_time: str = ""

    def load_saved_content(self):
        super().load_saved_content()
        self.last_check_time = (
            self.content_path.text or (datetime.now() - timedelta(days=365)).isoformat()
        )

    def make_item(self, item):
        item = Announcement.from_response(item)
        item.save_folder = self.save_folder
        return item

    def get_items(self):
        self.check_time = datetime.now().isoformat()
        announcements = client.get_announcements(
            [self.api], start_date=self.last_check_time, end_date=self.check_time
        )
        return announcements

    def after_check(self):
        self.content_path.text = self.check_time
