# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time
from dataclasses import dataclass

from stageclick import Window

from dgus_control.constants import DGUS_TITLE


@dataclass
class Dgus:
    window: Window

    @classmethod
    def find(cls, timeout=0):
        return cls(Window.find(DGUS_TITLE, timeout=timeout))

    def select(self):
        already_selected = self.window.visible
        self.window.select()
        if not already_selected:
            time.sleep(0.2)
