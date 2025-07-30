import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional, Callable


class BaseView(tk.Frame, ABC):
    """Base class for all application views."""

    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **{"bg": "white", **kwargs})
        self._status_callback: Optional[Callable[[str], None]] = None
        self._setup_ui()

    @abstractmethod
    def _setup_ui(self) -> None:
        """Set up the user interface for this view."""
        pass

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Set a callback for status updates."""
        self._status_callback = callback

    def update_status(self, message: str) -> None:
        """Update status using the callback if available."""
        if self._status_callback:
            self._status_callback(message)

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by this view."""
        pass
