# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Protocol


class DGUSStarter(Protocol):
    def start(self, *args, **kwargs) -> None:
        ...


class ManualStarter:
    def start(self):
        raise NotImplementedError


class ExeStarter:
    def start(self):
        raise NotImplementedError
