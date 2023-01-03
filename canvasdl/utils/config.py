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
        args = argparser.get_args()
        if args.configure or not cls.config_file().exists():
            configmaker.make_config()
        config_dict = cls.config_file().yaml
        return Config(**config_dict)

    @classmethod
    def config_file(cls):
        return Path.config if Path.config.exists() else Path.config.encrypted


config = Config.load()
