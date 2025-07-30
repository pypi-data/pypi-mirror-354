import pytest

import asyncio
import llm_interface


def test_generate_response_openai(monkeypatch):
    called = {}
    def fake_call(prompt, model, api_key, base_url=None):
        called['args'] = (prompt, model, api_key, base_url)
        return 'reply'
    monkeypatch.setattr(llm_interface, '_call_openai', fake_call)
    monkeypatch.setenv('OPENAI_API_KEY', 'key')
    result = llm_interface.generate_response('hi', provider='openai', model='model')
    assert result == 'reply'
    assert called['args'] == ('hi', 'model', 'key', llm_interface.OPENAI_BASE_URL)


def test_generate_response_ollama(monkeypatch):
    called = {}
    def fake_call(prompt, model, base_url):
        called['args'] = (prompt, model, base_url)
        return 'ok'
    monkeypatch.setattr(llm_interface, '_call_ollama', fake_call)
    result = llm_interface.generate_response('hey', provider='ollama', model='m')
    assert result == 'ok'
    assert called['args'] == ('hey', 'm', llm_interface.OLLAMA_BASE_URL)


def test_generate_response_unknown_provider():
    with pytest.raises(ValueError):
        llm_interface.generate_response('x', provider='bad')


def test_async_generate_response_openai(monkeypatch):
    called = {}

    async def fake_call(prompt, model, api_key, base_url=None):
        called['args'] = (prompt, model, api_key, base_url)
        return 'reply'

    monkeypatch.setattr(llm_interface, '_call_openai_async', fake_call)
    monkeypatch.setenv('OPENAI_API_KEY', 'key')
    result = asyncio.run(
        llm_interface.async_generate_response('hi', provider='openai', model='model')
    )
    assert result == 'reply'
    assert called['args'] == ('hi', 'model', 'key', llm_interface.OPENAI_BASE_URL)


def test_async_generate_response_ollama(monkeypatch):
    called = {}

    async def fake_call(prompt, model, base_url):
        called['args'] = (prompt, model, base_url)
        return 'ok'

    monkeypatch.setattr(llm_interface, '_call_ollama_async', fake_call)
    result = asyncio.run(
        llm_interface.async_generate_response('hey', provider='ollama', model='m')
    )
    assert result == 'ok'
    assert called['args'] == ('hey', 'm', llm_interface.OLLAMA_BASE_URL)


def test_async_generate_response_unknown_provider():
    with pytest.raises(ValueError):
        asyncio.run(llm_interface.async_generate_response('x', provider='bad'))
