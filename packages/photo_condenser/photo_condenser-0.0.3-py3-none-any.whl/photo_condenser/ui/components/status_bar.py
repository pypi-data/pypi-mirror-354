"""
Status bar component for displaying application status.
"""

import tkinter as tk
from typing import Optional


class StatusBar(tk.Frame):
    """A status bar widget that displays messages at the bottom of the window."""

    def __init__(self, master: tk.Misc, **kwargs):
        """Initialize the status bar.

        Args:
            master: The parent widget
            **kwargs: Additional arguments to pass to the Frame constructor
        """
        super().__init__(master, **{"bd": 1, "relief": tk.SUNKEN, **kwargs})

        self._status_var = tk.StringVar()
        self._status_var.set("Ready")

        self._label = tk.Label(self, textvariable=self._status_var, anchor=tk.W)
        self._label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def set_text(self, text: str) -> None:
        """Set the status bar text.

        Args:
            text: The text to display in the status bar
        """
        self._status_var.set(text)

    def get_text(self) -> str:
        """Get the current status bar text.

        Returns:
            The current status bar text
        """
        return self._status_var.get()

    def clear(self) -> None:
        """Clear the status bar text."""
        self._status_var.set("")


if __name__ == "__main__":
    # Simple test
    import time
    from tkinter import ttk

    root = tk.Tk()
    root.geometry("800x100")

    status_bar = StatusBar(root)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_progress():
        for i in range(101):
            status_bar.set_text(f"Processing item {i}/100")
            root.update()
            time.sleep(0.05)
        status_bar.set_text("Done!")

    btn = tk.Button(root, text="Start Progress", command=update_progress)
    btn.pack(pady=20)

    root.mainloop()
