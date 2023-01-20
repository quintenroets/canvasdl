from canvasdl.asset_types.course import Courses
from canvasdl.utils import Path


def get_courses():
    from . import coursemaker  # noqa: autoimport

    courses = (
        Path.courses.load() if Path.courses.exists() else coursemaker.make_courses()
    )
    courses = Courses.from_dict(courses)
    return courses.courses
