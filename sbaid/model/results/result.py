""" This module represents the Result class."""

from gi.repository import Gio, GLib, GObject

from sbaid import common
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
    id: str = GObject.Property(   # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    result_name: str = GObject.Property(type=str)  # type: ignore

    @result_name.getter  # type: ignore
    def result_name(self) -> str:
        return self.__name

    @result_name.setter  # type: ignore
    def result_name(self, new_name: str) -> None:
        self.__name = new_name

        print("set name ", new_name)
        common.run_coro_in_background(self.__global_db.set_result_name(self.id, new_name))

    project_name: str = GObject.Property(   # type: ignore
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    creation_date_time: GLib.DateTime = GObject.Property(   # type: ignore
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    selected_tags: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @selected_tags.getter  # type: ignore
    def selected_tags(self) -> Gio.ListModel:
        """Getter for the selected tags."""
        return self.__selected_tags

    snapshots: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @snapshots.getter  # type: ignore
    def snapshots(self) -> Gio.ListModel:
        """Getter for the snapshots."""
        return self.__snapshots

    __name: str
    __snapshots: Gio.ListStore
    __selected_tags: Gio.ListStore
    __global_db: GlobalDatabase

    def __init__(self, result_id: str, project_name: str,
                 creation_date_time: GLib.DateTime, global_db: GlobalDatabase) -> None:
        """Initializes the Result class."""
        super().__init__(id=result_id,
                         project_name=project_name,
                         creation_date_time=creation_date_time)

        self.__name = project_name + "_" + str(creation_date_time.format("%F"))
        self.__snapshots = Gio.ListStore.new(Snapshot)
        self.__selected_tags = Gio.ListStore.new(Tag)
        self.__global_db = global_db

    async def load(self) -> None:
        """Handles the logic for loading snapshots."""
        if self.__snapshots.get_n_items():  # We are already loaded
            return

        db_snapshots = await self.__global_db.get_all_snapshots(self.id)

        for snapshot in db_snapshots:
            new_snapshot = Snapshot(snapshot[0], snapshot[1], self.__global_db)
            await new_snapshot.load_from_db()
            self.add_snapshot(new_snapshot)

    def add_tag(self, tag: Tag) -> None:
        """Adds tag to the selected_tags list"""
        self.__selected_tags.append(tag)

    def remove_tag(self, tag: Tag) -> None:
        """Removes tag from the selected_tags list."""
        exists, position = self.__selected_tags.find(tag)
        if exists:
            self.__selected_tags.remove(position)

    async def load_from_db(self) -> None:
        """Loads metainformation about the result name and tags, and saves them in the class."""
        name_from_db = await self.__global_db.get_result_name(self.id)
        if name_from_db is not None:
            self.__name = name_from_db
            self.notify("result-name")

        tag_ids = await self.__global_db.get_result_tag_ids(self.id)

        for tag_id in tag_ids:
            tag_name = await self.__global_db.get_tag_name(tag_id)
            if tag_name is not None:
                self.add_tag(Tag(tag_id, tag_name))

    def add_snapshot(self, snapshot: Snapshot) -> None:
        """Adds a snapshot toe the list of snapshots"""
        self.__snapshots.append(snapshot)
