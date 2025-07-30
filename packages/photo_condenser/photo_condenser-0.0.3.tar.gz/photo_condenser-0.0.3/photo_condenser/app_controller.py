# app_controller.py
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import os
import shutil
from dataclasses import dataclass

from photo_condenser.image_data import ImageData
from photo_condenser.image_comparator import ImageComparator


@dataclass
class ImagePair:
    """Represents a pair of similar images in the UI."""

    path1: str
    path2: str
    similarity: float
    selected: Optional[bool] = None
    image_data1: Optional[ImageData] = None
    image_data2: Optional[ImageData] = None

    def __getitem__(self, key):
        if key == 0:
            return self.image_data1
        elif key == 1:
            return self.image_data2

        raise IndexError

    def __iter__(self):
        return iter([self.image_data1, self.image_data2])

    def __contains__(self, item):
        return item in [self.image_data1, self.image_data2]


class AppController:
    """Handles the core application logic separate from the UI."""

    def __init__(self, image_dir: Optional[str] = None):
        self.image_dir = image_dir
        self.trash_dir = os.path.join(image_dir, "trash") if image_dir else None
        self.comparator = ImageComparator(threshold=0.85)
        self.similar_pairs: List[ImagePair] = []
        self.current_pair_index: int = -1
        self._status_callback: Optional[Callable[[str], None]] = None

        if image_dir:
            self._setup_directories()

    def set_image_dir(self, directory: str) -> None:
        """Set the image directory and initialize required directories."""
        self.image_dir = directory
        if self.image_dir:
            os.makedirs(self.image_dir, exist_ok=True)
            self.trash_dir = os.path.join(self.image_dir, "trash")
            os.makedirs(self.trash_dir, exist_ok=True)

            self.comparator.set_images(self.image_dir)

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Set a callback for status updates."""
        self._status_callback = callback

    def update_status(self, message: str) -> None:
        """Update status using the callback if available."""
        if self._status_callback:
            self._status_callback(message)

    def find_similar_pairs(self) -> List[ImagePair]:
        """Find similar image pairs using the image comparator."""
        if not self.comparator:
            raise RuntimeError("Image comparator not initialized")

        self.similar_pairs = []
        similar_pairs = self.comparator.find_similar_pairs()

        for pair in similar_pairs:
            self.similar_pairs.append(
                ImagePair(
                    path1=pair.image1.path,
                    path2=pair.image2.path,
                    similarity=pair.similarity,
                    image_data1=pair.image1,
                    image_data2=pair.image2,
                )
            )

        return self.similar_pairs

    def get_current_pair(self) -> Optional[ImagePair]:
        """Get the current image pair."""
        if 0 <= self.current_pair_index < len(self.similar_pairs):
            return self.similar_pairs[self.current_pair_index]
        return None

    def next_pair(self) -> Optional[ImagePair]:
        """Move to the next image pair."""
        if self.current_pair_index < len(self.similar_pairs) - 1:
            self.current_pair_index += 1
            return self.get_current_pair()
        return None

    def previous_pair(self) -> Optional[ImagePair]:
        """Move to the previous image pair."""
        if self.current_pair_index > 0:
            self.current_pair_index -= 1
            return self.get_current_pair()
        return None

    def trash_image(self, keep_left: bool) -> bool:
        """Keep one image and move the other to trash.

        Args:
            keep_left: If True, keep the left image; if False, keep the right image

        Returns:
            bool: True if the operation was successful, False otherwise
        """
        if not self.similar_pairs or self.current_pair_index < 0:
            return False

        pair = self.similar_pairs[self.current_pair_index]
        if not pair:
            return False

        # keep_path = pair.path1 if keep_left else pair.path2
        imd_del = pair[1] if keep_left else pair[0]
        discard_path = imd_del.path

        try:
            # Move discarded image to trash
            trash_path = os.path.join(self.trash_dir, os.path.basename(discard_path))

            # Handle filename collisions
            counter = 1
            while os.path.exists(trash_path):
                name, ext = os.path.splitext(os.path.basename(discard_path))
                trash_path = os.path.join(self.trash_dir, f"{name}_{counter}{ext}")
                counter += 1

            shutil.move(discard_path, trash_path)

            # Remove the processed pair from the list
            del self.similar_pairs[self.current_pair_index]
            self.similar_pairs = [
                ipair for ipair in self.similar_pairs if imd_del not in ipair
            ]

            # Adjust the current pair index if needed
            if self.current_pair_index >= len(self.similar_pairs):
                self.current_pair_index = max(0, len(self.similar_pairs) - 1)

            return True

        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def process_folder(self, folder_path: str) -> bool:
        """
        Process a folder to find and compare images.

        Returns:
            bool: True if processing was successful, False otherwise
        """
        if not os.path.isdir(folder_path):
            return False

        self.set_image_dir(folder_path)
        self.update_status("Scanning for images...")

        # Find all images in the directory
        image_paths = self.comparator.valid_images
        if len(image_paths) < 2:
            self.update_status("Not enough images found in the selected folder")
            return False

        self.update_status(
            f"Found {len(image_paths)} images. Computing similarities..."
        )

        # Find similar pairs
        self.find_similar_pairs()
        if not self.similar_pairs:
            self.update_status("No similar image pairs found.")
            return False

        # Set the first pair as current
        self.current_pair_index = 0
        return True

    def get_current_images(self) -> Optional[tuple[ImageData, ImageData, float]]:
        """Get the current pair of images and their similarity."""
        pair = self.get_current_pair()
        if not pair:
            return None
        return (pair.image_data1, pair.image_data2, pair.similarity)

    def has_next_pair(self) -> bool:
        """Check if there is a next pair available."""
        return 0 <= self.current_pair_index < len(self.similar_pairs) - 1

    def has_previous_pair(self) -> bool:
        """Check if there is a previous pair available."""
        return self.current_pair_index > 0

    def cleanup(self) -> None:
        """Clean up resources."""
        if hasattr(self.comparator, "close"):
            self.comparator.close()
