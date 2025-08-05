"""This module defines the seaborn image"""
import uuid

from gi.repository import Gdk, Gio
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat


class SeabornImage(Image):
    """Implements methods for handling images made out of seaborn diagrams."""

    __image_bytes: bytes
    __texture: Gdk.Texture

    def __init__(self, image_bytes: bytes, export_format: ImageFormat):
        super().__init__()
        self._image_bytes = image_bytes
        random_name = uuid.uuid4().hex
        file_path = ("./tests/model/results/generator_outputs/" +
                     random_name + "." + export_format.name.lower())
        file = Gio.File.new_for_path(file_path)
        self.save_to_file(file_path)
        self.__texture = Gdk.Texture.new_from_file(file)

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
