"""This module defines the DiagramType class"""
from gi.repository import GObject


class DiagramType(GObject.GObject):
    """TODO"""
    diagram_type_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)

    def __init__(self, diagram_type_id: str, name: str) -> None:
        """TOOD"""
        super().__init__(diagram_type_id=diagram_type_id, name=name)
