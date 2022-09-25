import io
import urllib.parse
from dataclasses import dataclass
from functools import cached_property

import dateutil.parser
import downloader
import pandas as pd
import pywebcopy
import requests
from bs4 import BeautifulSoup
from plib import Path

from ..asset_types import Due, SaveItem
from ..utils import config, zip
from . import base


@dataclass
class Url(SaveItem):
    url: str
    root_url: str
    folder: Path

    @property
    def relative_url(self):
        return self.url.replace(self.root_url, "")

    @property
    def local_file(self):
        return self.folder / self.relative_url

    def save(self):
        if self.local_file.suffix == ".html":
            base_tag = f"<base href='{self.root_url}'>"
            self.local_file.text = base_tag + requests.get(self.url).text
        else:
            downloader.download(self.url, self.local_file)
        self.local_file.tag = 0
        if self.local_file.suffix == ".zip":
            zip.unzip(self.local_file)

    @property
    def display_title(self):
        return self.relative_url

    @property
    def save_id(self):
        return self.relative_url


class Checker(base.Checker):
    def make_item(self, item):
        return (
            Due(*item)
            if isinstance(item, tuple)
            else Url(item, self.url, self.path.parent)
        )

    @cached_property
    def url(self):
        return config.website[self.course.name]

    @property
    def path(self):
        return super().path / "Homepage.html"

    def get_items(self):
        html_content = requests.get(self.url).content
        items = [
            *self.get_calendar_items(html_content),
            *self.get_content_items(html_content),
        ]
        return items

    def get_content_items(self, html_content):
        soup = BeautifulSoup(html_content, features="lxml")
        urls = [
            urllib.parse.urljoin(self.url, link.get("href"))
            for link in soup.find_all("a")
        ]
        for u in urls:
            if u.startswith(self.url):
                yield u

    def get_calendar_items(self, html_content):
        with io.BytesIO(html_content) as fp:
            tables = pd.read_html(fp)

        calendar_table = next(t for t in tables if "Due" in t.columns)
        calendar_items = calendar_table[~calendar_table["Due"].isnull()]
        for _, item in calendar_items.iterrows():
            yield (
                self.course.assignment_name(item["Due"]),
                dateutil.parser.parse(item["Date"]),
            )

    def should_check(self):
        return self.course.name in config.website

    def check_new_items(self):
        self.save(config.website[self.course.name])
        super().check_new_items()

    def save(self, url, offline=False):
        if offline:
            self.save_offline(url)
        else:
            self.save_online(url)

    def save_offline(self, url):
        folder = self.path.with_suffix("")
        pywebcopy.save_webpage(url, str(folder.parent), project_name=folder.name)
        index_path = next(folder.rglob("index.html"))
        index_path_symlink = self.path
        index_path_symlink.symlink_to(index_path)

    def save_online(self, url):
        if not self.path.exists():
            self.path.text = f"<script>location.href = '{url}'</script>"
            self.path.tag = 9999
