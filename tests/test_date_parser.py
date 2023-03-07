from datetime import datetime

import pytest

from canvasdl.checkers import gradescope

parsing_pairs = [
    (
        (
            "2 weeks, 6 days leftMar 07 at 4:10PMMar 28 "
            "at 4:10PM Late Due Date: Apr 01 at 11"
        ),
        datetime(2023, 3, 28, 16, 10),
    )
]


@pytest.mark.parametrize("date_str, parsed_date", parsing_pairs)
def test_date_parser(date_str, parsed_date):
    assert gradescope.parse_date(date_str) == parsed_date
