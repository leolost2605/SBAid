"""This module defines the ResultBuilder class and its helper classes"""
import uuid
from typing import Self
from gi.repository import GLib, GObject
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.lane_snapshot import LaneSnapshot
from sbaid.model.results.result_manager import ResultManager
from sbaid.common.b_display import BDisplay
from sbaid.model.results.result import Result
from sbaid.model.results.snapshot import Snapshot
from sbaid.model.results.vehicle_snapshot import VehicleSnapshot


class _CrossSectionBuilder:
    """This auxiliary class contains the cross-section snapshot builder methods"""
    # required for construction
    __cross_section_name: str
    __cross_section_id: str
    __snapshot_id: str
    __global_db: GlobalDatabase

    # added later
    __cross_section_b_display: BDisplay | None

    def __init__(self, cs_name: str, snapshot_id: str, cross_section_id: str,
                 global_db: GlobalDatabase) -> None:
        self.__cross_section_name = cs_name
        self.__snapshot_id = snapshot_id
        self.__cross_section_id = cross_section_id
        self.__global_db = global_db
        self.__cross_section_b_display = None

    def set_b_display(self, b_display: BDisplay) -> Self:
        """Setter for b_display"""
        self.__cross_section_b_display = b_display
        return self

    def try_build(self) -> CrossSectionSnapshot | None:
        """Builds and returns cross-section snapshot if attributes complete, None otherwise"""
        if self.__cross_section_b_display is not None:
            return CrossSectionSnapshot(self.__snapshot_id, str(uuid.uuid4()),
                                        self.__cross_section_name,
                                        self.__cross_section_id,
                                        self.__cross_section_b_display, self.__global_db)
        return None


class _LaneBuilder:
    """This auxiliary class contains the lane snapshot builder methods"""
    # required for construction
    __lane_number: int
    __cross_section_id: str
    __global_db: GlobalDatabase
    # added later
    __average_speed: float | None
    __traffic_volume: int | None
    __a_display: ADisplay | None

    def __init__(self, lane_number: int, cross_section_id: str, global_db: GlobalDatabase) -> None:
        self.__lane_number = lane_number
        self.__cross_section_id = cross_section_id
        self.__global_db = global_db
        self.__average_speed = None
        self.__traffic_volume = None
        self.__a_display = None

    def set_average_speed(self, average_speed: float) -> Self:
        """Setter for average_speed"""
        self.__average_speed = average_speed
        return self

    def set_traffic_volume(self, traffic_volume: int) -> Self:
        """Setter for traffic_volume"""
        self.__traffic_volume = traffic_volume
        return self

    def set_a_display(self, a_display: ADisplay) -> Self:
        """Setter for a_display"""
        self.__a_display = a_display
        return self

    def try_build(self) -> LaneSnapshot | None:
        """Builds and returns lane snapshot if attributes complete, None otherwise"""
        if (self.__average_speed is not None) and (self.__average_speed is not None) and (
                self.__traffic_volume is not None) and (self.__a_display is not None):
            return LaneSnapshot(self.__cross_section_id,
                                str(uuid.uuid4()),
                                self.__lane_number,
                                self.__average_speed,
                                self.__traffic_volume,
                                self.__a_display,
                                self.__global_db)
        return None


class _VehicleBuilder:
    """This auxiliary class contains the vehicle snapshot builder methods"""
    # required for construction
    __lane_id: str
    # added later
    __vehicle_type: VehicleType | None
    __vehicle_speed: float | None

    def __init__(self, lane_id: str) -> None:
        self.__lane_id = lane_id
        self.__vehicle_type = None
        self.__vehicle_speed = None

    def set_vehicle_type(self, vehicle_type: VehicleType) -> Self:
        """Setter for vehicle_type"""
        self.__vehicle_type = vehicle_type
        return self

    def set_vehicle_speed(self, vehicle_speed: float) -> Self:
        """Setter for vehicle_speed"""
        self.__vehicle_speed = vehicle_speed
        return self

    def try_build(self) -> VehicleSnapshot | None:
        """Builds and returns vehicle snapshot if attributes complete, None otherwise"""
        if self.__vehicle_type is not None and self.__vehicle_speed is not None:
            return VehicleSnapshot(self.__lane_id, self.__vehicle_type, self.__vehicle_speed)
        return None


class ResultBuilder(GObject.GObject):  # pylint:disable=too-many-instance-attributes
    """Contains methods to build the results."""
    __result_manager: ResultManager
    __global_db: GlobalDatabase

    # the following optionals are also used for controlling the logic
    # that regulates the correct building order.

    __current_result: Result | None = None
    __current_snapshot: Snapshot | None = None

    __current_cross_section: CrossSectionSnapshot | None = None
    __current_cs_builder: _CrossSectionBuilder | None = None

    __current_lane: LaneSnapshot | None = None
    __current_lane_builder: _LaneBuilder | None = None

    __current_vehicle: VehicleSnapshot | None = None
    __current_vehicle_builder: _VehicleBuilder | None = None

    def __init__(self, result_manager: ResultManager, global_db: GlobalDatabase) -> None:
        """Initializes the ResultBuilder class."""
        super().__init__()
        self.__result_manager = result_manager
        self.__global_db = global_db

    def begin_result(self, project_name: str) -> None:
        """Sets current_result to a new result instance using
        the given project name and the current local time."""
        now = GLib.DateTime.new_now_local()

        if now is None:
            raise GLibErrorException("Could not get current time from local system")

        self.__current_result = Result(str(uuid.uuid4()),
                                       project_name, now, self.__global_db)

    def begin_snapshot(self, simulation_timestamp: GLib.DateTime) -> None:
        """Sets current_snapshot to a new snapshot with the given timestamp."""
        if self.__current_result is None:
            raise WrongOrderException("Result has not been set")

        self.__current_snapshot = Snapshot(str(uuid.uuid4()),
                                           simulation_timestamp, self.__global_db)

    def begin_cross_section(self, cross_section_id: str, cross_section_name: str) -> None:
        """Sets the current cs builder to a new instance, constructed with
        the given cross-section name and current snapshot id."""
        if self.__current_snapshot is None:
            raise WrongOrderException("Current snapshot has not been set")
        self.__current_cs_builder = _CrossSectionBuilder(cross_section_name,
                                                         self.__current_snapshot.id,
                                                         cross_section_id,
                                                         self.__global_db)

    def add_b_display(self, b_display: BDisplay) -> None:
        """Sets b-display in the current cross-section builder to desired value."""
        if self.__current_cs_builder is None:
            raise WrongOrderException("Cross section creation has not begun")

        # chained methods that first add the new value
        # and then tries to build the cross-section snapshot

        self.__current_cross_section = (self.__current_cs_builder
                                        .set_b_display(b_display).try_build())

    def begin_lane(self, lane_number: int) -> None:
        """Sets the current lane builder to a new instance, constructed with
        the given lane number and current snapshot id."""
        if self.__current_cross_section is None:
            raise WrongOrderException("Current cross section snapshot has not been set")
        self.__current_lane_builder = _LaneBuilder(lane_number,
                                                   self.__current_cross_section.cs_snapshot_id,
                                                   self.__global_db)

    def add_average_speed(self, speed: float) -> None:
        """Sets average speed in the current lane builder to given value."""
        if self.__current_lane_builder is None:
            raise WrongOrderException("Lane snapshot creation has not begun")
        self.__current_lane = self.__current_lane_builder.set_average_speed(speed).try_build()

    def add_traffic_volume(self, volume: int) -> None:
        """Sets traffic volume in the current lane builder to given value."""
        if self.__current_lane_builder is None:
            raise WrongOrderException("Lane snapshot creation has not begun")
        self.__current_lane = self.__current_lane_builder.set_traffic_volume(volume).try_build()

    def add_a_display(self, a_display: ADisplay) -> None:
        """Sets the a-display in the current lane builder to given value."""
        if self.__current_lane_builder is None:
            raise WrongOrderException("Lane snapshot creation has not begun")
        self.__current_lane = self.__current_lane_builder.set_a_display(a_display).try_build()

    def begin_vehicle(self) -> None:
        """Sets the current vehicle builder to a new instance."""
        if self.__current_lane is None:
            raise WrongOrderException("Current lane snapshot has not been set")
        self.__current_vehicle_builder = _VehicleBuilder(self.__current_lane.id)

    def add_vehicle_type(self, vehicle_type: VehicleType) -> None:
        """Sets the vehicle type in the current vehicle builder to given value."""
        if self.__current_vehicle_builder is None:
            raise WrongOrderException("Vehicle snapshot creation has not begun")
        self.__current_vehicle = self.__current_vehicle_builder.set_vehicle_type(
            vehicle_type).try_build()

    def add_vehicle_speed(self, speed: float) -> None:
        """Sets the vehicle speed in the current vehicle builder to given value."""
        if self.__current_vehicle_builder is None:
            raise WrongOrderException("Vehicle snapshot creation has not begun")
        self.__current_vehicle = self.__current_vehicle_builder.set_vehicle_speed(speed).try_build()

    def end_vehicle(self) -> None:
        """Adds the current vehicle snapshot to current lane snapshot.
        Resets current vehicle and its builder to None.
        Raises WrongOrderException if vehicle snapshot has not been created."""

        if self.__current_vehicle is None or self.__current_lane is None:
            raise WrongOrderException("Vehicle snapshot has not been created")

        self.__current_lane.add_vehicle_snapshot(self.__current_vehicle)
        self.__current_vehicle_builder = None
        self.__current_vehicle = None

    def end_lane(self) -> None:
        """Adds the current lane snapshot to current cross-section snapshot.
        Resets current lane snapshot and its builder to None.
        Raises WrongOrderException if lane snapshot has not been created
         or a vehicle snapshot is in the process of being created ."""

        if (self.__current_lane is None or self.__current_vehicle_builder is not None
                or self.__current_cross_section is None):
            raise WrongOrderException("Lane snapshot creation cannot successfully finish")

        self.__current_cross_section.add_lane_snapshot(self.__current_lane)
        self.__current_lane_builder = None
        self.__current_lane = None

    def end_cross_section(self) -> None:
        """Adds the current cross-section snapshot to current snapshot.
        Resets current cross-section snapshot and its builder to None.
        Raises WrongOrderException if cross-section snapshot has not been created
         or a lane snapshot is in the process of being created ."""

        if (self.__current_cross_section is None or self.__current_lane_builder is not None
                or self.__current_snapshot is None):
            raise WrongOrderException("Cross section snapshot creation cannot successfully finish")

        self.__current_snapshot.add_cross_section_snapshot(self.__current_cross_section)
        self.__current_cs_builder = None
        self.__current_cross_section = None

    def end_snapshot(self) -> None:
        """Adds the current snapshot to current result. Resets current snapshot to None.
        Raises WrongOrderException if snapshot has not been created
         or a cross-section snapshot is in the process of being created ."""

        if (self.__current_snapshot is None or self.__current_cs_builder is not None
                or self.__current_result is None):
            raise WrongOrderException("Snapshot creation cannot successfully finish")

        self.__current_result.add_snapshot(self.__current_snapshot)
        self.__current_snapshot = None

    async def end_result(self) -> Result:
        """Returns current result and resets to None.
         Raises WrongOrderException if result has not been
         created or a snapshot is in the process of being created"""
        if self.__current_result is None or self.__current_snapshot is not None:
            raise WrongOrderException("Result cannot be created")

        result = self.__current_result

        self.__result_manager.register_result(result)

        await self.__global_db.add_result(result.id,
                                          result.result_name,
                                          result.project_name,
                                          result.creation_date_time)

        return result


class WrongOrderException(Exception):
    """Raised when the result builder methods are called in the wrong order"""
    def __init__(self, message: str) -> None:
        self.message = message


class GLibErrorException(Exception):
    """Raised if GLib malfunctions."""
    def __init__(self, message: str) -> None:
        self.message = message
