"""This module defines the Parameter class."""
from gi.repository import GLib, GObject, Gio

from sbaid import common
from sbaid.model.database.project_database import ProjectDatabase
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

    __db: ProjectDatabase
    __algo_config_id: str
    __available_tags: Gio.ListModel
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

    value: GLib.Variant | None = GObject.Property(  # type: ignore
        type=GObject.TYPE_VARIANT,  # type: ignore[arg-type]
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE)

    @value.getter  # type: ignore[no-redef]
    def value(self) -> GLib.Variant | None:
        """Returns the current value of the parameter."""
        return self.__value

    @value.setter  # type: ignore[no-redef]
    def value(self, value: GLib.Variant | None) -> None:
        if value is None:
            self.__value = None
            return

        if not value.is_of_type(self.value_type):
            raise ValueError(f"The given value is not of the correct value type. "
                             f"Is: {value.get_type_string()}, "
                             f"Expected: {self.value_type.dup_string()}")
        self.__value = value

        common.run_coro_in_background(self.__db.set_parameter_value(
            self.__algo_config_id, self.name, self.__get_cs_id(), value))

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
                 cross_section: CrossSection | None, db: ProjectDatabase,
                 algo_config_id: str,
                 available_tags: Gio.ListModel) -> None:
        super().__init__(name=name, value_type=value_type, cross_section=cross_section)
        self.__db = db
        self.__algo_config_id = algo_config_id
        self.__available_tags = available_tags
        if value.is_of_type(value_type):
            self.__value = value
        self.__selected_tags = Gio.ListStore.new(Tag)

        available_tags.connect("items-changed", self.__on_available_tags_changed)

    def __on_available_tags_changed(self, model: Gio.ListModel, changed_pos: int,
                                    removed: int, added: int) -> None:
        assert removed <= 1

        if removed == 1:
            for pos, tag in enumerate(common.list_model_iterator(self.__selected_tags)):
                found = False
                for available_tag in common.list_model_iterator(self.__available_tags):
                    if tag == available_tag:
                        found = True
                        break

                if not found:
                    # We don't call remove_tag because deletion from database is
                    # handled by cascading deletion
                    self.__selected_tags.remove(pos)
                    break

    def __get_cs_id(self) -> str | None:
        if self.cross_section is not None:
            return self.cross_section.id
        return None

    def add_tag(self, tag: Tag) -> None:
        """Adds the given tag to the list. Raises an exception if the tag was already added."""
        for t in common.list_model_iterator(self.__selected_tags):
            if t == tag:
                raise TagAlreadySetException("The given tag is already set for the parameter.")

        self.__selected_tags.append(tag)

        # TODO, Parameter Tag fixen in db
        common.run_coro_in_background(self.__db.add_parameter_tag(
            "this field should be removed", self.name,
            self.__algo_config_id, self.__get_cs_id(), tag.tag_id))

    def remove_tag(self, tag: Tag) -> None:
        """
        Removes the given tag from the list. Raises an exception if the tag isn't currently added.
        """
        for i, t in enumerate(common.list_model_iterator(self.__selected_tags)):
            if t == tag:
                self.__selected_tags.remove(i)

                # TODO, Parameter Tag fixen in db
                common.run_coro_in_background(self.__db.remove_parameter_tag(
                    "we need algo config, name, cs id and tag id"))

                return

        raise TagNotFoundException("Tried to remove tag, that wasn't set.")

    async def load_from_db(self) -> None:
        """Loads information about this parameter from the db"""
        cs_id = self.__get_cs_id()

        db_value = await self.__db.get_parameter_value(self.__algo_config_id, self.name, cs_id)
        if db_value is not None:
            self.__value = db_value

        tags = await self.__db.get_all_tag_ids_for_parameter(self.__algo_config_id,
                                                             self.name, cs_id)
        for tag in tags:
            name = await self.__db.get_tag_name(tag)

            if name:
                self.__selected_tags.append(Tag(tag, name))
            else:
                self.__selected_tags.append(Tag(tag, "Unknown Tag"))
