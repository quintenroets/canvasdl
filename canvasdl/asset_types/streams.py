from __future__ import annotations

from dataclasses import dataclass
from typing import List

import cli
import downloader
import m3u8

from ..utils import Path
from . import base


@dataclass
class RelativeSegment(base.Item):
    RelativeStart: float


@dataclass
class Stream(base.Item):
    RelativeStart: float
    RelativeEnd: float
    StreamUrl: str
    RelativeSegments: List[RelativeSegment] | None

    @property
    def duration(self):
        return self.RelativeEnd - self.RelativeStart

    @property
    def to_download(self):
        return self.duration > 20

    @property
    def start(self):
        return (
            self.RelativeSegments[0].RelativeStart
            if self.RelativeSegments
            else self.RelativeStart
        )


@dataclass
class DownloadStream(Stream):
    index: int
    streams: Streams

    @property
    def name(self):
        name = self.streams.name
        if self.index > 0:
            name += f"__VIEW__{self.index + 1}"
        return name

    @property
    def dest(self):
        return (self.streams.folder / self.name).with_suffix(".mp4")

    def download(self):
        if self.to_download and not self.dest.exists():
            self.start_download()

    def start_download(self):
        if "m3u8" in self.StreamUrl:
            download_m3u8(self.StreamUrl, self.dest)
        else:
            downloader.download(self.StreamUrl, self.dest)
        self.synchronize_download_start()
        self.dest.mtime = self.streams.mtime

    def synchronize_download_start(self):
        offset_difference = self.streams.start - self.start
        cut(self.dest, offset_difference)


@dataclass
class Streams(base.Item):
    streams: List[Stream]
    folder: Path
    name: str
    mtime: float

    @property
    def streams_to_download(self):
        for stream in self.streams:
            if stream.to_download:
                yield stream

    @property
    def start(self):
        return max([s.start for s in self.streams_to_download])

    def download(self):
        for i, stream in enumerate(self.streams_to_download):
            stream_info = stream.dict() | dict(streams=self, index=i)
            stream = DownloadStream.from_dict(stream_info)
            stream.download()
        if self.folder.exists():
            self.folder.mtime = self.mtime


def download_m3u8(url: str, dest: Path, headers=None):
    headers = headers or {}
    playlist = m3u8.load(url, headers=headers)
    playlist = m3u8.load(playlist.playlists[0].absolute_uri, headers=headers)
    url = playlist.segments[0].absolute_uri
    downloader.download(url, dest)


def cut(dest: Path, start_offset):
    with Path.tempfile().with_suffix(dest.suffix) as tmp:
        args = (
            "ffmpeg",
            "-i",
            dest,
            "-ss",
            start_offset,
            "-vcodec",
            "copy",
            "-acodec",
            "copy",
            tmp,
        )
        cli.get(args)
        tmp.copy_to(dest)
