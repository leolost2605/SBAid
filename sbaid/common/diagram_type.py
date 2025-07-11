"""This module defines the DiagramType class"""
from gi.repository import GObject


class DiagramType(GObject.GObject):
    """TODO"""
    diagram_type_id = GObject.Property(type=str, flags=GObject.PARAM_READABLE)
    name = GObject.Property(type=str, flags=GObject.PARAM_WRITABLE)

    def __init__(self, diagram_type_id: str, name: str) -> None:
        """Initialize the diagram type."""
        self.diagram_type_id = diagram_type_id
        self.name = name
