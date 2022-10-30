import io
from dataclasses import dataclass

import dateutil.parser
import pandas as pd

from ..asset_types import Due
from .canvas import assignment, tab


@dataclass
class Checker(assignment.Checker, tab.Checker):
    @classmethod
    def tab_name(cls):
        return "Gradescope"

    def get_items(self):
        page = self.get_redirected_content()
        with io.StringIO(page) as fp:
            table = pd.read_html(fp)[0]
        table = table[~table["ReleasedDue (EDT)"].isnull()]
        content = [
            (self.course.assignment_name(row["Name"]), row["ReleasedDue (EDT)"])
            for i, row in table.iterrows()
        ]

        return content

    def make_item(self, item):
        name, date = item
        return Due(name, parse_date(date))


def parse_date(date_str):
    end = "Late Due Date: "
    if end in date_str:
        date_str = date_str.split(end)[0]

    start_pos = date_str.rfind("M", 0, -1)
    date_str = date_str[start_pos + 1 :]
    date = dateutil.parser.parse(date_str)
    return date
