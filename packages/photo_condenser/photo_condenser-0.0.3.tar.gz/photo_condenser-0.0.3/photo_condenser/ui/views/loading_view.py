import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import os

from photo_condenser.ui.views.base_view import BaseView


class LoadingView(BaseView):
    """View for showing loading progress."""

    def _setup_ui(self) -> None:
        """Set up the loading view UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center frame
        center_frame = ttk.Frame(self, style="Card.TFrame")
        center_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)

        # Loading label
        self.status_label = ttk.Label(
            center_frame, text="Processing images...", font=("Arial", 12)
        )
        self.status_label.pack(padx=40, pady=(20, 10), expand=True)

        # Current file label
        self.file_label = ttk.Label(
            center_frame,
            text="",
            font=("Arial", 10),
            wraplength=400,
            justify="center",
        )
        self.file_label.pack(padx=40, pady=(0, 20), expand=True)

        # Progress bar
        self.progress = ttk.Progressbar(
            center_frame, orient="horizontal", length=300, mode="determinate"
        )
        self.progress.pack(padx=20, pady=(0, 20), fill=tk.X, expand=True)

    def set_progress(self, value: int, maximum: int = 100) -> None:
        """Update the progress bar.

        Args:
            value: Current progress value
            maximum: Maximum progress value (default: 100)
        """
        self.progress["maximum"] = maximum
        self.progress["value"] = value
        self.update()

    def set_status(self, message: str) -> None:
        """Update the status message.

        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
        self.update()

    def set_current_file(self, filename: str) -> None:
        """Update the current file being processed.

        Args:
            filename: Name of the current file being processed
        """
        short_name = os.path.basename(filename)
        self.file_label.config(text=f"Processing: {short_name}")
        self.update()

    def cleanup(self) -> None:
        """Clean up resources."""
        pass
