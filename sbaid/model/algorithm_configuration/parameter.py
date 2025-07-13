"""This module defines the Parameter class."""
from gi.repository import GLib, GObject, Gio
from typing import Optional
from sbaid.model.network import CrossSection

class Parameter(GObject.GObject):

    # GObject Property Definitions
    name = GObject.Property(
        type=str,
        flags = GObject.ParamFlags.READABLE |
                GObject.ParamFlags.WRITABLE |
                GObject.ParamFlags.CONSTRUCT_ONLY)

    value_type = GObject.Property(
        type=GLib.VariantType,
        flags = GObject.ParamFlags.READABLE |
                GObject.ParamFlags.WRITABLE |
                GObject.ParamFlags.CONSTRUCT_ONLY)

    value = GObject.Property(
        type=GLib.Variant,
        flags = GObject.ParamFlags.READABLE |
                GObject.ParamFlags.WRITABLE |
                GObject.ParamFlags.CONSTRUCT_ONLY)

    cross_section = GObject.Property(
        type=Gio.ListModel,
        flags = GObject.ParamFlags.READABLE |
                GObject.ParamFlags.WRITABLE |
                GObject.ParamFlags.CONSTRUCT_ONLY)

    selected_tags= GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, name: str, value_type: GLib.VariantType,
                 value: GLib.Variant, cross_section: Optional[CrossSection] = None) -> None:
        self.name = name
        self.value_type = value_type
        self.value = value
        self.cross_section = cross_section
        pass

    def add_tag(self, tag: Tag) -> None:
        """todo"""
        pass

    def remove_tag(self, tag: Tag) -> None:
        """todo"""
        pass

    def load_from_db(self) -> None:
        """todo"""
        pass