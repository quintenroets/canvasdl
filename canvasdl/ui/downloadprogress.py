from __future__ import annotations

import html
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import cli

try:
    from .widget import Widget  # noqa: autoimport


except (ImportError, ModuleNotFoundError):
    pass

if TYPE_CHECKING:  # noqa: autoimport
    from ..asset_types import Section  # noqa: autoimport


@dataclass
class DownloadProgress:
    section: Section
    finished: bool = False
    to_show: bool = False
    amount: int = 0
    progress_value: int = 0
    widget: Any = None

    def request_widget(self):
        from . import userinterface  # noqa: autoimport

        userinterface.UserInterface.request_widget(self)

    def grant_widget(self):
        message = make_message(self.section)
        self.widget = Widget(message)

        self.widget.onCancel = self.onCancel
        self.widget.onOpen = self.onOpen
        self.widget.onClose = self.onClose
        progress = 1 if self.finished else None
        self.set_progress(progress)

        self.widget.exec()

    def onCancel(self):
        self.widget.close()
        self.widget = None
        raise KeyboardInterrupt

    def onOpen(self):
        if self.finished:
            self.show_download()
        else:
            self.to_show = True

    def onClose(self):
        self.widget.close()
        self.widget = None

    def set_progress(self, progress=None):
        if self.widget is None:
            self.request_widget()

        if self.amount and not progress:
            progress = self.progress_value / self.amount
        if progress and self.widget:
            value = int(progress * 100)
            self.widget.progress.setValue(value)
            if progress == 1:
                self.widget.closeButton.setDisabled(False)
                self.widget.enable_keyclose = True

    def add_progress(self, progress):
        self.progress_value += progress
        self.set_progress()

    def add_amount(self, amount):
        self.amount += amount
        self.set_progress()

    def show_download(self):
        self.onClose()
        cli.urlopen(self.section.path)

    def enable_show(self):
        self.set_progress(1)
        if self.to_show:
            self.show_download()
        else:
            self.finished = True


def make_message(section: Section):
    arrow = "\u2B9E "
    message = "\n".join(
        (
            section.course.name,
            *(i * "   " + arrow + part for i, part in enumerate(section.titles)),
            "",
            *(html.unescape(item.display_title) for item in section.items),
        )
    )
    return message
