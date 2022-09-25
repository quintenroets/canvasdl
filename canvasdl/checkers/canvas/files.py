from collections import defaultdict
from typing import List

from canvasdl.asset_types import File, Section

from ...ui.downloadprogress import DownloadProgress
from ...utils import config
from . import base


class Checker(base.Checker):
    def get_items(self) -> List[File]:
        files = self.api.get_files(sort="updated_at", order="desc")  # most recent first

        new_files = []
        for file in files:
            if file.updated_at != self.old_content.get(file.id, ""):
                new_files.append(file)
            else:
                break  # next files are less recent so no need to check

        return new_files

    def make_item(self, item):
        item = File.from_response(item)
        item.root = self.path
        return item

    def is_new(self, item: File):
        return True

    def process_new_items(self, items: List[File]):
        file_sections = defaultdict(lambda: [])
        for item in items:
            key = item.get_full_path().parent
            file_sections[key].append(item)

        for path, section_items in file_sections.items():
            section = Section(path, self.course, section_items)
            download_progress = DownloadProgress(section)
            for item in section_items:
                item.save()
            download_progress.enable_show()

        if config.save_content:
            self.save_new_content(items)

    def save_new_content(self, items: List[File]):
        self.old_content |= {item.id: item.updated_at for item in items}
        self.content_path.content = self.old_content
