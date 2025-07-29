# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["DGUS"]

import time
from typing import Optional

from stageclick.core import Window

from dgus_control.dgus_starter import DGUSStarter
from dgus_control.project_picker import DGUSPicker


class DGUS:
    def __init__(self, starter: DGUSStarter, picker: DGUSPicker = None):
        self.starter = starter
        self.picker = picker
        self.window: Optional['Window'] = None

    def find_or_start(self):
        self.window = self.starter.find_or_start()

    def start(self):
        self.window = self.starter.start()

    def find(self):
        self.window = self.starter.find()

    def select(self):
        already_selected = self.window.visible
        self.window.select()
        if not already_selected:
            time.sleep(0.2)

    def is_running(self):
        return self.window is not None and self.window.is_running()
