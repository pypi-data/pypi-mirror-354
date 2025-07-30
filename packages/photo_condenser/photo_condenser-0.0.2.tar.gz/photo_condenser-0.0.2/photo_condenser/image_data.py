# image_data.py
import os
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple
import hashlib
from photo_condenser.img_cache import ImageDataCache
from photo_condenser.model import onnx_model
from PIL import Image


class ImageData:
    """Represents an image and its essential properties for deduplication."""

    def __init__(self, path: str, cache: ImageDataCache):
        self.path = path
        self._image: Optional[np.ndarray] = None
        self._hash: Optional[str] = None
        self._ml_embedding: Optional[np.ndarray] = None

        """Initialize computed properties."""
        self.path = os.path.abspath(self.path)
        if self.hash in cache:
            cache_info = cache[self.hash]
            for k, v in cache_info.items():
                assert hasattr(self, f"_{k}")
                setattr(self, f"_{k}", v)
        else:
            cache[self.hash] = self.ml_embedding

    @property
    def hash(self) -> str:
        """Calculate a hash of the file contents for change detection."""
        if self._hash is None:
            hasher = hashlib.md5()
            with open(self.path, "rb") as f:
                buf = f.read(65536)  # Read in 64k chunks
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            self._hash = hasher.hexdigest()
        return self._hash

    @property
    def ml_embedding(self):
        """Get the color ml_embedding of the image for comparison."""
        if self._ml_embedding is None and self.image is not None:
            self._ml_embedding = onnx_model(self.image)
        return self._ml_embedding

    @property
    def image(self) -> np.ndarray:
        """Load the image data if not already loaded."""
        if self._image is None:
            self._image = Image.open(self.path).convert("RGB")
            if self._image is None:
                raise ValueError(f"Could not load image: {self.path}")
        return self._image

    def unload_image(self) -> None:
        """Unload the image data to free memory."""
        self._image = None

    @classmethod
    def from_file(cls, path: str, cache: ImageDataCache) -> "ImageData":
        """Create an ImageData instance from a file path."""
        return cls(path=path, cache=cache)

    def __eq__(self, other: object) -> bool:
        """Check if two ImageData instances represent the same file."""
        raise NotImplementedError
        if not isinstance(other, ImageData):
            return False
        return (
            os.path.samefile(self.path, other.path)
            if os.path.exists(self.path) and os.path.exists(other.path)
            else self.path == other.path
        )

    def __hash__(self) -> int:
        """Make ImageData hashable based on its path."""
        return self.hash

    def get_dimensions(self) -> tuple[int, int]:
        """Get the dimensions of the image.

        Returns:
            tuple: (width, height) of the image. Returns (0, 0) if the image cannot be read.
        """
        return self.image.size

    def is_landscape(self) -> bool:
        """Check if the image is in landscape orientation.

        Returns:
            bool: True if image is landscape (width > height), False otherwise
        """
        width, height = self.get_dimensions()
        return width > height if width > 0 and height > 0 else False
