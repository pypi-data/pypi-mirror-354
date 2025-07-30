#!/usr/bin/env python3
"""
Photo Deduplicator - A tool to find and remove duplicate or similar images.
"""

from photo_condenser.ui.main_window import MainWindow
import os


def main():
    """Launch the Photo Deduplicator application."""
    # Set a modern theme if available
    main_window = MainWindow()
    try:
        import ttkthemes

        style = ttkthemes.ThemedStyle(main_window)
        style.set_theme("arc")  # or "breeze", "clearlooks", etc.
    except ImportError:
        pass
    # Set the default folder to ~/Camera if it exists
    default_folder = os.path.expanduser("~/Camera")
    if os.path.isdir(default_folder):
        main_window.after(
            100, lambda: main_window.address_bar._navigate_to(default_folder)
        )

    # Run the application
    main_window.mainloop()

    return 0


if __name__ == "__main__":
    main()
