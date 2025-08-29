"""This module defines the ParameterExportFormat class."""
from gi.repository import GObject


class ParameterExportFormat(GObject.GObject):
    """This class represents a parameter export format."""
    format_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, format_id: str, name: str) -> None:
        """Constructs the diagram type."""
        super().__init__(format_id=format_id, name=name)
