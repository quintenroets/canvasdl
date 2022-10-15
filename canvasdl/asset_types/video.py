from dataclasses import dataclass
from typing import Any

from ..utils import Path, time
from . import base
from .streams import Streams


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
    local_url: Path | None = None

    @property
    def id(self):
        return self.url.split("?id=")[1]

    @property
    def filename_title(self):
        return self.title.replace("/", "_")

    def download(self, info: dict, folder: Path):
        saved_info = dict(
            folder=folder / self.id, name=self.filename_title, mtime=self.mtime
        )
        streams_info = {"streams": info["Delivery"]["Streams"]} | saved_info
        streams = Streams.from_dict(streams_info)
        streams.download()
