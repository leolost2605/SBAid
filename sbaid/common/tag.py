"""This module defines the Tag class"""
from gi.repository import GObject


class Tag(GObject.GObject):
    """TODO"""

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
        """TODO"""
        super().__init__(tag_id=tag_id, name=name)
