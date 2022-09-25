from dataclasses import dataclass
from typing import Any, List

from ..utils import Path, time
from . import SaveItem, base


@dataclass
class History(base.Item):
    anon: str
    subject: str
    created: str
    content: str
    uid: str = None
    uid_a: str = None


@dataclass
class Announcement(SaveItem):
    history_size: int
    folders: List[str]
    nr: int
    data: Any
    created: str
    bucket_order: int
    no_answer_followup: int
    change_log: Any
    bucket_name: str
    history: List[History]
    type: str
    tags: List[str]
    tag_good: List[Any]
    unique_views: int
    children: List[Any]
    tag_good_arr: List[str]
    id: str
    config: Any
    status: str
    drafts: Any
    request_instructor: int
    request_instructor_me: bool
    bookmarked: int
    num_favorites: int
    my_favorite: bool
    is_bookmarked: bool
    is_tag_good: bool
    q_edits: Any
    i_edits: Any
    s_edits: Any
    t: int
    default_anonymity: str
    no_answer: Any = None
    save_folder: Path = None

    @property
    def short_title(self):
        return self.history[0].subject

    @property
    def mtime(self):
        return self.history[0].created

    def save(self):
        save_path = self.save_folder / f"piazza_{self.nr}.yaml"
        save_path.yaml = {
            "title": self.short_title,
            "created_at": self.history[0].created,
            "message": self.history[0].content,
        }
        save_path.mtime = time.parse_time(self.mtime)

    def should_download(self):
        return "instructor-note" in self.tags

    @property
    def display_title(self):
        return f"{self.short_title} ({time.export_time(self.mtime)})"

    @property
    def save_id(self):
        return self.id
