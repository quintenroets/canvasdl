from datetime import datetime

from dateutil import parser


def parse_time(time_string: str):
    return parser.parse(time_string).timestamp()


def export_time(time_str: str):
    return datetime.fromtimestamp(parse_time(time_str))


def export_datetime(date: datetime):
    return date.strftime("%d-%m-%Y %H:%M")


def export_mtime(mtime: float):
    date = datetime.fromtimestamp(mtime)
    return export_datetime(date)
