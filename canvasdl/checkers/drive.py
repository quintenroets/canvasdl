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
        local_path = self.path / "Drive"
        drive_name = config.drive[self.course.name]
        remote_path = f"{drive_name}:"
        options = {"drive-export-formats": "pdf"}
        cli.run("rclone", "sync", options, remote_path, local_path)
