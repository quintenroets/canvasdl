import urllib.parse
from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property

import dateutil.parser
import downloader
import pandas as pd
import pywebcopy
import requests
from bs4 import BeautifulSoup
from plib import Path

from ..asset_types import Due, SaveItem
from . import base


@dataclass
class Url(SaveItem):
    url: str
    root_url: str
    folder: Path

    @property
    def relative_url(self):
        url = self.url.replace(self.root_url, "")
        url = urllib.parse.urlparse(url).path
        return url

    @property
    def local_file(self):
        return self.folder.subpath(*self.relative_url.split("/"))

    @property
    def is_html_content(self):
        is_html = self.local_file.suffix == ".html"
        if not is_html:
            headers = requests.get(self.url, headers=self.headers, stream=True).headers
            content_type = headers.get("content-type") or headers.get("Content-Type")
            is_html = "text/html" in content_type
        return is_html

    def save(self):
        dest = self.local_file
        if self.is_html_content:
            base_tag = f"<base href='{self.root_url}'>"
            dest = dest.with_suffix(".html")
            dest.text = base_tag + requests.get(self.url).text
        else:
            downloader.download(self.url, dest)
        dest.tag = 0
        dest.unpack_if_archive()

    @property
    def display_title(self):
        return self.relative_url

    @property
    def save_id(self):
        return self.relative_url

    @property
    def headers(self):
        browser = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/85.0.4183.83 Safari/537.36"
        )
        return {"User-Agent": browser}


class Checker(base.Checker):
    def make_item(self, item):
        return (
            Due(*item)
            if isinstance(item, tuple)
            else Url(item, self.url, self.path.parent / "Homepage")
        )

    def get_urls(self):
        return self.course.websites

    @cached_property
    def url(self):
        urls = self.get_urls()
        root_url = next(iter(urls))
        if not root_url.endswith("/"):
            root_url = f"{root_url}/"
        return root_url

    def sub_urls(self):
        return next(iter(self.get_urls().values()))

    @property
    def path(self):
        return super().path / "Homepage.html"

    def get_items(self):
        for sub_url in self.sub_urls():
            url = urllib.parse.urljoin(self.url, sub_url).strip("/")
            yield from self.get_url_items(url)

    def get_url_items(self, url):
        html_content: bytes = requests.get(url).content
        extractors = (self.get_content_items,)  # get_calendar_items
        for extractor in extractors:
            yield from extractor(html_content)  # noqa

    def get_content_items(self, html_content):
        soup = BeautifulSoup(html_content, features="lxml")
        for link in soup.find_all("a"):
            yield urllib.parse.urljoin(self.url, link.get("href"))

    def get_calendar_items(self, html_content: bytes):
        with Path.tempfile() as tmp:
            tmp.byte_content = html_content
            tables = pd.read_html(tmp)

        due_keywords = ("Due", "Assignments")
        for table in tables:
            table.reset_index(drop=True, inplace=True)

            for due_keyword in due_keywords:
                if due_keyword in table.columns:
                    calendar_items = table[~table[due_keyword].isnull()]
                    for _, item in calendar_items.iterrows():
                        date_key = "Date" if "Date" in table.columns else due_keyword
                        name_key = (
                            "Assignment"
                            if "Assignment" in table.columns
                            else due_keyword
                        )
                        date = item[date_key]
                        if date_key == "Due":
                            date = " ".join(date.split(" ")[1:])
                        if date:
                            date = date.replace("Tues", "Tue")
                            parsed_date = dateutil.parser.parse(date)
                            due_time = parsed_date + timedelta(hours=23, minutes=30)
                            parsed_name = self.course.assignment_name(item[name_key])
                            yield parsed_name, due_time

    def should_check(self) -> bool:
        return bool(self.course.websites)

    def check_new_items(self):
        self.save_website()
        super().check_new_items()

    def save_website(self, offline=False):
        if offline:
            self.save_offline()
        else:
            self.save_online()

    def save_offline(self):
        folder = self.path.with_suffix("")
        pywebcopy.save_webpage(self.url, str(folder.parent), project_name=folder.name)
        index_path = next(folder.rglob("index.html"))
        index_path_symlink = self.path
        index_path_symlink.symlink_to(index_path)

    def save_online(self):
        if not self.path.exists():
            self.path.text = f"<script>location.href = '{self.url}'</script>"
            self.path.tag = 9999
