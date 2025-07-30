import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Tuple

from photo_condenser.ui.views.base_view import BaseView
from photo_condenser.ui.components.image_viewer import ImageViewer


class LandscapeView(BaseView):
    """View for comparing landscape-oriented images in a vertical split."""

    def _setup_ui(self) -> None:
        """Set up the landscape view UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top image viewer
        self.viewer1 = ImageViewer(self, title="Top Image")
        self.viewer1.grid(row=0, column=0, sticky="nsew", padx=5, pady=(0, 5))

        # Bottom image viewer
        self.viewer2 = ImageViewer(self, title="Bottom Image")
        self.viewer2.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5, 0))

    def load_images(self, top_path: str, bottom_path: str) -> None:
        """Load images into the viewers.

        Args:
            top_path: Path to the top image
            bottom_path: Path to the bottom image
        """
        self.viewer1.load_image(top_path)
        self.viewer2.load_image(bottom_path)

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
