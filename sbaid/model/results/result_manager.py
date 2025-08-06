"""This module defines the ResultManager class."""
import uuid
from gi.repository import Gio, GObject
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.result import Result
from sbaid.common.tag import Tag
from sbaid.common import list_model_iterator
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot


class ResultManager(GObject.GObject):
    """This class handles a list of results and tags."""

    # GObject.Property definitions
    results: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @results.getter  # type: ignore
    def results(self) -> Gio.ListModel:
        """Getter for the results."""
        return self.__results

    available_tags: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @available_tags.getter  # type: ignore
    def available_tags(self) -> Gio.ListModel:
        """Getter for the available tags."""
        return self.__available_tags

    __available_tags: Gio.ListStore
    __results: Gio.ListStore
    __global_db: GlobalDatabase

    def global_db(self) -> GlobalDatabase:
        """Getter for the global database."""
        return self.__global_db

    def __init__(self, global_db: GlobalDatabase) -> None:
        """Initialize the ResultManager class."""
        super().__init__()
        self.__available_tags = Gio.ListStore.new(Tag)
        self.__results = Gio.ListStore.new(Result)
        self.__global_db = global_db

    async def load_from_db(self) -> None:
        """Loads metainformation about the results and tags from the global database"""
        result_information = await self.__global_db.get_all_results()
        for results in result_information:
            result = Result(results[0], results[2], results[3], self.__global_db)
            result.result_name = results[1]

            tag_information = await self.__global_db.get_all_tags()

            for tag in tag_information:
                new_tag = Tag(tag[0], tag[1])
                result.add_tag(new_tag)
                if not self.__is_tag_already_loaded(tag[0]):
                    self.__available_tags.append(new_tag)

            self.__results.append(result)

    def __is_tag_already_loaded(self, tag_id: str) -> bool:
        """Checks if a tag is already loaded."""
        for tag in self.__available_tags:
            assert isinstance(tag, Tag)
            if tag_id == tag.tag_id:
                return True
        return False

    async def create_tag(self, name: str) -> int:
        """Creates a new tag with the given name and adds it to the list of available tags."""
        new_tag_id = str(uuid.uuid4())
        new_tag = Tag(new_tag_id, name)
        await self.__global_db.add_tag(new_tag_id, name)
        self.__available_tags.append(new_tag)
        return len(self.__available_tags) - 1

    async def delete_tag(self, tags_id: str) -> None:
        """Removes a tag with the given id from the list of available tags,
         and removes all its uses in results"""
        for i, tag in enumerate(list_model_iterator(self.__available_tags)):
            assert isinstance(tag, Tag)
            if tags_id == tag.tag_id:
                self.__available_tags.remove(i)
                for result in enumerate(list_model_iterator(self.__results)):
                    assert isinstance(result, Result)
                    result.remove_tag(tag)
                    # await self.__global_db.remove_result_tag(result.id, tag.tag_id)
                break
            await self.__global_db.remove_tag(tags_id)

    async def delete_result(self, result_id: str) -> None:
        """Removes a result with the given id from the list of available tags."""
        for i, result in enumerate(list_model_iterator(self.__results)):
            assert isinstance(result, Result)
            if result.id == result_id:
                self.__results.remove(i)
                await self.__global_db.delete_result(result_id)
                break

    async def register_result(self, result: Result) -> None:
        """Appends a result to the existing list of results in the result manager.
        Also registers result and all snapshots to the database"""
        self.__results.append(result)
        await self.__global_db.add_result(result.id,
                                          result.result_name,
                                          result.project_name,
                                          result.creation_date_time)
        await self.__add_all_snapshots_to_database(result)

    async def __add_all_snapshots_to_database(self, result: Result) -> None:

        for snapshot in result.snapshots:
            assert isinstance(snapshot, Snapshot)

            await self.__global_db.add_snapshot(snapshot.id,
                                                result.id,
                                                snapshot.capture_timestamp)
            for cs_snapshot in snapshot.cross_section_snapshots:
                assert isinstance(cs_snapshot, CrossSectionSnapshot)

                await self.__global_db.add_cross_section_snapshot(cs_snapshot.cs_snapshot_id,
                                                                  cs_snapshot.snapshot_id,
                                                                  cs_snapshot.cross_section_name,
                                                                  cs_snapshot.b_display)

                for lane_snapshot in cs_snapshot.lane_snapshots:
                    assert isinstance(lane_snapshot, LaneSnapshot)

                    await self.__global_db.add_lane_snapshot(lane_snapshot.id,
                                                             lane_snapshot.
                                                             cross_section_snapshot_id,
                                                             lane_snapshot.lane,
                                                             lane_snapshot.average_speed,
                                                             lane_snapshot.traffic_volume,
                                                             lane_snapshot.a_display)

                    for vehicle_snapshot in lane_snapshot.vehicle_snapshots:
                        assert isinstance(vehicle_snapshot, VehicleSnapshot)
                        await self.__global_db.add_vehicle_snapshot(vehicle_snapshot.
                                                                    lane_snapshot_id,
                                                                    vehicle_snapshot.vehicle_type,
                                                                    vehicle_snapshot.speed)
