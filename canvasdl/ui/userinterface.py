import sys
import threading

WITH_UI = True

try:
    from PyQt6 import QtWidgets  # noqa: autoimport
except (ModuleNotFoundError, ImportError):
    WITH_UI = False

cond = threading.Condition()


class UserInterface:
    tasks = []
    to_show = 0
    checked = 0

    @classmethod
    def tasks_are_remaining(cls, done, to_check):
        return WITH_UI & (done < cls.to_show or cls.checked < to_check)

    @classmethod
    def show_progress(cls, to_check):
        done = 0
        app = None

        while cls.tasks_are_remaining(done, to_check):
            if not cls.tasks or cls.checked < to_check:
                with cond:
                    cond.wait()
            if cls.tasks:
                if app is None:
                    app = QtWidgets.QApplication(sys.argv)
                download_progress = UserInterface.tasks.pop(0)
                download_progress.grant_widget()
                done += 1
                with cond:  # allow new tasks
                    cond.notify_all()

    @classmethod
    def add_check(cls):
        cls.checked += 1
        with cond:
            cond.notify_all()

    @classmethod
    def request_widget(cls, download_progress):
        if download_progress not in cls.tasks:
            with cond:
                cls.to_show += 1
                cls.tasks.append(download_progress)
                cond.notify_all()
