# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['DGUSStarter', 'ExeStarter', 'ManualStarter']

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from stageclick.core import Window, WindowNotFound
from stageclick.step_runner import StepRunner, is_done, grab_input_once, grab_y_n_bool
from termcolor import cprint

from dgus_control import DGUS_TITLE
from dgus_control.exceptions import DGUSAlreadyStarted


class DGUSStarter(Protocol):
    def start(self, *args, **kwargs) -> Window:
        ...

    def find(self, *args, **kwargs) -> Window:
        ...

    def find_or_start(self, *args, **kwargs) -> Window:
        ...


@dataclass
class ManualStarter:
    runner: StepRunner = field(default_factory=lambda: StepRunner('Manual Starter'))
    title: str = DGUS_TITLE

    @staticmethod
    def _find_dgus_by_exe_path(path):
        return Window.find_window_by_exe_path(path)

    def _input_function(self):
        def _is_valid(n):
            try:
                path = Path(n.strip('\'"'))
            except Exception as e:
                cprint(f"Error: {e}", "red")
                return
            if not path.exists():
                cprint(f"Exe path {path} doesn't exist", "red")
                return
            try:
                return self._find_dgus_by_exe_path(n)
            except WindowNotFound:
                cprint(f"DGUS not found by exe path {n}", "red")
                return

        def _process_result(n):
            window = self._find_dgus_by_exe_path(n.strip('\'"'))
            window.set_title(self.title)
            return window

        return grab_input_once(_is_valid, _process_result)

    def start(self, *args, **kwargs):
        self.runner.step("Please start the DGUS manually, 'done' when ready", is_done, skip_allowed=False)
        self.runner.step("Provide the path to the DGUS executable", self._input_function(), skip_allowed=False,
                         save_key="dgus_window")
        window: Window = self.runner.state['dgus_window']
        return window

    def find(self, *args, **kwargs):
        try:
            return Window.find(self.title)
        except WindowNotFound:
            if not kwargs.get('skip_start', False):
                self.runner.step(f"Window with title {self.title} not found, y for start(), n for quit()",
                                 grab_y_n_bool(), skip_allowed=False, save_key="start_confirm")
                if self.runner.state["start_confirm"]:
                    return self.start()
            raise

    def find_or_start(self, *args, **kwargs):
        try:
            return self.find(skip_start=True)
        except WindowNotFound:
            return self.start()


@dataclass
class ExeStarter:
    exe_path: str
    title: str = DGUS_TITLE
    wait_seconds: int = 6

    def start(self, *args, **kwargs):
        try:
            if Window.find(title=self.title):
                raise DGUSAlreadyStarted
        except WindowNotFound:
            ...
        window = Window.start_and_find(exe_path=self.exe_path, title=self.title, wait_seconds=self.wait_seconds)
        return window

    def find(self, *args, **kwargs):
        return Window.find(self.title)

    def find_or_start(self, *args, **kwargs):
        try:
            return self.find()
        except WindowNotFound:
            return self.start()
