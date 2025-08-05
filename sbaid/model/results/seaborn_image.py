"""This module defines the seaborn image"""
from gi.repository import Gdk, GLib
from sbaid.common.image import Image


class SeabornImage(Image):
    """Implements methods for handling images made out of seaborn diagrams."""

    __image_bytes: bytes
    __texture: Gdk.Texture

    def __init__(self, image_bytes: bytes):
        super().__init__()
        self._image_bytes = image_bytes
        self.__texture = Gdk.Texture.new_from_bytes(GLib.Bytes.new_take(list(image_bytes)))

    def save_to_file(self, path: str) -> None:
        """Saves image to desired file path"""
        with open(path, 'wb') as f:
            f.write(self._image_bytes)

    def do_snapshot(self, snapshot: Gdk.Snapshot, width: float, height: float) -> None:
        """Delegate method to texture."""
        self.__texture.snapshot(snapshot, width, height)

    def do_get_intrinsic_width(self) -> int:
        """Delegate method to texture."""
        return self.__texture.get_intrinsic_width()

    def do_get_intrinsic_height(self) -> int:
        """Delegate method to texture."""
        return self.__texture.get_intrinsic_height()

    def do_get_intrinsic_aspect_ratio(self) -> float:
        """Delegate method to texture."""
        return self.__texture.get_intrinsic_aspect_ratio()

    def do_get_flags(self) -> Gdk.PaintableFlags:
        """Delegate method to texture."""
        return self.__texture.get_flags()

    def do_get_current_image(self) -> Gdk.Paintable:
        """Delegate method to texture."""
        return self.__texture.get_current_image()
