import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Tuple

from photo_condenser.ui.views.base_view import BaseView
from photo_condenser.ui.components.image_viewer import ImageViewer


class PortraitView(BaseView):
    """View for comparing portrait-oriented images side by side."""

    def _setup_ui(self) -> None:
        """Set up the portrait view UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left image viewer
        self.viewer1 = ImageViewer(self, title="Left Image")
        self.viewer1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        # Right image viewer
        self.viewer2 = ImageViewer(self, title="Right Image")
        self.viewer2.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)

    def load_images(self, left_path: str, right_path: str) -> None:
        """Load images into the viewers.

        Args:
            left_path: Path to the left image
            right_path: Path to the right image
        """
        self.viewer1.load_image(left_path)
        self.viewer2.load_image(right_path)

    def highlight_selection(self, select: int) -> None:
        """Highlight the selected image.

        Args:
            select: 0 None, 1 Left/Top, 2 Right/Bottom
        """
        if select == 0:
            self.viewer1.highlight(False)
            self.viewer2.highlight(False)
        elif select == 1:
            self.viewer1.highlight(True)
            self.viewer2.highlight(False)
        elif select == 2:
            self.viewer1.highlight(False)
            self.viewer2.highlight(True)
        else:
            raise NotImplementedError

    def cleanup(self) -> None:
        """Clean up resources."""
        self.viewer1.cleanup()
        self.viewer2.cleanup()
