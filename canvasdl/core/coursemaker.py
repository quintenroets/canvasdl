from typing import List

from libs.shortcutmaker import ShortcutMaker

from canvasdl import client
from canvasdl.asset_types import Course
from canvasdl.checkers.canvas import videos
from canvasdl.utils import Path, config


def make_courses():
    courses = client.get_courses()
    courses = parse_courses(courses)

    make_shortcuts(courses)
    for course in courses:
        (Path.school / course.name).mkdir(parents=True, exist_ok=True)

    courses_dict = [c.dict() for c in courses]
    if config.update_content:
        Path.courses.content = courses_dict

    return courses_dict


def parse_courses(courses):
    def parse_name(name: str):
        delim = " - "
        return name.split(delim)[1] if delim in name else name

    def include_course(course):
        return hasattr(course, "original_name")  # check if nickname given

    courses = [c for c in courses if include_course(c)]
    parsed_courses = []

    for c in courses:
        course = Course(name=parse_name(c.name), id=c.id)
        video_id = videos.Checker(course).get_folder_id(c.original_name)
        course.video_id = video_id
        parsed_courses.append(course)

    courses = sorted(parsed_courses, key=lambda item: item.name.lower())
    return courses


def make_shortcuts(courses: List[Course]):
    shortcut_maker = ShortcutMaker()
    for i, course in enumerate(courses):
        shortcut_name = course.name.replace(" ", "_").replace("'", "")
        url = f"https://courseworks2.columbia.edu/courses/{course.id}"

        shortcuts = {
            f"checkpoint {shortcut_name}": f'control "c:{10 + i}"',
            f"checkpoint choose {shortcut_name}": f'control shift "c:{10 + i}"',  # 10, 11, 12 -> 1, 2, 3, ..
            f"xdg-open {url}": f'control "c:{67 + i}"',  # 67, 68, 69 -> F1, F2, F3, ..
            "": "",
        }

        for target, hotkey in shortcuts.items():
            shortcut_maker.add_shortcut(hotkey, target)

    shortcut_maker.save_shortcuts()
