from xmlrpc.client import DateTime
from gi.repository import GLib, GObject
from sbaid.common.tag import Tag
from sbaid.results.snapshot import Snapshot
""" This module represents the Result class."""

class Result:
    """This class represents a result.
    Attributes: TODO checken ob kritische information fehlt
        result_id (str): The unique identifier of the result.
        result_name (str): The name of the result.
        project_name (str): The name of the project the result belongs to. Is created automatically from the result metadata.
        creation_date_time (DateTime): Date and time the result was created.
        selected_tags (ListModel<Tag>): Available tags with tags that have been added to the result selected.
    """

    #GObject.Property definitions
    result_id = GObject.Property(type=str)
    result_name = GObject.Property(type=str)
    project_name = GObject.Property(type=str)
    creation_date_time = GObject.Property(type=DateTime)
    selected_tags = GObject.Property(type=GLib.ListModel)

    def __init__(self, result_id: str, project_name: str, creation_date_time: DateTime) -> None:
        """todo"""
        self.result_id = result_id
        self.project_name = project_name
        self.creation_date_time = creation_date_time

    def load(self) -> None:
        """todo"""
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

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """todo"""
        pass
