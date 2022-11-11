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

    @classmethod
    def clean_table(cls, table: pd.DataFrame) -> pd.DataFrame:
        new_column_names = {n: n.split(" (")[0] for n in table.columns}
        table = table.rename(columns=new_column_names)
        table = table[~table["ReleasedDue"].isnull()]
        return table

    def get_content_table(self) -> pd.DataFrame:
        page = self.get_redirected_content()
        with io.StringIO(page) as fp:
            return pd.read_html(fp)[0]

    def extract_row_info(self, row):
        name = self.course.assignment_name(row["Name"])
        date = row["ReleasedDue"]
        return name, date

    def get_items(self):
        table = self.get_content_table()
        table = self.clean_table(table)
        content = [self.extract_row_info(row) for _, row in table.iterrows()]
        return content

    def make_item(self, item):
        name, date = item
        return Due(name, parse_date(date))


def parse_date(date_str):
    end = "Late Due Date: "
    if end in date_str:
        date_str = date_str.split(end)[0].strip()

    start_pos = date_str.rfind("M", 0, -1)
    date_str = date_str[start_pos + 1 :]
    date = dateutil.parser.parse(date_str)
    return date
