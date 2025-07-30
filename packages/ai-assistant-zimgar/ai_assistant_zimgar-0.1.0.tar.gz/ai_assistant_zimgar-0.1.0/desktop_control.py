"""Desktop automation utilities."""

import pyautogui
from pynput.keyboard import Controller as KeyboardController

keyboard = KeyboardController()


def move_mouse(x: int, y: int) -> None:
    """Move mouse to the specified screen coordinates."""
    pyautogui.moveTo(x, y)


def click(button: str = "left") -> None:
    """Click the specified mouse button."""
    pyautogui.click(button=button)


def type_text(text: str) -> None:
    """Type the provided text using the keyboard."""
    keyboard.type(text)
