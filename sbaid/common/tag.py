"""This module defines the Tag class"""
from gi.repository import GObject


class Tag(GObject.GObject):
    """This class represents a tag."""

    # GObject property definition
    tag_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT
    )

    def __init__(self, tag_id: str, name: str) -> None:
        """Constructs a new tag with its id and name."""
        super().__init__(tag_id=tag_id, name=name)

    def __eq__(self, other: object) -> bool:
        """Verify if this tag already exists."""
        return isinstance(other, Tag) and self.tag_id == other.tag_id
