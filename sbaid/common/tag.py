"""This module defines the Tag class"""
from gi.repository import GObject


class Tag(GObject.GObject):
    """TODO"""

    # GObject property definition
    tag_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.CONSTRUCT)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE
    )

    def __init__(self, tag_id: str, name: str) -> None:
        """Initialize the tag with an id and a name."""
        self.tag_id = tag_id
        self.name = name
