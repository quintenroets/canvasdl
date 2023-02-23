import cli
from plib import Path


class ShortcutMaker:
    def __init__(self):
        self.config_file = Path.HOME / ".xbindkeysrc.scm"
        self.lines = self.config_file.lines
        edge = "; -- scripts --"
        if edge in self.lines:
            self.lines = self.lines[: self.lines.index(edge) + 1]
        self.lines += ["(set-keyboard-bindings", ")"]

    def save_shortcuts(self):
        self.config_file.lines = self.lines
        cli.run("xbindkeys --poll-rc")

    def add_shortcut(self, hotkey, target):
        item = f'\t(list \'({hotkey}) "{target}")' if target else "\n"
        self.lines.insert(-1, item)  # insert before closing parenthese
