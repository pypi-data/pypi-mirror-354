"""Voice recording and transcription utilities."""

from __future__ import annotations

import speech_recognition as sr

__all__ = ["listen_and_transcribe"]


def listen_and_transcribe() -> str:
    """Record audio from the default microphone and return the transcribed text.

    This uses the ``speech_recognition`` package with the Google Web Speech API.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition request failed: {exc}") from exc

