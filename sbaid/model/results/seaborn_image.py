"""This module defines the seaborn image"""
from gi.repository import Gdk, GLib
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat


class SeabornImage(Image):
    """Implements methods for handling images made out of seaborn diagrams."""

    __image_bytes: bytes
    __texture: Gdk.Texture | None
    __export_format: ImageFormat

    def __init__(self, image_bytes: bytes, export_format: ImageFormat):
        super().__init__()
        self._image_bytes = image_bytes
        self.__export_format = export_format
        # separates supported types for gdk texture for the previews in the ui
        if self.__export_format == ImageFormat.PNG:
            self.__texture = Gdk.Texture.new_from_bytes(GLib.Bytes.new(list(image_bytes)))
        else:
            self.__texture = None

    def save_to_file(self, path: str) -> None:
        """Saves image to desired file path"""
        path_with_ending = path + "." + self.__export_format.name.lower()
        with open(path_with_ending, 'wb') as f:
            f.write(self._image_bytes)

    def do_snapshot(self, snapshot: Gdk.Snapshot, width: float, height: float) -> None:
        """Delegate method to texture."""
        if self.__texture is not None:
            self.__texture.snapshot(snapshot, width, height)

    def do_get_intrinsic_width(self) -> int | None:
        """Delegate method to texture."""
        if self.__texture is not None:
            return self.__texture.get_intrinsic_width()
        return None

    def do_get_intrinsic_height(self) -> int | None:
        """Delegate method to texture."""
        if self.__texture is not None:
            return self.__texture.get_intrinsic_height()
        return None

    def do_get_intrinsic_aspect_ratio(self) -> float | None:
        """Delegate method to texture."""
        if self.__texture is not None:
            return self.__texture.get_intrinsic_aspect_ratio()
        return None

    def do_get_flags(self) -> Gdk.PaintableFlags | None:
        """Delegate method to texture."""
        if self.__texture is not None:
            return self.__texture.get_flags()
        return None

    def do_get_current_image(self) -> Gdk.Paintable | None:
        """Delegate method to texture."""
        if self.__texture is not None:
            return self.__texture.get_current_image()
        return None
