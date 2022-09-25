import sys
import threading

from PyQt6 import QtWidgets

cond = threading.Condition()


class UserInterface:
    tasks = []
    to_show = 0
    checked = 0

    @staticmethod
    def show_progress(to_check):
        done = 0
        app = None

        while done < UserInterface.to_show or UserInterface.checked < to_check:
            if not UserInterface.tasks or UserInterface.checked < to_check:
                with cond:
                    cond.wait()
            if UserInterface.tasks:
                if app is None:
                    app = QtWidgets.QApplication(sys.argv)
                download_progress = UserInterface.tasks.pop(0)
                download_progress.grant_widget()
                done += 1
                with cond:  # allow new tasks
                    cond.notify_all()

    @staticmethod
    def add_check():
        UserInterface.checked += 1
        with cond:
            cond.notify_all()

    @staticmethod
    def request_widget(download_progress):
        if download_progress not in UserInterface.tasks:
            with cond:
                UserInterface.to_show += 1
                UserInterface.tasks.append(download_progress)
                cond.notify_all()
