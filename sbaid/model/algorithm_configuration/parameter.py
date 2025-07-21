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
        type=GObject.TYPE_VARIANT,  # type: ignore
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

        super().__init__(name=name,
                         value_type=value_type,
                         value=value,
                         cross_section=cross_section,
                         selected_tags=Gio.ListStore.new(Tag))

    def add_tag(self, tag: Tag) -> None:
        """Adds a tag to the list of selected tags."""
        self.selected_tags.append(tag)


    def remove_tag(self, tag: Tag) -> None:
        """Removes a tag from the list of selected tags."""
        exists, position = self.selected_tags.find(tag)
        if exists:
            self.selected_tags.remove(position)

    def load_from_db(self) -> None:
        """todo"""
