"""TODO"""
from typing import Optional
from gi.repository import GObject
from gi.repository import GLib


class ParameterState(GObject.GObject):
    """TODO"""
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    value = GObject.Property(
        # mypy thinks this is wrong but it actually isn't yay, confirmed via actual testing
        type=GObject.TYPE_VARIANT,  # type: ignore
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    cross_section_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, name: str, value: GLib.Variant, cross_section_id: Optional[str]) -> None:
        """TODO"""
        super().__init__(name=name, value=value, cross_section_id=cross_section_id)
