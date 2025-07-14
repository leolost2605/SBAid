""" This module represents the Result class."""
from gi.repository import Gio, GLib, GObject
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot


class Result(GObject.GObject):
    """This class represents a result.
    Attributes: TODO checken ob kritische information fehlt
        result_id (str): The unique identifier of the result.
        result_name (str): The name of the result.
        project_name (str): The name of the project the result belongs to.
            Is created automatically from the result metadata.
        creation_date_time (DateTime): Date and time the result was created.
        selected_tags (ListModel<Tag>): Available tags for a result. Tags that have been
         added to the result are selected.
    """

    # GObject.Property definitions
    result_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    result_name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)
    project_name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    creation_date_time = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    selected_tags = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, result_id: str, project_name: str,
                 creation_date_time: GLib.DateTime) -> None:
        """todo"""

        self.selected_tags = Gio.ListStore.new(Tag)

        super().__init__(result_id=result_id,
                         project_name=project_name,
                         creation_date_time=creation_date_time)

    def load(self) -> None:
        """todo"""

    def add_tag(self, tag: Tag) -> None:
        """this method adds tag to the selected_tags list if it is not already present."""
        if tag not in self.selected_tags:
            self.selected_tags.append(tag)



    def remove_tag(self, tag: Tag) -> None:
        """this method removes tag from the selected_tags list."""
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)

    def print_tags(self):
        """only for testing, todo delete this"""
        for tag in self.selected_tags:
            print(tag.name)

    def load_from_db(self) -> None:
        """todo"""

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """todo"""


