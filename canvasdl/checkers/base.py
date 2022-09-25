import inspect
from dataclasses import dataclass
from typing import Any, Iterable, List

from canvasdl.asset_types import Course, Section
from canvasdl.ui.progressmanager import ProgressManager
from canvasdl.ui.userinterface import UserInterface
from canvasdl.utils import Path, config

from ..asset_types import SaveItem
from ..ui.downloadprogress import DownloadProgress


@dataclass
class Checker:
    course: Course
    old_content: Any = None

    @property
    def path(self):
        return Path.school / self.course.name

    @classmethod
    def names(cls) -> Iterable[str]:
        root_path = Path(__file__).parent
        full_path = Path(inspect.getfile(cls))
        relative_path = full_path.relative_to(root_path)
        return relative_path.with_suffix("").parts

    @classmethod
    def make_item(cls, item):
        return SaveItem()

    def get_items(self) -> List[Any]:
        raise NotImplementedError

    def __post_init__(self):
        ProgressManager.progress.amount += 1
        self.content_path = Path.content_path(self.course.name, self.names())

    def load_saved_content(self):
        self.old_content = self.content_path.content or {}

    def should_check(self):
        return True

    def check(self):
        self.check_new_content()
        ProgressManager.progress.progress += 1
        UserInterface.add_check()

    def check_new_content(self):
        self.load_saved_content()
        self.check_new_items()
        self.after_check()

    def check_new_items(self):
        items = self.get_items()
        items = [self.make_item(it) for it in items]
        items = [it for it in items if self.is_new(it)]
        if items:
            self.process_new_items(items)

    def is_new(self, item: SaveItem):
        return item.save_id not in self.old_content

    def process_new_items(self, items: List[SaveItem]):
        download_items = [it for it in items if it.should_download()]
        section = Section(self.path, self.course, download_items)
        download_progress = DownloadProgress(section)
        for item in download_items:
            item.save()

        if config.save_content:
            self.save_new_content(items)
        self.export_downloads()
        download_progress.enable_show()

    def save_new_content(self, items: List[SaveItem]):
        self.old_content = (self.old_content or {}) | {
            item.save_id: "" for item in items
        }
        self.content_path.content = self.old_content

    def export_downloads(self):
        pass

    def after_check(self):
        pass
