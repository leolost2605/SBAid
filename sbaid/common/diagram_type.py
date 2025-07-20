"""This module defines the DiagramType class"""
from gi.repository import GObject


class DiagramType(GObject.GObject):
    """TODO"""
    diagram_type_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)
    is_diagram_global = GObject.Property(
        type=GObject.TYPE_BOOLEAN,
        default=False,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, diagram_type_id: str, name: str, is_global: bool) -> None:
        """TODO"""
        super().__init__(diagram_type_id=diagram_type_id, name=name, is_diagram_global=is_global)
