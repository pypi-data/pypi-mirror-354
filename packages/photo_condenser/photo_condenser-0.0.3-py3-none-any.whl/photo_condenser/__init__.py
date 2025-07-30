"""
Photo Deduplicator - A tool to find and remove duplicate or similar images.
"""

__version__ = '0.0.3'

# Import main components
from photo_condenser.image_comparator import ImageComparator, ImagePair
from photo_condenser.ui.main_window import MainWindow

__all__ = [
    "ImageComparator",
    "ImagePair",
    "MainWindow",
    "__version__",
]
