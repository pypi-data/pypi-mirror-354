import pytest
from unittest.mock import MagicMock, patch
from dgus_control.dgus import DGUS, DGUSAlreadyStarted, DGUSTemplates
from stageclick import Window


def test_start_raises_if_dgus_already_running():
    with patch("stageclick.Window.find", return_value=MagicMock(spec=Window)):
        with pytest.raises(DGUSAlreadyStarted):
            DGUS.start(exe_path="path/to/exe")


def test_find_existing_dgus_window():
    mock_window = MagicMock(spec=Window)
    with patch("stageclick.Window.find", return_value=mock_window):
        dgus_instance = DGUS.find(title="DGUS_TITLE")
        assert isinstance(dgus_instance, DGUS)
        assert dgus_instance.window == mock_window


def test_selects_window_when_not_visible():
    mock_window = MagicMock(spec=Window, visible=False)
    with patch.object(mock_window, "select") as mock_select:
        dgus_instance = DGUS(mock_window)
        dgus_instance.select()
        mock_select.assert_called_once()


def test_skips_selection_if_window_is_visible():
    mock_window = MagicMock(spec=Window, visible=True)

    with patch("time.sleep") as mock_sleep, \
            patch.object(mock_window, "select") as mock_select:
        dgus_instance = DGUS(mock_window)
        dgus_instance.select()

        mock_select.assert_called_once()
        mock_sleep.assert_not_called()
