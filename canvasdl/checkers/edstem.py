from dataclasses import dataclass
from typing import Any, Dict, List

import requests
from requests import Session

from ..asset_types.edstem import Announcement
from . import announ
from .canvas import tab


@dataclass
class Checker(announ.Checker, tab.Checker):
    api_url: str = None
    api_headers: Dict = None

    @property
    def pin_amount_path(self):
        return self.content_path.with_stem(self.content_path.stem + "pinned")

    def get_api_data(self, limit=1, sort="new", offset=0, filter="staff", **params):
        params |= {"limit": limit, "sort": sort, "offset": offset, "filter": filter}
        return requests.get(
            self.api_url, params=params, headers=self.api_headers
        ).json()["threads"]

    def get_thread(self, position):
        threads = self.get_api_data(offset=position)
        thread = threads[0] if threads else None
        return thread

    def get_items(self) -> List[Any]:
        self.prepare_api()
        items = [*self.get_thread_items(), *self.get_unpinned_items()]
        return items

    def get_thread_items(self, start_offset=0):
        last_item_new = True
        offset = start_offset
        while last_item_new:
            thread = self.get_thread(offset)
            if thread and thread["id"] not in self.old_content:
                yield thread
                offset += 1
            else:
                last_item_new = False

    def get_unpinned_items(self):
        unpinned_index = int(self.pin_amount_path.text or "0")
        thread = self.get_thread(unpinned_index)

        while thread and thread["is_pinned"]:
            unpinned_index += 1
            thread = self.get_thread(unpinned_index)

        if thread and thread["id"] not in self.old_content:
            yield thread

        self.pin_amount_path.text = unpinned_index
        yield from self.get_thread_items(start_offset=unpinned_index)

    def make_item(self, item):
        item_info = item | dict(save_folder=self.save_folder)
        return Announcement.from_dict(item_info)

    @classmethod
    def tab_name(cls):
        return "Ed Discussion"

    def prepare_api(self):
        url = "https://us.edstem.org/api/login_token"
        course_id, login_token = self.get_tokens()
        self.api_url = f"https://us.edstem.org/api/courses/{course_id}/threads"

        data = {"login_token": login_token}
        resp = requests.post(url, json=data).json()
        self.api_headers = {"x-token": resp["token"]}

    def get_tokens(self):
        session = Session()
        launch_url = self.get_launch_url()
        launch_response = session.get(launch_url).text
        relocation_url = None

        for _ in range(2):
            url, data = self.parse_form(launch_response)
            response = session.post(url, data=data)
            relocation_url = response.url
            launch_response = response.text

        info = relocation_url.split("/")[-1]
        tokens = info.split("?_logintoken=")
        return tokens
