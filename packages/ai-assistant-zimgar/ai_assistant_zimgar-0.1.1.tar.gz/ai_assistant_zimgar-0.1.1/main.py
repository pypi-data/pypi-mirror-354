"""Simple CLI entrypoint."""

import argparse
from pathlib import Path
import sys
import logging

from logging_utils import setup_logging

from llm_interface import generate_response
from screen_capture import capture_screen
from desktop_control import type_text
from n8n_interface import run_workflow
from voice_input import listen_and_transcribe
from feedback_memory import record_feedback, get_mood


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Desktop Assistant")
    parser.add_argument("prompt", nargs="?", help="Text prompt for the assistant")
    parser.add_argument(
        "--screenshot", action="store_true", help="Capture a screenshot before sending the prompt"
    )
    parser.add_argument(
        "--screenshot-path",
        metavar="PATH",
        help="Path to save the screenshot (implies --screenshot if set)",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the HTTP server instead of running the CLI",
    )
    parser.add_argument(
        "--workflow",
        metavar="WORKFLOW_ID",
        help="Trigger this n8n workflow after generating the response",
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Capture voice input instead of typing a prompt",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Keep prompting until the user indicates success",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama", "lmstudio"],
        help="LLM provider to use (overrides LLM_PROVIDER env var)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase log verbosity (can be repeated)",
    )
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    logger.debug("Arguments: %s", args)

    if args.serve:
        import server

        logger.info("Starting server mode")
        server.main()
        return

    if args.screenshot or args.screenshot_path:
        screenshot_path = Path(args.screenshot_path or "screenshot.png")
        try:
            logger.info("Capturing screenshot to %s", screenshot_path)
            capture_screen(str(screenshot_path))
        except Exception as exc:
            logger.error("Error capturing screen", exc_info=exc)
            print(f"Error capturing screen: {exc}", file=sys.stderr)
            sys.exit(1)
        logger.info("Screenshot saved to %s", screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    if args.voice:
        try:
            logger.info("Capturing voice input")
            args.prompt = listen_and_transcribe()
        except Exception as exc:
            logger.error("Error capturing voice input", exc_info=exc)
            print(f"Error capturing voice input: {exc}", file=sys.stderr)
            sys.exit(1)
        logger.info("Transcribed prompt: %s", args.prompt)
        print(f"Transcribed prompt: {args.prompt}")
    elif not args.prompt:
        args.prompt = input("Enter prompt: ")
        logger.debug("User prompt: %s", args.prompt)

    while True:
        try:
            logger.info("Sending prompt to LLM")
            response = generate_response(args.prompt, provider=args.provider)
        except Exception as exc:
            logger.error("Error calling language model", exc_info=exc)
            print(f"Error calling language model: {exc}", file=sys.stderr)
            sys.exit(1)
        logger.info("LLM response: %s", response)
        print(response)
        if args.workflow:
            logger.info("Running workflow %s", args.workflow)
            result = run_workflow(args.workflow, {"prompt": args.prompt, "response": response})
            logger.info("Workflow result: %s", result)
            print(result)
        feedback = input("Was this correct? (y/n): ").strip().lower()
        record_feedback(feedback == "y")
        logger.debug("Feedback recorded: %s", feedback)
        print(f"Assistant mood: {get_mood()}")
        if feedback == "y" or not args.loop:
            logger.info("Exiting prompt loop")
            break
        args.prompt = input("Enter new prompt: ")
        logger.debug("Next prompt: %s", args.prompt)
    # Example of using the desktop control module
    # type_text(response)


if __name__ == "__main__":
    main()
