""" This module represents the Result class."""

from gi.repository import Gio, GLib, GObject
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot


class Result(GObject.GObject):
    """This class represents a result.
    Attributes: TODO checken ob kritische information fehlt
        id (str): The unique identifier of the result.
        result_name (str): The name of the result.
        project_name (str): The name of the project the result belongs to.
            Is created automatically from the result metadata.
        creation_date_time (DateTime): Date and time the result was created.
        selected_tags (ListModel<Tag>): Available tags for a result. Tags that have been
         added to the result are selected.
    """

    # GObject.Property definitions
    id = GObject.Property(
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
        super().__init__(id=result_id,
                         project_name=project_name,
                         creation_date_time=creation_date_time)

    def load(self) -> None:
        """todo"""

    def add_tag(self, tag: Tag) -> None:
        """todo"""

    def remove_tag(self, tag: Tag) -> None:
        """todo"""

    def load_from_db(self) -> None:
        """todo"""

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """todo"""
