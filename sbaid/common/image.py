"""This module defines the Image class,
which represents an image that can be painted within the UI"""
from gi.repository import Gdk


class Image(Gdk.Paintable):
    """This class represents an image that can be painted within the UI."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_to_file(self, path: str) -> None:
        """Saves the image to a file at the specified path."""
