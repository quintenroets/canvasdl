from dataclasses import dataclass
from typing import List

from canvasdl.utils.path import Path

from ..utils import config
from .base import Item


@dataclass(order=True)
class Course(Item):
    name: str
    id: str
    video_id: str = None

    @property
    def sort_index(self):
        return -Path.content_path(self.name).size

    @property
    def abbreviation(self):
        removes = ("Topics in", "Introduction to")
        name = self.name
        for r in removes:
            name = name.replace(r, "")
        return "".join(word[0].capitalize() for word in name.split(" ") if word)

    def assignment_name(self, name: str):
        return f"{self.abbreviation}: {name} due"


@dataclass
class Courses:
    courses: List[Course]

    @classmethod
    def from_dict(cls, courses):
        if config.one_course_nr:
            courses = [courses[config.one_course_nr - 1]]
        return Courses(sorted([Course(**c) for c in courses]))
