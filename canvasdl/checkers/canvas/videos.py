from functools import cached_property

import requests
import video_exporter

from canvasdl.utils import Path

from ...asset_types import SavedVideo, Video
from . import tab


class Checker(tab.Checker):
    @classmethod
    def tab_name(cls):
        return "Video Library"

    @property
    def api_url(self):
        return "https://cvn.hosted.panopto.com/Panopto/api/v1/"

    @property
    def path(self):
        return super().path / "Videos.html"

    def __post_init__(self):
        super().__post_init__()
        self.save_folder = Path.content_path(self.course.name, ("videos",)).with_suffix(
            ""
        )

    def make_item(self, item):
        item |= dict(save_folder=self.save_folder)
        return Video.from_dict(item)

    def get_items(self):
        session = self.authenticated_session
        folder_id = self.course.video_id

        if folder_id:
            url = f"{self.api_url}folders/{folder_id}/sessions"
            params = {"sortfield": "CreatedDate", "sortOrder": "Desc"}
            # pageNumber, https://demo.hosted.panopto.com/Panopto/api/docs
            # /index.html#/Folders/Folders_GetSessions
            response = session.get(url, params=params)
            content = response.json()["Results"]
        else:
            content = []
        return content

    def get_folder_id(self, name):
        folder_id = None
        if self.should_check():
            url = f"{self.api_url}folders/search"
            params = {"searchQuery": name}
            response = self.authenticated_session.get(url, params=params)
            results = response.json()["Results"]
            if results:
                folder_id = results[0]["Id"]

        return folder_id

    @cached_property
    def authenticated_session(self):
        launch_url = self.get_launch_url()
        launch_response = requests.get(launch_url).text
        url, data = self.parse_form(launch_response)
        session = requests.Session()
        session.post(url, data=data)

        uni = data["lis_person_sourcedid"]
        cookie = {
            f"CVNCanvas\\{uni}": (
                '{"lastSessionView":1,"sortData-lastSessionWithSearchSort":'
                '"{"column":3,"currentAscending":false}",'
                '"sortData-lastSessionSort":"{"column":1,"currentAscending":false}"}]'
            )
        }
        session.cookies.update(cookie)

        return session

    def export_downloads(self):
        self.download_recordings()
        self.export_html_files()

    def export_html_files(self):
        exports = {
            self.path: self.download_folder,
            Path.school / "Videos.html": list(self.download_folder.parent.iterdir()),
        }
        for dest, video_folders in exports.items():
            video_exporter.export(video_folders, dest, merge_folders=True)

    @property
    def download_folder(self):
        return (
            self.save_folder.parent.parent / "video_downloads" / self.save_folder.name
        )

    def download_recordings(self):
        for path in self.save_folder.iterdir():
            video = SavedVideo.from_dict(path.yaml)
            self.download_streams(video)

    def get_api(self, data):
        post_url = (
            "https://cvn.hosted.panopto.com/Panopto/Pages/Viewer/DeliveryInfo.aspx"
        )
        return self.authenticated_session.post(post_url, data=data).json()

    def download_streams(self, video: SavedVideo):
        info = self.get_api({"deliveryId": video.id, "responseType": "json"})
        video.download(info, self.download_folder)
