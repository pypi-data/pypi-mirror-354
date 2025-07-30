"""
Persistent cache for image histograms using SQLite for storage.
"""

import os
import sqlite3
from typing import Optional, List, Dict
import hashlib
import numpy as np


class ImageDataCache:
    """Manages persistent storage of image data using SQLite for faster comparison."""

    DB_FILENAME = ".condense.db"

    def __init__(self, directory: str):
        """Initialize the histogram cache.

        Args:
            directory: Directory where the database file will be stored
        """
        self.directory = os.path.abspath(directory)
        self.db_path = os.path.join(self.directory, self.DB_FILENAME)
        self._conn = None
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection, creating it if necessary."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            # Enable foreign keys
            self._conn.execute("PRAGMA foreign_keys = ON")
            # Use WAL mode for better concurrency
            self._conn.execute("PRAGMA journal_mode = WAL")
        return self._conn

    def _init_db(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    hash TEXT PRIMARY KEY,
                    ml_embedding BLOB NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_images_hash
                ON images(hash)
            """)


    def __contains__(self, img_hash: str) -> bool:
        """Check if the image is in the cache."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM images 
                WHERE hash = ?
            """,
                (img_hash,),
            )
            count= cursor.rowcount > 0
        return count

    def get_embeddings(self, img_hashes: List[str]) -> Dict[str, np.ndarray]:
        """Get the histograms for a list of images, either from cache or by computing them.

        Args:
            img_hashes: List of hashes of images

        Returns:
            Dictionary of histograms, with the same order as the input list
        """
        
        placeholders = ','.join(['?'] * len(img_hashes))
        query = f"SELECT * FROM images WHERE hash IN ({placeholders})"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, img_hashes)
            out = cursor.fetchall()
        embeddings = {}
        for e in out:
            hash, embedding=e
            embeddings[hash] = np.frombuffer(embedding, dtype=np.float32).reshape(-1, 1)
        return embeddings


    def __getitem__(self, img_hash: str) -> Optional[np.ndarray]:
        """Get the histogram for an image, either from cache or by computing it.

        Args:
            img_hash: Hash of the image

        Returns:
            Normalized histogram as a numpy array, or None if the image couldn't be processed
        """
        # Try to get from cache
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT ml_embedding FROM images 
                WHERE hash = ?
            """,
                (img_hash,),
            )
            if cursor.rowcount > 0:
                result = cursor.fetchone()
                if result is not None:
                    # Deserialize the histogram
                    hist_data = np.frombuffer(result[0], dtype=np.float32)
                return hist_data.reshape(-1, 1)  # Reshape to column vector
        return None

    def __setitem__(self, img_hash: str, ml_embedding: np.ndarray) -> None:
        # Store in database
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO images 
                (hash, ml_embedding) 
                VALUES (?, ?)
            """,
                (img_hash, ml_embedding.tobytes()),
            )
            conn.commit()

    def __delitem__(self, img_hash: str) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM images WHERE hash = ?", (img_hash,))
            conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __del__(self):
        """Ensure the database connection is closed when the object is destroyed."""
        self.close()