# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['DGUSPicker', 'ManualPicker', 'TemplatePicker', 'OCRPicker']

from dataclasses import dataclass
from typing import Protocol

from numpy import ndarray
from stageclick.core import Window, Button

from dgus_control.log import log_colored


class DGUSPicker(Protocol):
    def pick(self, window: Window, project_name: str) -> None:
        ...


class ManualPicker:
    def pick(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class TemplateProject:
    select_path_template: ndarray
    top_path_template: ndarray


@dataclass
class TemplatePicker:
    options: dict[str, TemplateProject]
    click_offset: tuple[int, int] = 80, 15
    wait_until_ready: bool = True
    timeout_ready: float = 5.0

    def pick(self, window: Window, project_name: str):
        project = self.options[project_name]
        Button(window, project.select_path_template, click_offset=self.click_offset).click()
        log_colored(f"Picking project {project_name}...", "yellow")
        if self.wait_until_ready:
            window.wait_for_template(project.top_path_template, timeout=self.timeout_ready)
            log_colored(f"Project {project_name} picked successfully.", "green")


class OCRPicker:
    def pick(self, *args, **kwargs):
        raise NotImplementedError
