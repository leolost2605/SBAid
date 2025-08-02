"""This module defines the seaborn image"""
from sbaid.common.image import Image

class SeabornImage(Image):
    """todo"""

    __image_bytes: bytes

    def __init__(self, image_bytes: bytes):
        super().__init__()
        self._image_bytes = image_bytes

    def save_to_file(self, path: str) -> None:

        with open(path, 'wb') as f:
            f.write(self._image_bytes)