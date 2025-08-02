""" This module represents the Result class."""
from gi.repository import Gio, GLib, GObject
from sbaid.common.tag import Tag
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.database.global_database import GlobalDatabase


class Result(GObject.GObject):
    """This class represents a result.
    Attributes:
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
    __global_db: GlobalDatabase

    def __init__(self, result_id: str, project_name: str,
                 creation_date_time: GLib.DateTime, global_db: GlobalDatabase) -> None:
        """Initializes the Result class."""
        super().__init__(id=result_id,
                         project_name=project_name,
                         creation_date_time=creation_date_time,
                         selected_tags=Gio.ListStore.new(Tag),
                         snapshots=Gio.ListStore.new(Snapshot))

        self.__global_db = global_db

    async def load(self) -> None:
        """Handles the logic for loading snapshots."""
        db_snapshots = await self.__global_db.get_all_snapshots(self.id)

        for snapshot in db_snapshots:
            new_snapshot = Snapshot(snapshot[0], snapshot[1], self.__global_db)
            await new_snapshot.load_from_db()
            self.add_snapshot(new_snapshot)

    def add_tag(self, tag: Tag) -> None:
        """Adds tag to the selected_tags list"""
        self.selected_tags.append(tag)  # pylint:disable=no-member

    def remove_tag(self, tag: Tag) -> None:
        """Removes tag from the selected_tags list."""
        exists, position = self.selected_tags.find(tag)  # pylint:disable=no-member
        if exists:
            self.selected_tags.remove(position)  # pylint:disable=no-member

    async def load_from_db(self) -> None:
        """Loads metainformation about the result name and tags, and saves them in the class."""
        self.result_name = await self.__global_db.get_result_name(self.id)
        self.selected_tags = await self.__global_db.get_result_tags(self.id)

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """Adds a snapshot toe the list of snapshots"""
        self.snapshots.append(snapshot)  # pylint:disable=no-member
