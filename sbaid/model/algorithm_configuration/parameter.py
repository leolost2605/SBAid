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

    __value: GLib.Variant | None = None
    __selected_tags: Gio.ListStore

    name: str = GObject.Property(  # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    value_type: GLib.VariantType = GObject.Property(  # type: ignore
        type=GLib.VariantType,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    value: GLib.Variant = GObject.Property(  # type: ignore
        type=GObject.TYPE_VARIANT,  # type: ignore[arg-type]
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE)

    @value.getter  # type: ignore[no-redef]
    def value(self) -> GLib.Variant | None:
        """Returns the current value of the parameter."""
        return self.__value

    @value.setter  # type: ignore[no-redef]
    def value(self, value: GLib.Variant | None) -> None:
        if not value:
            self.__value = None
            return

        if not value.is_of_type(self.value_type):
            raise ValueError(f"The given value is not of the correct value type. "
                             f"Is: {value.get_type_string()}, "
                             f"Expected: {self.value_type.dup_string()}")
        self.__value = value
        # TODO: Write to db

    cross_section: CrossSection = GObject.Property(  # type: ignore
        type=CrossSection,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    selected_tags: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    @selected_tags.getter  # type: ignore
    def selected_tags(self) -> Gio.ListModel:
        """A list of the tags set for this parameter."""
        return self.__selected_tags

    def __init__(self, name: str, value_type: GLib.VariantType,
                 value: GLib.Variant | None,
                 cross_section: CrossSection | None) -> None:
        super().__init__(name=name, value_type=value_type, cross_section=cross_section)
        self.value = value
        self.__selected_tags = Gio.ListStore.new(Tag)

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
                return

        raise TagNotFoundException("Tried to remove tag, that wasn't set.")

    def load_from_db(self) -> None:
        """todo"""
        # TODO: Datbase load value
