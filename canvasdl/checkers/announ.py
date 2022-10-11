from abc import ABC
from dataclasses import dataclass

from canvasdl.utils import Path, config
from canvasdl.utils.time import export_time, parse_time

from . import base


@dataclass
class Checker(base.Checker, ABC):
    def __post_init__(self):
        super().__post_init__()
        self.save_folder = Path.content_path(self.course.name, ("announ",)).with_suffix(
            ""
        )

    @property
    def path(self):
        return super().path / "Announcements.html"

    def export_downloads(self):
        href = Path.announ_css.as_uri()
        style = f'<link href="{href}" rel="stylesheet" />'
        base_tag = f'<base href="{config.API_URL}">'
        title = f"<br><h1>{self.course.name}</h1><hr>"
        html, last_announ_time = self.load_announs()
        content = base_tag + style + title + html
        self.path.text = content
        self.path.mtime = last_announ_time
        self.path.tag = 9999

    def load_announs(self):
        paths = sorted(
            list(self.save_folder.iterdir()), key=lambda path: -int(path.mtime)
        )
        announs = [path.yaml for path in paths]
        last_announ_time = parse_time(announs[0]["created_at"])
        announs = "<br><hr>".join(
            f"<h2><strong>{announ['title']}</strong><small>&ensp;&ensp;"
            f"{export_time(announ['created_at'])}"
            f"</small></h2>{announ['message']}"
            for announ in announs
        )
        return announs, last_announ_time
