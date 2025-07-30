"""Utilities for triggering n8n workflows."""


from __future__ import annotations

import os

from typing import Optional

import requests

N8N_BASE_URL = os.getenv("N8N_BASE_URL", "http://localhost:5678")
N8N_API_KEY = os.getenv("N8N_API_KEY")

__all__ = ["run_workflow"]


def run_workflow(workflow_id: str, payload: Optional[dict] = None) -> dict:
    """Run an n8n workflow and return the JSON response.

    Parameters
    ----------
    workflow_id: str
        Identifier of the workflow webhook to trigger.
    payload: dict, optional
        Data to include in the POST request body.
    """
    if not N8N_BASE_URL:
        raise ValueError("N8N_BASE_URL environment variable not set")

    url = f"{N8N_BASE_URL.rstrip('/')}/{workflow_id.lstrip('/')}"
    headers = {}
    if N8N_API_KEY:
        headers["X-N8N-API-KEY"] = N8N_API_KEY

    try:
        resp = requests.post(url, json=payload or {}, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to run workflow {workflow_id}: {exc}") from exc

    try:
        return resp.json()
    except ValueError:
        return {"response": resp.text}
