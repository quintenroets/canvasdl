from dataclasses import dataclass

import cli

from ..utils import config
from . import base


@dataclass
class Checker(base.Checker):
    def get_items(self):
        return []

    def should_check(self):
        return self.course.name in config.drive

    def check_new_content(self):
        drive_name = config.drive[self.course.name]
        cli.run("rclone", "sync", f"{drive_name}:", self.path / "Drive")
