from abc import ABC
from dataclasses import dataclass

from canvasdl import client

from .. import base


@dataclass
class Checker(base.Checker, ABC):
    @property
    def api(self):
        return client.get_course(self.course.id)
