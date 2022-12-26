import os
from dataclasses import dataclass
from functools import cached_property

import cli
from piazza_api import Piazza

from ..asset_types.piazza import Announcement
from . import announ


@dataclass
class Checker(announ.Checker):
    def should_check(self) -> bool:
        return bool(self.course.piazza_id)

    @cached_property
    def api(self):
        api = get_api()
        network_id = self.course.piazza_id
        api = api.network(network_id)
        return api

    def get_items(self):
        feed = self.api.get_feed(limit=999999, offset=0)
        ids = [post["id"] for post in feed["feed"]]
        new_ids = [i for i in ids if i not in self.old_content]
        return new_ids

    def make_item(self, item):
        item_info = self.api.get_post(item) | dict(save_folder=self.save_folder)
        return Announcement.from_dict(item_info)


def get_api():
    piazza = Piazza()
    email = os.environ["school_email"]
    password = cli.get("pw piazza")

    piazza.user_login(email=email, password=password)
    return piazza
