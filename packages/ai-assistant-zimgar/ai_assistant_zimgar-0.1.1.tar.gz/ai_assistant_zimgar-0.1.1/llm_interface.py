"""LLM interaction utilities."""

from __future__ import annotations

import os
from typing import Optional

import httpx

import requests

# Base URLs for LLM providers can be overridden via environment variables.
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def _call_openai(prompt: str, model: str, api_key: str, base_url: Optional[str] = None) -> str:
    """Return a completion from the OpenAI compatible API."""
    try:
        import openai
    except ImportError as exc:
        raise ImportError(
            "openai package is required for OpenAI or LM Studio providers"
        ) from exc

    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


async def _call_openai_async(prompt: str, model: str, api_key: str, base_url: Optional[str] = None) -> str:
    """Async wrapper around the OpenAI compatible API."""
    try:
        import openai
    except ImportError as exc:  # pragma: no cover - dependency check
        raise ImportError(
            "openai package is required for OpenAI or LM Studio providers"
        ) from exc

    client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def _call_ollama(prompt: str, model: str, base_url: str) -> str:
    """Return a completion from an Ollama server."""
    url = f"{base_url.rstrip('/')}/api/generate"
    resp = requests.post(url, json={"model": model, "prompt": prompt})
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "").strip()


async def _call_ollama_async(prompt: str, model: str, base_url: str) -> str:
    """Async variant for Ollama server."""
    url = f"{base_url.rstrip('/')}/api/generate"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"model": model, "prompt": prompt})
        resp.raise_for_status()
        data = resp.json()
    return data.get("response", "").strip()


def generate_response(prompt: str, *, model: Optional[str] = None, provider: Optional[str] = None) -> str:
    """Send ``prompt`` to the configured LLM provider and return the response."""

    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        return _call_openai(prompt, model, api_key, OPENAI_BASE_URL)

    if provider == "lmstudio":
        api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
        return _call_openai(prompt, model, api_key, LMSTUDIO_BASE_URL)

    if provider == "ollama":
        return _call_ollama(prompt, model, OLLAMA_BASE_URL)

    raise ValueError(f"Unknown provider: {provider}")


async def async_generate_response(
    prompt: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """Asynchronously send ``prompt`` to the configured LLM provider."""

    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        return await _call_openai_async(prompt, model, api_key, OPENAI_BASE_URL)

    if provider == "lmstudio":
        api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
        return await _call_openai_async(prompt, model, api_key, LMSTUDIO_BASE_URL)

    if provider == "ollama":
        return await _call_ollama_async(prompt, model, OLLAMA_BASE_URL)

    raise ValueError(f"Unknown provider: {provider}")

