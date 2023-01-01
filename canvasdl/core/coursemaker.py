import cli
from libs.shortcutmaker import ShortcutMaker
from rich.prompt import Confirm, Prompt

from canvasdl import client
from canvasdl.asset_types import Course
from canvasdl.checkers.canvas import videos
from canvasdl.utils import Path, config


def make_courses():
    courses = client.get_courses()
    courses = ask_courses(courses)
    courses = save_courses(courses)
    return courses


def save_courses(courses: list[Course]):
    make_shortcuts(courses)
    for course in courses:
        (Path.school / course.name).mkdir(parents=True, exist_ok=True)

    courses_dict = [c.dict() for c in courses]
    if config.update_content:
        Path.courses.content = courses_dict

    return courses_dict


# no longer used
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


def make_shortcuts(courses: list[Course]):
    try:
        _make_shortcuts(courses)
    except (ImportError, FileNotFoundError):
        # disable on non-personal machines
        pass


def _make_shortcuts(courses: list[Course]):
    shortcut_maker = ShortcutMaker()
    for i, course in enumerate(courses):
        shortcut_name = course.name.replace(" ", "_").replace("'", "")
        url = f"{config.API_URL}/courses/{course.id}"

        shortcuts = {
            f"checkpoint {shortcut_name}": f'control "c:{10 + i}"',
            # 10, 11, 12 -> 1, 2, 3, ..
            f"checkpoint choose {shortcut_name}": f'control shift "c:{10 + i}"',
            # 67, 68, 69 -> F1, F2, F3, ..
            f"xdg-open {url}": f'control "c:{67 + i}"',
            "": "",
        }

        for target, hotkey in shortcuts.items():
            shortcut_maker.add_shortcut(hotkey, target)

    shortcut_maker.save_shortcuts()


def ask_courses(courses):
    synced_courses = []

    for course in courses:
        name = get_course_name(course)
        question = f"Do you want to synchronize {name}?"
        do_sync = Confirm().ask(question, default=True)
        if do_sync:
            course = Course(name=name, id=course.id)
            original_name = (
                course.original_name
                if hasattr(course, "original_name")
                else course.name
            )

            question = "Do you have an rclone source you want to synchronize with?"
            if Confirm().ask(question):
                rclone_name = Prompt().ask("Rclone source name")
                course.drive_name = rclone_name

            question = "Do you want to synchronize the Piazza posts in this course?"
            if Confirm().ask(question):
                url = Prompt().ask("Piazza url for the course")
                course.piazza_id = url.split("/")[-1]

            question = "Does the course have a custom website you want to synchronize?"
            if Confirm().ask(question):
                root_url = Prompt().ask("Course webpage root url")
                question = (
                    "Does the course have any additional specific subpages you want to"
                    " synchronize?"
                )
                sub_pages = []
                while Confirm().ask(question):
                    sub_pages.append(Prompt.ask("Course subpage sub url"))
                if not sub_pages:
                    sub_pages = [""]
                course.websites = {root_url: sub_pages}

            with cli.status("Saving course"):
                course.video_id = videos.Checker(course).get_folder_id(original_name)
            synced_courses.append(course)

    return synced_courses


def get_course_name(course_info):
    delim = " - "
    name = course_info.name
    if delim in name:
        name = name.split(delim)[1]
    return name
