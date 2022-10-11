from dataclasses import dataclass
from typing import Any

import downloader
import m3u8

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
    local_url: Path | None = None

    @property
    def id(self):
        return self.url.split("?id=")[1]

    @property
    def filename_title(self):
        return self.title.replace("/", "_")

    def download(self, info, folder: Path):
        folder /= self.id
        streams = info["Delivery"]["Streams"]
        for i, stream in enumerate(streams):
            url = stream["StreamUrl"]
            name = self.filename_title
            if i > 0:
                name += f"__VIEW__{i+1}"
            dest = (folder / name).with_suffix(".mp4")
            if not dest.exists():
                if "m3u8" in url:
                    self.download_m3u8(url, dest)
                else:
                    downloader.download(url, dest)
                dest.mtime = self.mtime
        folder.mtime = self.mtime

    @classmethod
    def download_m3u8(cls, url, dest, headers=None):
        headers = headers or {}
        playlist = m3u8.load(url, headers=headers)
        playlist = m3u8.load(playlist.playlists[0].absolute_uri, headers=headers)
        url = playlist.segments[0].absolute_uri
        downloader.download(url, dest)
