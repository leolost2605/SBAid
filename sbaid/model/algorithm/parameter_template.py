"""todo"""
from typing import Optional

from gi.repository import GLib, GObject


class ParameterTemplate(GObject.GObject):
    """todo"""

    # GObject.Property definitions
    name = GObject.Property(type=str,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT_ONLY)
    value_type = GObject.Property(type=GLib.VariantType,
                                  flags=GObject.ParamFlags.READABLE |
                                  GObject.ParamFlags.WRITABLE |
                                  GObject.ParamFlags.CONSTRUCT_ONLY)
    # there seems to be a bug that you can't use GLib.Variant as type argument,
    # so instead use the GType directly even though mypy thinks it's wrong :(
    default_value = GObject.Property(type=GObject.TYPE_VARIANT,  # type: ignore
                                     flags=GObject.ParamFlags.READABLE |
                                     GObject.ParamFlags.WRITABLE |
                                     GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, name: str, value_type: GLib.VariantType,
                 default_value: Optional[GLib.Variant]) -> None:
        super().__init__(name=name, value_type=value_type, default_value=default_value)
