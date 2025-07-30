import builtins
import sys
import importlib

import types
import pytest


dummy_pg = types.ModuleType('pyautogui')
dummy_pg.screenshot = lambda: types.SimpleNamespace(save=lambda p: None)
dummy_np = types.ModuleType('numpy')
sys.modules.setdefault('pyautogui', dummy_pg)
sys.modules.setdefault('numpy', dummy_np)
dummy_pynput = types.ModuleType('pynput')
keyboard_mod = types.ModuleType('pynput.keyboard')
keyboard_mod.Controller = lambda: types.SimpleNamespace(type=lambda t: None)
dummy_pynput.keyboard = keyboard_mod
sys.modules.setdefault('pynput', dummy_pynput)
sys.modules.setdefault('pynput.keyboard', keyboard_mod)
dummy_sr = types.ModuleType('speech_recognition')
dummy_sr.Microphone = object
dummy_sr.Recognizer = lambda: None
dummy_sr.UnknownValueError = type('e', (), {})
dummy_sr.RequestError = type('e', (), {})
sys.modules.setdefault('speech_recognition', dummy_sr)

import main


def test_screenshot_path(monkeypatch):
    called = {}
    def fake_capture(path):
        called['path'] = path
    monkeypatch.setattr(builtins, 'input', lambda *args: 'y')
    argv = ['prog', 'hi', '--screenshot-path', 'out.png']
    monkeypatch.setattr(sys, 'argv', argv)
    importlib.reload(main)
    monkeypatch.setattr(main, 'capture_screen', fake_capture)
    monkeypatch.setattr(main, 'generate_response', lambda prompt, provider=None: 'resp')
    main.main()
    assert called['path'] == 'out.png'


def test_capture_screen_error(monkeypatch, capsys):
    def boom(path):
        raise RuntimeError('fail')

    monkeypatch.setattr(builtins, 'input', lambda *args: 'y')
    argv = ['prog', 'hi', '--screenshot']
    monkeypatch.setattr(sys, 'argv', argv)
    importlib.reload(main)
    monkeypatch.setattr(main, 'capture_screen', boom)
    monkeypatch.setattr(main, 'generate_response', lambda prompt, provider=None: 'resp')

    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 1
    assert 'Error capturing screen: fail' in capsys.readouterr().err


def test_voice_input_error(monkeypatch, capsys):
    def boom():
        raise RuntimeError('mic')

    argv = ['prog', '--voice']
    monkeypatch.setattr(sys, 'argv', argv)
    importlib.reload(main)
    monkeypatch.setattr(main, 'listen_and_transcribe', boom)
    monkeypatch.setattr(main, 'generate_response', lambda prompt, provider=None: 'resp')

    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 1
    assert 'Error capturing voice input: mic' in capsys.readouterr().err


def test_llm_error(monkeypatch, capsys):
    def boom(prompt, provider=None):
        raise RuntimeError('nope')

    monkeypatch.setattr(builtins, 'input', lambda *args: 'y')
    argv = ['prog', 'hello']
    monkeypatch.setattr(sys, 'argv', argv)
    importlib.reload(main)
    monkeypatch.setattr(main, 'generate_response', boom)

    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 1
    assert 'Error calling language model: nope' in capsys.readouterr().err

