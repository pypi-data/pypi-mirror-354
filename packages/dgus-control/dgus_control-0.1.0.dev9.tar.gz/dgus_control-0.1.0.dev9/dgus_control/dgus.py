# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time
from dataclasses import dataclass
from pathlib import Path

from stageclick.core import Window, WindowNotFound
from termcolor import cprint

from dgus_control.constants import DGUS_TITLE
from dgus_control.project_picker import DGUSPicker


class DGUSAlreadyStarted(Exception):
    ...


@dataclass
class DGUSTemplates:
    location: Path


class DGUS:
    def __init__(self, window: Window, picker: DGUSPicker = None):
        self.window = window
        self.picker = picker

    @classmethod
    def find_or_start(cls):
        raise NotImplementedError

    @classmethod
    def start(cls, exe_path, wait_until_ready=False, ready_timeout=10, is_ready_template=None, title=DGUS_TITLE):
        try:
            if cls.find(title=title):
                raise DGUSAlreadyStarted
        except WindowNotFound:
            ...
        window = Window.start_and_find(exe_path=exe_path, title=title, wait_seconds=6)
        if wait_until_ready:
            if is_ready_template is None:
                cprint("Skipping is_ready_template because it wasn't provided", "red")
                return cls(window)
            window.wait_for_template(is_ready_template, timeout=ready_timeout)
        return cls(window)

    @classmethod
    def find(cls, timeout=0, title=DGUS_TITLE):
        return cls(Window.find(title, timeout=timeout))

    def select(self):
        already_selected = self.window.visible
        self.window.select()
        if not already_selected:
            time.sleep(0.2)
