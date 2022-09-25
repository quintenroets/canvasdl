from dataclasses import dataclass, field
from typing import Dict

import cli

from canvasdl.utils.path import Path


@dataclass
class Config:
    API_URL: str
    uni: str
    one_course_nr: int = None
    update_content: bool = True
    save_content: bool = True
    drive: Dict[str, str] = field(default_factory=dict)
    website: Dict[str, str] = field(default_factory=dict)
    piazza: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self.API_KEY: str = cli.get("pw CANVAS_API_KEY")

    @classmethod
    def load(cls):
        return Config(**Path.config.yaml)
