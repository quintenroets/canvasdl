from libs.threading import Threads

from canvasdl.checkers import get_checkers
from canvasdl.ui.userinterface import UserInterface

from . import courseinfo


def check_changes():
    courses = courseinfo.get_courses()
    checkers = get_checkers()
    course_checkers = [
        checker.Checker(course) for course in courses for checker in checkers
    ]
    course_checkers = [checker for checker in course_checkers if checker.should_check()]
    content_threads = Threads([c.check for c in course_checkers]).start()
    UserInterface.show_progress(len(course_checkers))
    content_threads.join()
