from dataclasses import dataclass

import cli

from . import base


@dataclass
class Checker(base.Checker):
    def get_items(self):
        return []

    def should_check(self) -> bool:
        return bool(self.course.drive_name)

    def check_new_content(self):
        local_path = self.path / "Drive"
        remote_path = f"{self.course.drive_name}:"
        options = {"drive-export-formats": "pdf"}
        cli.run("rclone", "sync", options, remote_path, local_path)
