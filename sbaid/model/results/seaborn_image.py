"""This module defines the seaborn image"""

from sbaid.common.image import Image


class SeabornImage(Image):
    """Implements methods for handling images made out of seaborn diagrams."""

    __image_bytes: bytes

    def __init__(self, image_bytes: bytes):
        super().__init__()
        self._image_bytes = image_bytes

    def save_to_file(self, path: str) -> None:
        """Saves image to desired file path"""
        with open(path, 'wb') as f:
            f.write(self._image_bytes)
