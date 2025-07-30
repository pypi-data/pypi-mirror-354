import sys
import types
import importlib
from unittest.mock import MagicMock



def test_desktop_control_functions(monkeypatch):
    pyautogui = types.ModuleType("pyautogui")
    pyautogui.moveTo = MagicMock()
    pyautogui.click = MagicMock()
    monkeypatch.setitem(sys.modules, "pyautogui", pyautogui)

    controller_instance = MagicMock()
    ControllerClass = MagicMock(return_value=controller_instance)
    keyboard_module = types.ModuleType("pynput.keyboard")
    keyboard_module.Controller = ControllerClass
    pynput = types.ModuleType("pynput")
    pynput.keyboard = keyboard_module
    monkeypatch.setitem(sys.modules, "pynput", pynput)
    monkeypatch.setitem(sys.modules, "pynput.keyboard", keyboard_module)

    import desktop_control
    importlib.reload(desktop_control)

    desktop_control.move_mouse(100, 200)
    pyautogui.moveTo.assert_called_once_with(100, 200)

    desktop_control.click("right")
    pyautogui.click.assert_called_once_with(button="right")

    desktop_control.type_text("text")
    controller_instance.type.assert_called_once_with("text")


def test_move_mouse_click_type_text_with_patch(monkeypatch):
    """Verify desktop_control uses pyautogui and pynput correctly after import."""
    import desktop_control

    move_mock = MagicMock()
    click_mock = MagicMock()
    monkeypatch.setattr(desktop_control.pyautogui, "moveTo", move_mock)
    monkeypatch.setattr(desktop_control.pyautogui, "click", click_mock)

    keyboard_mock = MagicMock()
    monkeypatch.setattr(desktop_control, "keyboard", keyboard_mock)

    desktop_control.move_mouse(10, 20)
    move_mock.assert_called_once_with(10, 20)

    desktop_control.click("right")
    click_mock.assert_called_once_with(button="right")

    desktop_control.type_text("hello")
    keyboard_mock.type.assert_called_once_with("hello")
