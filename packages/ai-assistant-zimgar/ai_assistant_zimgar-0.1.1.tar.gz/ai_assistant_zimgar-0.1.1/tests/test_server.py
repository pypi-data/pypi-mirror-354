from fastapi.testclient import TestClient
import asyncio
import server


def test_post_prompt(monkeypatch):
    async def fake_generate(prompt: str) -> str:
        # ensure the endpoint awaits this coroutine
        await asyncio.sleep(0)
        return f"reply:{prompt}"

    monkeypatch.setattr(server, "async_generate_response", fake_generate)
    client = TestClient(server.app)
    resp = client.post("/prompt", json={"prompt": "hi"})
    assert resp.status_code == 200
    assert resp.json() == {"response": "reply:hi"}


def test_post_prompt_error(monkeypatch):
    async def fake_generate(prompt: str) -> str:
        raise RuntimeError("boom")

    monkeypatch.setattr(server, "async_generate_response", fake_generate)
    client = TestClient(server.app)
    resp = client.post("/prompt", json={"prompt": "oops"})
    assert resp.status_code == 500
    assert resp.json() == {"detail": "boom"}


def test_static_files_served():
    client = TestClient(server.app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "AI Assistant" in resp.text
