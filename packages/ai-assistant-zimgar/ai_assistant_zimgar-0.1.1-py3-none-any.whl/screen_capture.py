"""Screen capture utilities."""

import time

import numpy as np
import pyautogui


def capture_screen(path: str) -> None:
    """Save a screenshot to the given file path using PyAutoGUI."""
    screenshot = pyautogui.screenshot()
    screenshot.save(path)


def capture_screenshot(path: str) -> None:
    """Capture a screenshot using the :mod:`mss` library."""
    from mss import mss

    with mss() as sct:
        sct.shot(output=path)


def capture_video(duration: float, path: str, fps: int = 10) -> None:
    """Record the desktop for ``duration`` seconds and save it to ``path``."""
    try:
        import cv2
    except ImportError as exc:
        raise ImportError(
            "OpenCV is required for capture_video. Install 'opencv-python' to use this feature."
        ) from exc

    try:
        from mss import mss
    except ImportError as exc:
        raise ImportError("The 'mss' library is required for capture_video.") from exc

    with mss() as sct:
        monitor = sct.monitors[1]
        width = monitor["width"]
        height = monitor["height"]
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(path, fourcc, fps, (width, height))

        end_time = time.time() + duration
        while time.time() < end_time:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            writer.write(frame)
            time.sleep(1.0 / fps)
        writer.release()
