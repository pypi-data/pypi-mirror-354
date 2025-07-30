import pytest
import requests
import n8n_interface


class DummyResponse:
    def __init__(self, *, data=None, text="", status=200):
        self._data = data
        self.text = text
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        if isinstance(self._data, Exception):
            raise self._data
        return self._data


def test_run_workflow_success(monkeypatch):
    called = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        called["args"] = (url, json, headers, timeout)
        return DummyResponse(data={"ok": True})

    monkeypatch.setattr(n8n_interface, "N8N_BASE_URL", "http://base")
    monkeypatch.setattr(n8n_interface, "N8N_API_KEY", "secret")
    monkeypatch.setattr(n8n_interface.requests, "post", fake_post)

    result = n8n_interface.run_workflow("flow", {"a": 1})
    assert result == {"ok": True}
    assert called["args"] == (
        "http://base/flow",
        {"a": 1},
        {"X-N8N-API-KEY": "secret"},
        10,
    )


def test_run_workflow_http_error(monkeypatch):
    def fake_post(*args, **kwargs):
        return DummyResponse(status=500)

    monkeypatch.setattr(n8n_interface.requests, "post", fake_post)
    with pytest.raises(RuntimeError):
        n8n_interface.run_workflow("bad")


def test_run_workflow_non_json(monkeypatch):
    def fake_post(*args, **kwargs):
        return DummyResponse(data=ValueError(), text="plain")

    monkeypatch.setattr(n8n_interface.requests, "post", fake_post)
    result = n8n_interface.run_workflow("wf")
    assert result == {"response": "plain"}

