import os
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional


class AddressBar(ttk.Frame):
    """A custom address bar widget with navigation buttons."""

    def __init__(self, master, on_navigate: Callable[[str], None], **kwargs):
        """Initialize the address bar.

        Args:
            master: The parent widget
            on_navigate: Callback function when navigation is triggered
            **kwargs: Additional arguments to pass to the Frame
        """
        super().__init__(master, **{"padding": (2, 2, 2, 2), **kwargs})
        self.on_navigate = on_navigate
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create the address bar widgets."""
        # Address entry
        self.path_var = tk.StringVar()
        self.entry = ttk.Entry(
            self, textvariable=self.path_var, font=("Arial", 10), width=40
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        self.entry.bind("<Return>", self._on_enter_pressed)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        # Browse button
        self.browse_btn = ttk.Button(
            self, text="Browse...", command=self._on_browse_clicked, width=10
        )
        self.browse_btn.pack(side=tk.RIGHT)

    def set_path(self, path: str) -> None:
        """Set the current path in the address bar.

        Args:
            path: The path to display in the address bar
        """
        self.path_var.set(os.path.normpath(path))

    def get_path(self) -> str:
        """Get the current path from the address bar.

        Returns:
            The current path as a string
        """
        return os.path.normpath(self.path_var.get())

    def _on_enter_pressed(self, event=None) -> None:
        """Handle Enter key press in the address bar."""
        self._navigate_to(self.get_path())

    def _on_focus_out(self, event=None) -> None:
        """Handle focus out event on the address bar."""
        self.set_path(self.get_path())

    def _on_browse_clicked(self) -> None:
        """Handle browse button click."""
        initial_dir = self.get_path() or os.path.expanduser("~")
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")

        folder = filedialog.askdirectory(title="Select Folder", initialdir=initial_dir)
        if folder:
            self._navigate_to(folder)

    def _navigate_to(self, path: str) -> None:
        """Navigate to the specified path.

        Args:
            path: The absolute path to navigate to
        """
        if os.path.isdir(path):
            self.set_path(path)
            if self.on_navigate:
                self.on_navigate(path)
