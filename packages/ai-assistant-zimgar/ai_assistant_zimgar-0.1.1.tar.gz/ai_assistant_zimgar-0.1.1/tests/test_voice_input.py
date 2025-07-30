import sys
import types
import importlib
import pytest



def test_listen_and_transcribe(monkeypatch):
    sr = types.ModuleType("speech_recognition")

    class DummyMicrophone:
        def __enter__(self):
            return "src"

        def __exit__(self, exc_type, exc, tb):
            pass

    class UnknownValueError(Exception):
        pass

    class RequestError(Exception):
        pass

    sr.Microphone = DummyMicrophone
    sr.UnknownValueError = UnknownValueError
    sr.RequestError = RequestError

    audio = object()

    class DummyRecognizer:
        def __init__(self, outcome):
            self.outcome = outcome

        def listen(self, source):
            assert source == "src"
            return audio

        def recognize_google(self, audio_in):
            assert audio_in is audio
            if isinstance(self.outcome, Exception):
                raise self.outcome
            return self.outcome

    monkeypatch.setitem(sys.modules, "speech_recognition", sr)

    import voice_input

    # success
    sr.Recognizer = lambda: DummyRecognizer("ok")
    importlib.reload(voice_input)
    assert voice_input.listen_and_transcribe() == "ok"

    # unknown value
    sr.Recognizer = lambda: DummyRecognizer(UnknownValueError())
    importlib.reload(voice_input)
    assert voice_input.listen_and_transcribe() == ""

    # request error
    sr.Recognizer = lambda: DummyRecognizer(RequestError("bad"))
    importlib.reload(voice_input)
    with pytest.raises(RuntimeError):
        voice_input.listen_and_transcribe()


def test_listen_and_transcribe_with_patch(monkeypatch):
    """Ensure listen_and_transcribe handles different recognizer outcomes."""
    import voice_input

    sr = types.ModuleType("speech_recognition")

    class DummyMicrophone:
        def __enter__(self):
            return "src"

        def __exit__(self, exc_type, exc, tb):
            pass

    class UnknownValueError(Exception):
        pass

    class RequestError(Exception):
        pass

    sr.Microphone = DummyMicrophone
    sr.UnknownValueError = UnknownValueError
    sr.RequestError = RequestError

    audio = object()

    class DummyRecognizer:
        def __init__(self, outcome):
            self.outcome = outcome

        def listen(self, source):
            assert source == "src"
            return audio

        def recognize_google(self, audio_in):
            assert audio_in is audio
            if isinstance(self.outcome, Exception):
                raise self.outcome
            return self.outcome

    def make_recognizer():
        return DummyRecognizer(sr._outcome)

    sr.Recognizer = make_recognizer
    sr._outcome = None

    monkeypatch.setattr(voice_input, "sr", sr)

    sr._outcome = "ok"
    assert voice_input.listen_and_transcribe() == "ok"

    sr._outcome = UnknownValueError()
    assert voice_input.listen_and_transcribe() == ""

    sr._outcome = RequestError("bad")
    with pytest.raises(RuntimeError):
        voice_input.listen_and_transcribe()
