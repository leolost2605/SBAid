"""This module defines the Parameter class."""
from gi.repository import GLib, GObject, Gio

from sbaid import common
from sbaid.model.network.cross_section import CrossSection
from sbaid.common.tag import Tag


class TagAlreadySetException(Exception):
    """An exception that will be raised if the given tag is already in the list of tags."""


class TagNotFoundException(Exception):
    """An exception that will be raised if the given tag is not in the list of tags."""


class Parameter(GObject.GObject):
    """
    This class represents an editable parameter for the algorithm.
    The parameter can be global or cross section specific. In the latter case
    cross_section will not be none and will hold the cross section this parameter
    applies to.
    """

    __selected_tags: Gio.ListStore

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

    @GObject.Property(type=Gio.ListModel)
    def selected_tags(self) -> Gio.ListModel:
        """A list of the tags set for this parameter."""
        return self.__selected_tags

    def __init__(self, name: str, value_type: GLib.VariantType,
                 value: GLib.Variant,
                 cross_section: CrossSection | None) -> None:
        super().__init__(name=name, value_type=value_type, value=value, cross_section=cross_section)
        self.__selected_tags = Gio.ListStore.new(Tag)
        self.connect("notify::value", self.__on_value_changed)

    def add_tag(self, tag: Tag) -> None:
        """Adds the given tag to the list. Raises an exception if the tag was already added."""
        for t in common.list_model_iterator(self.__selected_tags):
            if t == tag:
                raise TagAlreadySetException("The given tag is already set for the parameter.")

        self.__selected_tags.append(tag)

    def remove_tag(self, tag: Tag) -> None:
        """
        Removes the given tag from the list. Raises an exception if the tag isn't currently added.
        """
        for i, t in enumerate(common.list_model_iterator(self.__selected_tags)):
            if t == tag:
                self.__selected_tags.remove(i)

        raise TagNotFoundException("Tried to remove tag, that wasn't set.")

    def load_from_db(self) -> None:
        """todo"""
        # TODO: Datbase load value

    def __on_value_changed(self) -> None:
        # TODO: Datbase set value
        pass
