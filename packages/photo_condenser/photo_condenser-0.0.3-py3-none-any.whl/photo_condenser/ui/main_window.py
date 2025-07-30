import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

from photo_condenser.ui.components.status_bar import StatusBar
from photo_condenser.ui.components.address_bar import AddressBar
from photo_condenser.ui.views.loading_view import LoadingView
from photo_condenser.ui.views.portrait_view import PortraitView
from photo_condenser.ui.views.landscape_view import LandscapeView
from photo_condenser.app_controller import AppController


class MainWindow(tk.Tk):
    """Main application window for the Photo Deduplicator."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        self.title("Photo Deduplicator")
        self.geometry("1200x800")
        self.minsize(800, 600)

        # Initialize controller
        self.controller = AppController()

        # Views
        self.views = {}
        self.current_view = None

        self.cancel_del_id = None

        # Setup UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create toolbar
        self._create_toolbar()

        # Create views container
        self.views_container = ttk.Frame(self)
        self.views_container.grid(row=1, column=0, sticky="nsew")
        self.views_container.grid_rowconfigure(0, weight=1)
        self.views_container.grid_columnconfigure(0, weight=1)

        # Create status bar
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=2, column=0, sticky="ew")

        # Initialize views
        self._init_views()

        # Bind keyboard shortcuts
        # Common navigation bindings
        self.bind("<Prior>", lambda e: self._on_prev_pair())  # Page Up
        self.bind("<Next>", lambda e: self._on_next_pair())  # Page Down
        self.bind("<space>", lambda e: self._on_next_pair())
        self.bind("<Escape>", lambda e: self._cancel_selection())
        self._update_ui_for_orientation(False)

    def _init_views(self) -> None:
        """Initialize all views."""
        # Loading view
        self.views["loading"] = LoadingView(self.views_container)
        self.views["loading"].set_status_callback(self._update_status)

        # Portrait view (side by side)
        self.views["portrait"] = PortraitView(self.views_container)

        # Landscape view (top/bottom)
        self.views["landscape"] = LandscapeView(self.views_container)

        # Show loading view initially
        self.show_view("loading")

    def show_view(self, view_name: str) -> None:
        """Show the specified view.

        Args:
            view_name: Name of the view to show ("loading", "portrait", "landscape")
        """
        if self.current_view:
            self.current_view.grid_remove()

        self.current_view = self.views[view_name]
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.update()

    def _create_toolbar(self) -> None:
        """Create the toolbar with navigation buttons."""
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Navigation buttons
        self.prev_btn = ttk.Button(
            toolbar, text="Previous (←)", command=self._on_prev_pair
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.next_btn = ttk.Button(
            toolbar, text="Next (→)", command=self._on_next_pair
        )
        self.next_btn.pack(side=tk.LEFT, padx=2)

        # Keep/Delete buttons
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, padx=10, fill=tk.Y
        )

        self.keep_left_btn = ttk.Button(
            toolbar, text="Keep Left (1)", command=lambda: self._on_keep_image(True)
        )
        self.keep_left_btn.pack(side=tk.LEFT, padx=2)

        self.keep_right_btn = ttk.Button(
            toolbar,
            text="Keep Right (2)",
            command=lambda: self._on_keep_image(False),
        )
        self.keep_right_btn.pack(side=tk.LEFT, padx=2)

        # Address bar
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(
            side=tk.LEFT, padx=10, fill=tk.Y
        )
        self.address_bar = AddressBar(toolbar, on_navigate=self._on_folder_selected)
        self.address_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def _update_ui_for_orientation(self, is_landscape: bool) -> None:
        """Update the UI elements and keybindings based on image orientation.

        Args:
            is_landscape: Whether the images are in landscape orientation
        """
        # Clear existing bindings
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Up>")
        self.unbind("<Down>")

        if is_landscape:
            # Landscape orientation - use Up/Down for selection
            self.keep_left_btn.config(text="Keep Top (↑)")
            self.keep_right_btn.config(text="Keep Bottom (↓)")

            # Bind Up/Down for selection in landscape mode
            self.bind("<Up>", lambda e: self._on_keep_image(True))
            self.bind("<Down>", lambda e: self._on_keep_image(False))

        else:
            # Portrait orientation - use Left/Right for selection
            self.keep_left_btn.config(text="Keep Left (←)")
            self.keep_right_btn.config(text="Keep Right (→)")

            # Bind Left/Right for selection in portrait mode
            self.bind("<Left>", lambda e: self._on_keep_image(True))
            self.bind("<Right>", lambda e: self._on_keep_image(False))

    def _update_status(self, message: str) -> None:
        """Update the status bar."""
        self.status_bar.set_text(message)
        self.update()

    def _on_folder_selected(self, folder_path: str) -> None:
        """Handle folder selection."""
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", f"Folder not found: {folder_path}")
            return

        # Show loading view
        self.show_view("loading")
        self._update_status("Processing folder...")

        # Process folder in background
        self.after(100, lambda: self._process_folder_async(folder_path))

    def _process_folder_async(self, folder_path: str) -> None:
        """Process folder asynchronously."""
        # try:
        if self.controller.process_folder(folder_path):
            self._show_current_pair()
        else:
            self._update_status("No similar images found.")
        # except Exception as e:
        #     messagebox.showerror("Error", f"Failed to process folder: {str(e)}")
        #     self._update_status("Ready")

    def _show_current_pair(self) -> None:
        """Show the current image pair in the appropriate view."""
        result = self.controller.get_current_images()
        if not result:
            return

        img1, img2, similarity = result

        # Determine orientation based on actual image dimensions
        both_landscape = img1.is_landscape() and img2.is_landscape()

        if both_landscape:
            self.show_view("landscape")
            self.views["landscape"].load_images(img1.path, img2.path)
        else:
            self.show_view("portrait")
            self.views["portrait"].load_images(img1.path, img2.path)

        # Update UI for the current orientation
        self._update_ui_for_orientation(both_landscape)

        # Update status
        total_pairs = len(self.controller.similar_pairs)
        current_pair = self.controller.current_pair_index + 1
        self._update_status(
            f"Pair {current_pair} of {total_pairs} | Similarity: {similarity:.1f}%"
        )

        # Update UI state
        self._update_ui_state()

    def _on_keep_image(self, keep_first: bool) -> None:
        """Handle keeping one image and deleting the other."""
        if not self.controller.similar_pairs:
            return

        # Show selection feedback
        current_view = (
            self.views["portrait"]
            if isinstance(self.current_view, PortraitView)
            else self.views["landscape"]
        )
        current_view.highlight_selection(1 if keep_first else 2)

        # Schedule the actual deletion after a delay
        self.cancel_del_id = self.after(
            1000, lambda: self._process_deletion(keep_first)
        )

    def _process_deletion(self, keep_first: bool) -> None:
        """Process the image deletion after selection."""
        if self.controller.trash_image(keep_first):
            self._on_next_pair()
        else:
            messagebox.showerror("Error", "Failed to process images")
        self.current_view.highlight_selection(0)

    def _cancel_selection(self) -> None:
        """Cancel the current selection."""

        if self.cancel_del_id is not None:
            self.after_cancel(self.cancel_del_id)
        if isinstance(self.current_view, (PortraitView, LandscapeView)):
            self.current_view.highlight_selection(0)

    def _on_prev_pair(self) -> None:
        """Show the previous image pair."""
        self.current_view.highlight_selection(0)

        if self.controller.previous_pair():
            self._show_current_pair()

    def _on_next_pair(self) -> None:
        """Show the next image pair."""
        self.current_view.highlight_selection(0)

        if self.controller.next_pair():
            self._show_current_pair()
        else:
            self._update_status("No more image pairs to review.")

    def _update_ui_state(self) -> None:
        """Update the UI state based on current state."""
        has_pairs = bool(self.controller.similar_pairs)
        can_go_prev = has_pairs and self.controller.has_previous_pair()
        can_go_next = has_pairs and self.controller.has_next_pair()

        self.prev_btn.config(state=tk.NORMAL if can_go_prev else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if can_go_next else tk.DISABLED)
        self.keep_left_btn.config(state=tk.NORMAL if has_pairs else tk.DISABLED)
        self.keep_right_btn.config(state=tk.NORMAL if has_pairs else tk.DISABLED)

    def cleanup(self) -> None:
        """Clean up resources."""
        for view in self.views.values():
            view.cleanup()
        if hasattr(self.controller, "cleanup"):
            self.controller.cleanup()
