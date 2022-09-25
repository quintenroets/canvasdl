import plib

root = plib.Path(__file__).parent.parent


class Path(plib.Path):
    templates = root.parent / "assets" / "templates"
    assets: plib.Path = plib.Path.assets / root.name
    content_assets = assets / "content"
    config = assets / "config.yaml"
    calendar_credentials = assets / "credentials.json"
    courses = assets / "courses" / "courses.yaml"

    school = plib.Path.docs / "School"

    @classmethod
    def content_path(cls, course, names=[]):
        path = Path.content_assets.subpath(*names, course).with_suffix(".txt")
        path = Path(path)  # convert to right type
        return path
