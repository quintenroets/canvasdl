import html
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests
from bs4 import BeautifulSoup

from ... import utils
from ...utils import time
from . import base


@dataclass
class Due:
    name: str
    date: datetime

    @property
    def title(self):
        return f"{self.name} ({time.export_datetime(self.date)})"


@dataclass
class Checker(base.Checker, ABC):
    tab: Any = None

    @classmethod
    def tab_name(cls):
        raise NotImplementedError

    def should_check(self):
        tabs = [tab for tab in self.api.get_tabs() if tab.label == self.tab_name()]
        self.tab = tabs[0] if tabs else None
        return self.tab is not None

    def get_launch_url(self):
        launch_request_url = self.tab.url
        params = {"access_token": utils.config.API_KEY}
        launch_url = requests.get(launch_request_url, params=params).json()["url"]
        return launch_url

    def get_redirected_content(self):
        launch_url = self.get_launch_url()
        launch_response = requests.get(launch_url).text
        url, data = self.parse_form(launch_response)
        return requests.post(url, data=data).text

    @classmethod
    def parse_form(cls, html_string: str):
        soup = BeautifulSoup(html_string, features="lxml")
        form = soup.find("form")
        url = form["action"]
        process = html.unescape
        data = {
            process(field["name"]): process(field["value"])
            for field in form.find_all("input")
        }
        return url, data
