from dataclasses import dataclass
from typing import Dict

from ..utils import Path, time
from . import SaveItem


@dataclass
class Announcement(SaveItem):
    id: int
    user_id: int
    course_id: int
    editor_id: int | None
    accepted_id: int | None
    duplicate_id: int | None
    number: int
    type: str
    title: str
    content: str
    document: str
    category: str
    subcategory: str
    subsubcategory: str
    flag_count: int
    star_count: int
    view_count: int
    unique_view_count: int
    vote_count: int
    reply_count: int
    unresolved_count: int
    is_locked: bool
    is_pinned: bool
    is_private: bool
    is_endorsed: bool
    is_answered: bool
    is_student_answered: bool
    is_staff_answered: bool
    is_archived: bool
    is_anonymous: bool
    is_megathread: bool
    anonymous_comments: bool
    approved_status: str
    created_at: str
    updated_at: str
    deleted_at: None
    pinned_at: str | None
    anonymous_id: int
    vote: int
    is_seen: bool
    is_starred: bool
    is_watched: None
    glanced_at: str | None
    new_reply_count: int
    duplicate_title: None
    user: Dict

    save_folder: Path = None

    @property
    def short_title(self):
        return self.title

    @property
    def mtime(self):
        return self.created_at

    def save(self):
        save_path = self.save_folder / f"edstem_{self.save_id}.yaml"
        save_path.yaml = {
            "title": self.short_title,
            "created_at": self.mtime,
            "message": self.content,
        }
        save_path.mtime = time.parse_time(self.mtime)

    @property
    def display_title(self):
        return f"{self.short_title} ({time.export_time(self.mtime)})"

    @property
    def save_id(self):
        return self.id
