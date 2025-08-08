"""This module defines the Image class,
which represents an image that can be painted within the UI"""
import gi

try:
    gi.require_version('Gdk', '4.0')
    from gi.repository import GObject, Gdk
except ImportError as exception:
    print('Error: Gdk is not installed correctly.', exception)
except ValueError as exception:
    print('Error: Gdk has an inappropriate argument value.', exception)


class Image(GObject.GObject, Gdk.Paintable):  # type: ignore
    """
    This class serves as an interface that has to be implemented by diagrams for preview in the ui
    and saving.
    """

    def save_to_file(self, path: str) -> None:
        """Saves the image to a file at the specified path."""
