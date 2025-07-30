import sys
import types
import importlib
from unittest.mock import MagicMock

import pytest


def test_capture_screen(monkeypatch):
    pyautogui = types.ModuleType('pyautogui')
    screenshot_mock = MagicMock()
    pyautogui.screenshot = MagicMock(return_value=screenshot_mock)
    monkeypatch.setitem(sys.modules, 'pyautogui', pyautogui)
    # provide dummy numpy module for import
    numpy = types.ModuleType('numpy')
    monkeypatch.setitem(sys.modules, 'numpy', numpy)

    import screen_capture
    importlib.reload(screen_capture)

    screen_capture.capture_screen('out.png')
    pyautogui.screenshot.assert_called_once_with()
    screenshot_mock.save.assert_called_once_with('out.png')
