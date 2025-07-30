# image_comparator.py
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import os
from pathlib import Path
from photo_condenser.image_data import ImageData
from photo_condenser.img_cache import ImageDataCache


@dataclass
class ImagePair:
    """Represents a pair of similar images."""

    image1: ImageData
    image2: ImageData
    similarity: float


class ImageComparator:
    """Handles comparison of images to find duplicates or similar images."""

    def __init__(self, threshold: float = 0.85):
        """Initialize the image comparator.

        Args:
            threshold: Similarity threshold (0-1) above which images are considered similar
        """
        self.threshold = threshold
        self.valid_images = None

    def set_images(self, image_dir: str) -> None:
        """Set the working directory for histogram caching.

        Args:
            directory: Directory where the cache database will be stored
        """
        self.image_dir = image_dir
        self.cache = ImageDataCache(image_dir)
        image_paths = self.find_images()

        self.valid_images = [
            ImageData.from_file(path, self.cache) for path in image_paths
        ]
        img_dict = {img.hash: img for img in self.valid_images}

        cached_embeddings = self.cache.get_embeddings(list(img_dict.keys()))

        for img_hash, cached in cached_embeddings.items():
            img_dict[img_hash]._ml_embedding = cached

    def find_images(self) -> List[str]:
        """Find all supported images in the current directory."""
        if not self.image_dir or not os.path.isdir(self.image_dir):
            return []

        extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")
        return [
            str(p)
            for p in Path(self.image_dir).glob("*")
            if p.suffix.lower() in extensions and "trash" not in str(p)
        ]

    def find_similar_pairs(self) -> List[ImagePair]:
        """Find all pairs of similar images in the given list.

        Args:
            image_paths: List of paths to images to compare

        Returns:
            List of ImagePair objects for similar image pairs, sorted by similarity (highest first)
        """
        if not self.valid_images:
            raise RuntimeError(
                "Directory must be set using set_directory() before finding similar pairs"
            )

        pairs = []

        # Compare all pairs
        n = len(self.valid_images)
        for i in range(n):
            for j in range(i + 1, n):
                similarity = float(
                    np.dot(
                        self.valid_images[i].ml_embedding.T,
                        self.valid_images[j].ml_embedding,
                    )
                    .squeeze()
                    .item()
                )

                # Convert from [-1, 1] to [0, 1] range
                similarity = (similarity + 1) / 2

                if similarity >= self.threshold:
                    pairs.append(
                        ImagePair(
                            image1=self.valid_images[i],
                            image2=self.valid_images[j],
                            similarity=float(similarity),
                        )
                    )

        # Sort by similarity (highest first)
        pairs.sort(key=lambda x: x.similarity, reverse=True)
        return pairs

    def close(self) -> None:
        """Clean up resources used by the comparator."""
        if self.cache:
            self.cache.close()
            self.cache = None

    def __del__(self):
        """Ensure resources are cleaned up when the object is destroyed."""
        self.close()
