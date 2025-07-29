# Author: TheRealRazbi (https://github.com/TheRealRazbi)
# License: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from unittest.mock import MagicMock, patch

from dgus_control import ExeStarter
from dgus_control.dgus import DGUS
from stageclick.core import Window

from dgus_control.exceptions import DGUSAlreadyStarted


def test_start_raises_if_dgus_already_running():
    with patch("stageclick.core.Window.find", return_value=MagicMock(spec=Window)):
        with pytest.raises(DGUSAlreadyStarted):
            dgus = DGUS(starter=ExeStarter("path/to/exe"))
            dgus.start()


def test_find_existing_dgus_window():
    mock_window = MagicMock(spec=Window)
    with patch("stageclick.core.Window.find", return_value=mock_window):
        dgus = DGUS(starter=ExeStarter('path/to/exe'))
        dgus.find()
        assert dgus.window == mock_window


def test_selects_window_when_not_visible():
    mock_window = MagicMock(spec=Window, visible=False)
    with patch.object(mock_window, "select") as mock_select:
        dgus = DGUS(starter=ExeStarter('path/to/exe'))
        dgus.window = mock_window
        dgus.select()
        mock_select.assert_called_once()


def test_skips_selection_if_window_is_visible():
    mock_window = MagicMock(spec=Window, visible=True)

    with patch("time.sleep") as mock_sleep, \
            patch.object(mock_window, "select") as mock_select:
        dgus = DGUS(starter=ExeStarter('path/to/exe'))
        dgus.window = mock_window
        dgus.select()
        mock_select.assert_called_once()
        mock_sleep.assert_not_called()
