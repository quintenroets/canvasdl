from dataclasses import dataclass, field

from canvasdl.utils.path import Path

from . import argparser, configmaker


@dataclass
class Config:
    API_URL: str
    API_KEY: str
    one_course_nr: int = None
    update_content: bool = True
    save_content: bool = True
    google_calendar_id: str = None
    drive: dict[str, str] = field(default_factory=dict)
    website: dict[str, str] = field(default_factory=dict)
    piazza: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls):
        config_path = Path.config
        args = argparser.get_args()
        if not config_path.exists() or args.configure:
            configmaker.make_config()
        return Config(**config_path.yaml)


config = Config.load()
