"""This module defines the Parameter class."""
from typing import Optional
from gi.repository import GLib, GObject, Gio
from sbaid.model.network.cross_section import CrossSection
from sbaid.common.tag import Tag


class Parameter(GObject.GObject):
    """todo"""

    # GObject Property Definitions
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    value_type = GObject.Property(
        type=GLib.VariantType,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    value = GObject.Property(
        type=GObject.TYPE_VARIANT,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    cross_section = GObject.Property(
        type=CrossSection,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    selected_tags = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, name: str, value_type: GLib.VariantType,
                 value: GLib.Variant,
                 cross_section: Optional[CrossSection]) -> None:
        super().__init__()

    def add_tag(self, tag: Tag) -> None:
        """todo"""

    def remove_tag(self, tag: Tag) -> None:
        """todo"""

    def load_from_db(self) -> None:
        """todo"""
