"""HTTP server exposing the LLM prompt API."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
import logging
from logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from llm_interface import async_generate_response

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/prompt")
async def post_prompt(data: PromptRequest) -> dict:
    """Return the LLM response for the provided prompt."""
    logger.info("Received prompt")
    try:
        response = await async_generate_response(data.prompt)
    except Exception as exc:  # pragma: no cover - errors handled by FastAPI
        logger.error("LLM error", exc_info=exc)
        raise HTTPException(status_code=500, detail=str(exc))
    logger.info("Sending response")
    return {"response": response}

# Serve files from the local web directory after defining API routes
app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "web", html=True),
    name="web",
)


def main() -> None:
    """Run the FastAPI server using uvicorn."""
    import uvicorn
    logger.info("Starting HTTP server")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
