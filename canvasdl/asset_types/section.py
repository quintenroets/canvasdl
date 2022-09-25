from __future__ import annotations

import typing
from dataclasses import dataclass
from typing import Iterable

from ..utils import Path
from .course import Course

if typing.TYPE_CHECKING:
    from ..asset_types import SaveItem  # noqa: autoimport


@dataclass
class Section:
    path: Path
    course: Course
    items: Iterable[SaveItem]

    @property
    def root(self):
        return Path.school / self.course.name

    @property
    def titles(self):
        for name in self.path.relative_to(self.root).parts:
            yield Path(name).stem

    @property
    def announ(self):
        return self.path.suffix == ".html"
