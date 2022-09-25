from canvasdl.asset_types.course import Courses
from canvasdl.utils import Path


def get_courses():
    from . import coursemaker  # noqa: autoimport

    courses = Path.courses.load()
    if not courses:
        courses = coursemaker.make_courses()

    return Courses.from_dict(courses).courses
