from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import Any

import downloader

from canvasdl import client
from canvasdl.utils.time import parse_time

from ..utils import Path, time
from . import base
from .base import SaveItem


@dataclass
class Asset(base.Item):
    _requester: Any
    id: int


@dataclass
class Item(Asset):
    created_at: str
    created_at_date: datetime
    updated_at: str
    updated_at_date: datetime
    lock_at: None
    unlock_at: None
    locked: bool
    hidden: bool | None
    locked_for_user: bool
    hidden_for_user: bool

    @cached_property
    def mtime(self):
        return parse_time(self.updated_at)


@dataclass
class File(Item):
    uuid: str
    folder_id: int
    display_name: str
    filename: str
    upload_status: str
    content_type: str
    url: str
    size: int
    thumbnail_url: str | None
    modified_at: str
    modified_at_date: datetime
    mime_class: str
    media_entry_id: str | None
    category: str | None = None
    root: Path = None

    @property
    def display_title(self):
        return self.display_name

    @classmethod
    def from_response(cls, response):
        file_info = response.__dict__
        # rename field for parsing
        file_info["content_type"] = file_info.pop("content-type")
        return File.from_dict(file_info)

    @cached_property
    def folder(self):
        folder = client.get_folder(self.folder_id)
        folder = Folder.from_response(folder)
        return folder

    @property
    def folder_path(self):
        return self.root / self.folder.path_name

    def get_full_path(self):
        return self.folder_path / self.display_name

    def save(self):
        path = self.get_full_path()
        downloader.download(self.url, path)
        path.tag = 0
        path.mtime = self.mtime
        path.unpack_if_archive()
        self.folder.set_time(self.root)

    @property
    def save_id(self):
        return self.id


@dataclass
class Folder(Item):
    name: str
    full_name: str
    context_id: int
    context_type: Any
    parent_folder_id: int | None
    position: int | None
    folders_url: str
    files_url: str
    files_count: int
    folders_count: int
    for_submissions: bool
    can_upload: bool

    @property
    def path_name(self):
        folder_name = self.full_name
        for append in ("/", ""):
            folder_name = folder_name.replace(f"course files{append}", "")
        return folder_name

    def set_time(self, root):
        path = root / self.path_name
        path.mtime = self.mtime
        if self.parent:
            self.parent.set_time(root)

    @property
    def parent(self):
        if self.parent_folder_id:
            folder = client.get_folder(self.parent_folder_id)
            folder = Folder.from_response(folder)
        else:
            folder = None
        return folder


@dataclass
class Announcement(Asset, SaveItem):
    title: str
    last_reply_at: str
    last_reply_at_date: datetime
    created_at: str
    created_at_date: datetime
    delayed_post_at: str | None
    posted_at: str
    posted_at_date: datetime
    assignment_id: str | None
    root_topic_id: str | None
    position: int
    podcast_has_student_posts: bool
    discussion_type: str
    lock_at: None
    allow_rating: bool
    only_graders_can_rate: bool
    sort_by_rating: bool
    is_section_specific: bool
    anonymous_state: None
    user_name: str
    discussion_subentry_count: int
    permissions: Any
    require_initial_post: bool | None
    user_can_see_posts: bool
    podcast_url: None
    read_state: str
    unread_count: int
    subscribed: bool
    attachments: Any
    published: bool
    can_unpublish: bool
    locked: bool
    can_lock: bool
    comments_disabled: bool
    author: Any
    html_url: str
    url: str
    pinned: bool
    group_category_id: None
    can_group: bool
    topic_children: Any
    group_topic_children: Any
    context_code: str
    locked_for_user: bool
    message: str
    subscription_hold: Any
    todo_date: None
    delayed_post_at_date: datetime = None

    lock_info: Any = None
    lock_explanation: Any = None
    save_folder: Path = None

    def save(self):
        save_path = self.save_folder / f"{self.position}.yaml"
        save_path.yaml = {
            k: self.__dict__[k] for k in ("title", "created_at", "message")
        }
        save_path.mtime = time.parse_time(self.created_at)

    @property
    def save_id(self):
        return self.id

    @property
    def display_title(self):
        return self.title
