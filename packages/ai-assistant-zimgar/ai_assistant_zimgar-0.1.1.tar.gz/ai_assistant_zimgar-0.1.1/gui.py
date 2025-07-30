"""Simple Tkinter-based GUI for sending prompts to the language model."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import scrolledtext
import logging

from logging_utils import setup_logging
from llm_interface import generate_response

setup_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the GUI application."""

    root = tk.Tk()
    root.title("AI Assistant")

    prompt_var = tk.StringVar()

    entry = tk.Entry(root, textvariable=prompt_var)
    entry.pack(fill=tk.X, padx=5, pady=5)
    entry.focus()

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
    text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def send() -> None:
        prompt = prompt_var.get().strip()
        if not prompt:
            return
        text_area.insert(tk.END, f"> {prompt}\n")
        text_area.see(tk.END)
        prompt_var.set("")

        def worker() -> None:
            try:
                response = generate_response(prompt)
            except Exception as exc:  # pragma: no cover - GUI feedback
                logger.error("LLM error", exc_info=exc)
                response = f"Error: {exc}"
            text_area.insert(tk.END, response + "\n")
            text_area.see(tk.END)

        threading.Thread(target=worker, daemon=True).start()

    button = tk.Button(root, text="Send", command=send)
    button.pack(padx=5, pady=(0, 5))

    entry.bind("<Return>", lambda event: (send(), "break"))

    root.mainloop()


if __name__ == "__main__":
    main()
