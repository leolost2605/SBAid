from gi.repository import GObject
from gi.repository import GLib
from typing import Optional


class ParameterState(GObject.GObject):
    """TODO"""
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    value = GObject.Property(
        type=GLib.Variant,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_id = GObject.Property(
        type=Optional[str],
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, name: str, value: GLib.Variant, cross_section_id: Optional[str]) -> None:
        """TODO"""
        super().__init__(name=name, value=value, cross_section_id=cross_section_id)

