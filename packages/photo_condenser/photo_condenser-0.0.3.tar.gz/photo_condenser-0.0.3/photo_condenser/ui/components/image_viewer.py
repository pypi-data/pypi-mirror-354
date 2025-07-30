"""
Image viewer component for displaying and managing images in the UI.
"""

from __future__ import annotations
from typing import Optional, Tuple, Callable
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path


class ImageViewer(tk.Frame):
    """A widget for displaying and managing a single image with zoom and pan capabilities."""

    def __init__(
        self,
        master: tk.Misc,
        title: str = "Image",
        width: int = 400,
        height: int = 400,
        **kwargs,
    ):
        """Initialize the image viewer.

        Args:
            master: The parent widget
            title: The title to display above the image
            width: Default width of the viewer
            height: Default height of the viewer
            **kwargs: Additional arguments to pass to the Frame
        """
        super().__init__(master, **kwargs)

        self.image_path: Optional[str] = None
        self.image: Optional[Image.Image] = None
        self.photo_image: Optional[ImageTk.PhotoImage] = None
        self.zoom_level: float = 1.0
        self.pan_start_x: int = 0
        self.pan_start_y: int = 0
        self.highlighted: bool = False
        self.highlight_color: str = "#4CAF50"  # Green color for highlight
        self.normal_border_color: str = "#cccccc"  # Default border color

        # Create UI
        self._create_widgets(title, width, height)

        # Bind events
        self.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Configure>", self._on_resize)

    def _create_widgets(self, title: str, width: int, height: int) -> None:
        """Create the UI components."""
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Title label
        self.title_label = tk.Label(self, text=title, font=("Arial", 10, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        # Canvas for the image with scrollbars
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")

        # Configure grid weights for canvas frame
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        # Canvas for the image with initial border
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="white",
            width=width,
            height=height,
            highlightthickness=3,  # Thicker border for better visibility
            highlightbackground=self.normal_border_color,
            highlightcolor=self.normal_border_color,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.h_scrollbar = ttk.Scrollbar(
            self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )

        # Configure canvas
        self.canvas.config(
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
        )

        # Info label for image details
        self.info_var = tk.StringVar()
        self.info_label = tk.Label(
            self,
            textvariable=self.info_var,
            font=("Arial", 8),
            fg="#666666",
        )
        self.info_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        # Bind events
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<ButtonPress-1>", self._on_pan_start)
        self.canvas.bind("<B1-Motion>", self._on_pan_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_pan_end)

    def load_image(self, image_path: str) -> bool:
        """Load an image from the specified path.

        Args:
            image_path: Path to the image file

        Returns:
            bool: True if the image was loaded successfully, False otherwise
        """
        # try:
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.zoom_level = 1.0
        self._update_display()
        self._update_info()
        return True
        # except Exception as e:
        #     print(f"Error loading image {image_path}: {e}")
        #     self.clear()
        #     return False

    def clear(self) -> None:
        """Clear the current image."""
        self.canvas.delete("all")
        self.image_path = None
        self.image = None
        self.photo_image = None
        self.info_var.set("")

    def _update_display(self) -> None:
        """Update the displayed image with the current zoom and pan settings."""
        if self.image is None:
            return

        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # If canvas is too small, use default size
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 400
            canvas_height = 400

        # Calculate aspect ratio of image and canvas
        img_ratio = self.image.width / self.image.height
        canvas_ratio = canvas_width / canvas_height

        # Calculate size to fit image in canvas while maintaining aspect ratio
        if img_ratio > canvas_ratio:
            # Image is wider than canvas relative to height
            display_width = canvas_width
            display_height = int(display_width / img_ratio)
        else:
            # Image is taller than canvas relative to width
            display_height = canvas_height
            display_width = int(display_height * img_ratio)

        # Apply zoom level
        display_width = int(display_width * self.zoom_level)
        display_height = int(display_height * self.zoom_level)

        # Ensure minimum size
        display_width = max(10, display_width)
        display_height = max(10, display_height)

        # Resize image
        resized = self.image.resize(
            (display_width, display_height), Image.Resampling.LANCZOS
        )

        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized)

        # Clear canvas and display image
        self.canvas.delete("all")

        # Center the image on the canvas
        x = canvas_width // 2
        y = canvas_height // 2

        self.canvas.create_image(x, y, image=self.photo_image, anchor=tk.CENTER)

        # Update scroll region to include the entire image
        self.canvas.config(
            scrollregion=(
                -canvas_width // 2,
                -canvas_height // 2,
                canvas_width * 1.5,
                canvas_height * 1.5,
            )
        )

        # Show scrollbars if needed
        self._update_scrollbars(
            display_width, display_height, canvas_width, canvas_height
        )

    def _update_scrollbars(
        self, img_width: int, img_height: int, canvas_width: int, canvas_height: int
    ) -> None:
        """Show/hide scrollbars based on image and canvas sizes."""
        need_h_scroll = img_width > canvas_width
        need_v_scroll = img_height > canvas_height

        # Configure scrollbars
        self.h_scrollbar.grid_forget()
        self.v_scrollbar.grid_forget()

        if need_h_scroll:
            self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        if need_v_scroll:
            self.v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Update canvas scroll region
        self.canvas.config(
            xscrollcommand=self.h_scrollbar.set if need_h_scroll else None,
            yscrollcommand=self.v_scrollbar.set if need_v_scroll else None,
        )

        # Update scrollbar commands
        if need_h_scroll:
            self.h_scrollbar.config(command=self.canvas.xview)
        if need_v_scroll:
            self.v_scrollbar.config(command=self.canvas.yview)

        # Update scroll region to include the entire image
        self.canvas.config(
            scrollregion=(
                0,
                0,
                max(canvas_width, img_width),
                max(canvas_height, img_height),
            )
        )

    def _update_info(self) -> None:
        """Update the image information display."""
        if self.image is None or self.image_path is None:
            return

        # Get file size in KB
        file_size = Path(self.image_path).stat().st_size / 1024

        # Get image dimensions
        width, height = self.image.size

        # Update info label
        self.info_var.set(
            f"{width}×{height} | {file_size:.1f} KB | {Path(self.image_path).name}"
        )

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """Handle mouse wheel events for zooming."""
        if event.delta > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level *= 0.9

        # Limit zoom levels
        self.zoom_level = max(0.1, min(10.0, self.zoom_level))

        self._update_display()

    def _on_pan_start(self, event: tk.Event) -> None:
        """Start panning the image."""
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _on_pan_move(self, event: tk.Event) -> None:
        """Pan the image."""
        if not hasattr(self, "pan_start_x"):
            return

        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y

        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")

        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _on_pan_end(self, event: tk.Event) -> None:
        """End panning the image."""
        if hasattr(self, "pan_start_x"):
            del self.pan_start_x
            del self.pan_start_y

    def _on_resize(self, event=None) -> None:
        """Handle window resize events."""
        if self.image is not None:
            self._update_display()

    def highlight(self, enable: bool = True) -> None:
        """Highlight or unhighlight the image viewer.

        Args:
            enable: If True, highlight the viewer; if False, remove highlight
        """
        self.highlighted = enable
        color = self.highlight_color if enable else self.normal_border_color
        self.canvas.config(highlightbackground=color, highlightcolor=color)
        # Force update to show the highlight immediately
        self.update_idletasks()


if __name__ == "__main__":
    # Simple test
    root = tk.Tk()
    root.geometry("900x600")

    viewer = ImageViewer(root, title="Test Image")
    viewer.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Load a test image
    import sys

    if len(sys.argv) > 1:
        viewer.load_image(sys.argv[1])

    root.mainloop()
