import urllib
import urllib.parse
from dataclasses import dataclass
from typing import Any

import cli

from ..utils import Path, time
from . import base


@dataclass
class ViewUrls:
    ViewerUrl: str
    EmbedUrl: str | None
    ShareSettingsUrl: str | None
    DownloadUrl: str | None
    CaptionDownloadUrl: str | None
    EditorUrl: str | None
    ThumbnailUrl: str


@dataclass
class Video(base.SaveItem):
    Description: str | None
    StartTime: str
    Duration: float
    MostRecentViewPosition: float
    CreatedBy: Any
    Urls: ViewUrls
    Folder: str
    FolderDetails: Any
    PercentCompleted: int | None
    Id: str
    Name: str

    save_folder: Path | None = None

    @property
    def display_title(self):
        return self.Name

    def __post_init__(self):
        delim = " - "
        if delim in self.Name:
            self.Name = self.Name.split(delim)[1]

    @property
    def mtime(self):
        return time.parse_time(self.StartTime)

    @property
    def save_id(self):
        return self.Id

    def save(self):
        save_path = self.save_folder / f"{self.Id}.yaml"
        saved_video = SavedVideo(
            title=self.Name,
            mtime=self.mtime,
            url=self.Urls.ViewerUrl,
            duration=self.Duration,
        )
        save_path.yaml = saved_video.dict()
        save_path.mtime = self.mtime


@dataclass
class SavedVideo(base.Item):
    title: str
    mtime: float
    url: str
    duration: float

    @property
    def id(self):
        return self.url.split("?id=")[1]

    @property
    def tag(self):
        mtime = time.export_mtime(self.mtime)
        tag = (
            f"<h2><button>Toggle</button><a href='{self.url}' style='text-decoration: none' target = '_blanck'>"
            f"&ensp;{self.title}<small>&ensp;({self.duration_string})&ensp;[{mtime}]</small></a></h2><hr>"
        )
        return tag

    @property
    def duration_string(self):
        # durations are in float format
        seconds = int(float(self.duration))

        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        hours_str = str(int(hours))
        minutes_str = str(minutes)
        if hours:
            minutes_str = minutes_str.zfill(2)
        seconds_str = str(seconds).zfill(2)

        duration_string = minutes_str + ":" + seconds_str
        if hours:
            duration_string = hours_str + ":" + duration_string

        return duration_string

    def download(self, info, folder: Path):
        folder /= self.id
        streams = info["Delivery"]["Streams"]
        for i, stream in enumerate(streams):
            url = stream["StreamUrl"]
            dest = folder / f"{i}.mp4"
            if not dest.exists():
                cli.run("youtube-dl", url, {"output": dest})
                dest.mtime = self.mtime
        folder.mtime = self.mtime

    def export_html(self, folder: Path):
        download_folder = folder / self.id
        sources = list(download_folder.iterdir())
        sources = sorted(sources, key=lambda path: path.size, reverse=True)[:2]
        template_path = Path.template1 if len(sources) == 1 else Path.template2
        content = template_path.text
        content = content.replace("**TITLE**", self.title)
        replacements = {
            "SOURCENAME": sources[0],
            "SOURCENAME1": sources[0],
            "SOURCENAME2": sources[-1],
            "TEMPLATES": Path.templates,
        }
        for k, v in replacements.items():
            content = content.replace(f"**{k}**", v.as_uri())

        export_filename = (
            folder.parent.parent
            / "video_htmls"
            / folder.name
            / self.id
            / self.title.replace("/", "_")
        ).with_suffix(".html")

        export_filename.text = content
        sources[0].copy_properties_to(export_filename)
