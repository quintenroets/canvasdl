import requests

from canvasdl.utils import Path

from ...asset_types import SavedVideo, Video
from ...utils import config
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
        session = self.get_authenticated_session()
        folder_id = self.course.video_id

        url = f"{self.api_url}folders/{folder_id}/sessions"
        params = {"sortfield": "CreatedDate", "sortOrder": "Desc"}
        content = session.get(url, params=params).json()["Results"]
        return content

    def get_folder_id(self, name):
        folder_id = None
        if self.should_check():
            session = self.get_authenticated_session()
            url = f"{self.api_url}folders/search"
            params = {"searchQuery": name}
            results = session.get(url, params=params).json()["Results"]
            if results:
                folder_id = results[0]["Id"]

        return folder_id

    def get_authenticated_session(self):
        launch_url = self.get_launch_url()
        launch_response = requests.get(launch_url).text
        url, data = self.parse_form(launch_response)

        cookie_name = f"CVNCanvas\\{config.uni}"
        cookie_value = (
            '{"lastSessionView":1,"sortData-lastSessionWithSearchSort":"{"column":3,"currentAscending":false}",'
            '"sortData-lastSessionSort":"{"column":1,"currentAscending":false}"}]'
        )

        def authenticate(session):
            session.post(url, data=data)
            session.cookies[cookie_name] = cookie_value

        session = requests.Session()
        authenticate(session)
        return session

    def export_downloads(self):
        folder = Path.templates.as_uri()
        css = f'<link href="{folder}/video_index.css" rel="stylesheet" />\n'
        js = f'<script src="{folder}/index_script.js"></script>\n'

        exports = {
            self.path: self.create_video_tags,
            Path.school / "Videos.html": self.create_all_video_tags,
        }
        for path, tag_create_function in exports.items():

            video_tags = tag_create_function()
            body = f"<body style=\"background-image: url('{folder}/background_index.jpg')\">{video_tags}</body>"
            content = css + js + body
            path.text = content
            path.tag = 9999

    def create_video_tags(self):
        paths = sorted(
            list(self.save_folder.iterdir()), key=lambda path: int(path.mtime)
        )
        videos = [SavedVideo.from_dict(path.yaml) for path in paths]
        video_tags = "".join(v.tag for v in videos)
        return video_tags

    def create_all_video_tags(self):
        paths = sorted(
            [
                path
                for folder in self.save_folder.parent.iterdir()
                for path in list(folder.iterdir())
            ],
            key=lambda path: int(path.mtime),
        )
        videos = [SavedVideo.from_dict(path.yaml) for path in paths]
        video_tags = "".join(v.tag for v in videos)
        return video_tags
