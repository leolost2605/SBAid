""" This module represents the Result class."""
from gi.repository import Gio, GLib, GObject
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot
# import GlobalDatabase


class Result(GObject.GObject):
    """This class represents a result.
    Attributes: TODO check if critical information is missing
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

    snapshots = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY
    )

    def __init__(self, result_id: str, project_name: str,
                 creation_date_time: GLib.DateTime) -> None:
        """Initialize for the Result class."""
        # todo ask should the id not be generated internally?
        super().__init__(id=result_id,
                         project_name=project_name,
                         creation_date_time=creation_date_time,
                         selected_tags=Gio.ListStore.new(Tag),
                         snapshots=Gio.ListStore.new(Snapshot))

    def load(self) -> None:
        """todo this method handles the logic for loading snapshots."""
        # db_snapshots = [Snapshot]  # GlobalDatabase.get_all_snapshots(self.id)

        """ for snapshot in db_snapshots:
            new_snapshot = Snapshot(snapshot)
            new_snapshot.load_from_db()
            self.add_snapshot(new_snapshot) """

    def add_tag(self, tag: Tag) -> None:
        """Adds tag to the selected_tags list if it is not already present."""
        if tag not in self.selected_tags:
            self.selected_tags.append(tag)

    def remove_tag(self, tag: Tag) -> None:
        """Removes tag from the selected_tags list."""
        exists, position = self.selected_tags.find(tag)
        if exists:
            self.selected_tags.remove(position)

    def load_from_db(self) -> None:
        """todo"""

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """Adds a snapshot toe the list of snapshots"""
        self.snapshots.append(snapshot)
