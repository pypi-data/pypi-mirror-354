# AI Assistant

This project automates desktop tasks with help from a language model. It can type text, control the mouse and keyboard, and capture screenshots or video. A simple CLI accepts a natural language prompt, queries an LLM provider, and optionally triggers an n8n workflow.

## Features

- Basic keyboard and mouse automation
- Screenshot and optional video capture
- Interface for querying different LLM providers
- Voice input via microphone (optional)
- Tracks success and failure feedback and shows the assistant's mood

The `capture_video` function depends on `opencv-python` and `mss`. Screenshots only require `pyautogui`.

## Installation

Install the package with pip:

```bash
pip install ai-assistant
```

For voice input support you also need the `pyaudio` backend. Installing
`pyaudio` often requires system libraries such as `portaudio` to be present.

## System Requirements

Some of the Python packages rely on additional operating system
libraries. Install the following tools for your platform before using
`pyaudio`, `pyautogui` or video capture features.

### Linux (Debian/Ubuntu)

```bash
sudo apt-get install portaudio19-dev scrot xclip python3-tk ffmpeg
```

### macOS

```bash
brew install portaudio ffmpeg
```
The built in screenshot utility works with `pyautogui` so no extra
packages are required.

### Windows

Building `pyaudio` from source is difficult. Install it via
`pipwin` and add `ffmpeg` for video capture:

```bash
pip install pipwin
pipwin install pyaudio
choco install ffmpeg  # or download from https://ffmpeg.org/
```

## Usage

Run the command line interface:

```bash
ai-assistant "your prompt" --screenshot --workflow WORKFLOW_ID
```
Specify a custom image file with `--screenshot-path`:

```bash
ai-assistant "your prompt" --screenshot-path /tmp/shot.png
```
Add `--voice` to capture a spoken prompt via your microphone:

```bash
ai-assistant --voice
```
Use `--loop` to keep prompting until you confirm the response is correct.
You can also specify the LLM backend with `--provider` (for example `--provider lmstudio`).
After each iteration you are asked for feedback and the assistant reports its
current mood based on that history.
The feedback is saved to `feedback.json` by default; set the
`ASSISTANT_FEEDBACK_FILE` environment variable to change this path.

To start the HTTP server instead of the CLI use:

```bash
ai-assistant --serve
```

For a graphical interface run:

```bash
ai-assistant-gui
```
This opens a small Tkinter window where you can type prompts and see the
responses without using a browser.

You can also run the server module directly:

```bash
python server.py
```

Run it in the background with `python server.py &` or create a systemd service
for long-running deployments.

The API exposes a single asynchronous endpoint:

- `POST /prompt` – JSON body `{"prompt": "your text"}` returns `{"response": "..."}`.
  The server awaits `async_generate_response` from `llm_interface`.

If no prompt is provided, the script will ask for one. Use `--screenshot` to capture the screen before sending the prompt and `--screenshot-path` to choose where the image is saved. Add `--workflow` to trigger an n8n workflow with the prompt and LLM response.

## Module Overview

- `llm_interface.py` – `generate_response(prompt)` and `async_generate_response(prompt)` communicate with the configured LLM provider.
- `screen_capture.py` – `capture_screen(path)` and `capture_video(duration, path, fps)` for screenshots and recordings.
- `desktop_control.py` – helpers such as `move_mouse`, `click` and `type_text` for automation.
- `n8n_interface.py` – `run_workflow(workflow_id, payload)` to trigger n8n workflows.
- `main.py` – command line entry point combining these utilities.

- `voice_input.py` – `listen_and_transcribe()` records speech and returns text.

- `server.py` – lightweight FastAPI server exposing a `/prompt` endpoint that awaits `async_generate_response`.
- `gui.py` – Tkinter interface for entering prompts and viewing responses.


## Environment Variables

Set these variables to configure the assistant. You can override `LLM_PROVIDER`
via the `--provider` CLI flag.

- `LLM_PROVIDER` – `openai` (default), `ollama` or `lmstudio`.
  The `lmstudio` option uses the OpenAI-compatible API and therefore requires
  the `openai` Python package but **not** an OpenAI account.
- `LLM_MODEL` – model name for the provider (default `gpt-3.5-turbo`).
- `OPENAI_API_KEY` – API key for OpenAI.
- `OPENAI_BASE_URL` – override the OpenAI API base URL.
- `LMSTUDIO_API_KEY` – API key for LM Studio (default `lm-studio`).
- `LMSTUDIO_BASE_URL` – base URL of the LM Studio server (default `http://localhost:1234/v1`).
- `OLLAMA_BASE_URL` – URL of the Ollama server (default `http://localhost:11434`).
- `N8N_BASE_URL` – base URL of your n8n instance (default `http://localhost:5678`).
- `N8N_API_KEY` – API key for authenticating requests to n8n (optional).
- `ASSISTANT_FEEDBACK_FILE` – where success/failure feedback is saved
  (default `feedback.json`).

These settings are read by `llm_interface.py` and `n8n_interface.py` at runtime.

## Running Tests

Unit tests live in the `tests` directory and can be run with `pytest`.
They rely on dependencies from `requirements.txt` such as `requests`,
`fastapi` and `httpx`:

```bash
pip install pytest
pytest
```

### Publishing to TestPyPI

To build and upload a release to [TestPyPI](https://test.pypi.org/):

```bash
pip install build twine
python -m build
twine upload --repository testpypi dist/*
```

Install the package from TestPyPI with:

```bash
pip install --index-url https://test.pypi.org/simple/ ai-assistant
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
