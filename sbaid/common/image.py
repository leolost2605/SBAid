"""This module defines the Image class,
which represents an image that can be painted within the UI"""
import gi

try:
    gi.require_version('Gdk', '4.0')
    from gi.repository import Gdk
except ImportError as exception:
    print('Error: Gdk is not installed correctly.', exception)
except ValueError as exception:
    print('Error: Gdk has an inappropriate argument value.', exception)


class Image(Gdk.Paintable):
    """TODO"""

    def save_to_file(self, path: str) -> None:
        """Saves the image to a file at the specified path."""
