import json
from dataclasses import asdict, dataclass

import dacite


@dataclass
class Item:
    @classmethod
    def from_dict(cls, data):
        if isinstance(data, list):
            data = {"items": data}
        return dacite.from_dict(cls, data) 

    @classmethod
    def from_bytes(cls, data):
        return cls.from_dict(json.loads(data)) if data else cls()

    @classmethod
    def from_response(cls, response):
        return cls.from_dict(response.__dict__)

    def dict(self):
        return asdict(self)


@dataclass
class SaveItem(Item):
    @classmethod
    def save(cls):
        raise NotImplementedError

    @property
    def display_title(self):
        raise NotImplementedError

    @property
    def save_id(self):
        raise NotImplementedError

    @classmethod
    def should_download(cls):
        return True
