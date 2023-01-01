import itertools

import dbus

from .silentpopup import SilentUIHandle

session_bus = dbus.SessionBus()


def get_dbus_interface(name, path, interface):
    obj = session_bus.get_object(name, path)
    return dbus.Interface(obj, dbus_interface=interface)


class UIHandle:
    def __new__(self, title, app_icon_name=""):
        ui_interface = get_dbus_interface(
            "org.kde.kuiserver", "/JobViewServer", "org.kde.JobViewServer"
        )
        own_interface_path = ui_interface.requestView(title, app_icon_name, 0)

        handle = get_dbus_interface(
            "org.kde.kuiserver", own_interface_path, "org.kde.JobViewV2"
        )
        return handle


class Popup:
    def __init__(
        self,
        *args,
        title="Working",
        message="",
        progress_name=None,
        amount=0,
        description=False,
        capture_errors=False,
        silent=False,
    ):
        self.handle = UIHandle(title) if not silent else SilentUIHandle()
        self.handle.setInfoMessage(message)

        # title can be given by first argument as well
        if args and isinstance(args[0], str):
            title, *args = args
        self.iterator = itertools.chain(*args) if args else None

        self.amount = amount
        if self.amount == 0 and args:
            try:
                self.amount = sum([len(arg) for arg in args])
            except TypeError:
                pass

        self.progress_name = progress_name
        self.message = message
        self.progress = 0
        self.finished = False

        if amount != 0:
            self.handle.setPercent(1)
        if description:
            self.handle.setDescriptionField(0, "", self.message)

    def __enter__(self):
        return self

    def __exit__(self, _, exception, tb):
        self.show_progress()
        self.finished = True

        if not exception:
            message = ""
        elif isinstance(exception, KeyboardInterrupt):
            message = "Cancelled"
        else:
            message = "Error"

        self.handle.setInfoMessage("")
        self.handle.terminate(message)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.show_progress()

    def increase_progress(self, value=1):
        self._progress += value

    @property
    def percentage(self):
        return 100 * self.progress / self.amount

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.show_progress_message()

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def increase_amount(self, value=1):
        self._amount += value

    def show_progress(self):
        if self.amount != 0 and self.amount is not None:
            # Don't go backwards
            percentage = min(self.percentage, 100)
            self.handle.setPercent(percentage)
            self.show_progress_message()

    def show_progress_message(self):
        message = (
            f"{self.message}\n{self.progress}/{self.amount} {self.progress_name}"
            if self.progress_name
            else self.message
        )
        self.handle.setInfoMessage(message)

    def __iter__(self):
        with self:
            for item in self.iterator:
                yield item
                self.progress += 1

    def iterate(self, iterator):
        self.iterator = iterator
        return self.__iter__()
