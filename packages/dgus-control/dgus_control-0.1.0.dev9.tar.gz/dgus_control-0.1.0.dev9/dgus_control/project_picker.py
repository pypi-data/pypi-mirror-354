# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Protocol

from stageclick.core import Window


class DGUSPicker(Protocol):
    def pick(self, window: Window, project_name: str) -> None:
        ...


class ManualPicker:
    def pick(self, *args, **kwargs):
        raise NotImplementedError


class TemplatePicker:
    def pick(self, *args, **kwargs):
        return NotImplementedError


class OCRPicker:
    def pick(self, *args, **kwargs):
        raise NotImplementedError
