"""Simple feedback storage for the assistant."""

from __future__ import annotations

import json
import os
from typing import Dict

__all__ = ["record_feedback", "load_feedback", "get_mood"]

_FEEDBACK_FILE = os.getenv("ASSISTANT_FEEDBACK_FILE", "feedback.json")


def load_feedback(path: str = _FEEDBACK_FILE) -> Dict[str, int]:
    """Return stored feedback counters from ``path``."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    data.setdefault("success", 0)
    data.setdefault("failure", 0)
    return data


def record_feedback(success: bool, path: str = _FEEDBACK_FILE) -> None:
    """Update the feedback file with a success or failure entry."""
    data = load_feedback(path)
    key = "success" if success else "failure"
    data[key] = data.get(key, 0) + 1
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def get_mood(path: str = _FEEDBACK_FILE) -> str:
    """Return the assistant's mood based on feedback counts."""
    data = load_feedback(path)
    score = data.get("success", 0) - data.get("failure", 0)
    if score > 0:
        return "happy"
    if score < 0:
        return "sad"
    return "neutral"
