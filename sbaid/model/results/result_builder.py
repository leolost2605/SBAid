"""This module defines the ResultBuilder class and its helper classes"""
from typing import Self
from gi.repository import GLib, GObject
from numpy.f2py.auxfuncs import throw_error
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
    """todo"""
    # required
    __cross_section_name: str
    __snapshot_id: str
    __global_db: GlobalDatabase

    # added later
    __cross_section_b_display: BDisplay

    def __init__(self, cross_section_name: str, snapshot_id: str, global_db: GlobalDatabase) -> None:
        self.__cross_section_name = cross_section_name
        self.__snapshot_id = snapshot_id
        self.__global_db = global_db


    def set_b_display(self, b_display: BDisplay) -> Self:
        self.__cross_section_b_display = b_display

    def try_build(self) -> CrossSectionSnapshot | None:
        if self.__cross_section_b_display is not None:
            return CrossSectionSnapshot(self.__snapshot_id, GLib.uuid_string_random(),
                                    self.__cross_section_name,
                                    self.__cross_section_b_display, self.__global_db)
        return None

class _LaneBuilder:
    # required
    __lane_number: int
    __cross_section_id: str
    __global_db: GlobalDatabase
    # added later
    __average_speed: float
    __traffic_volume: int
    __a_display: ADisplay

    def __init__(self, lane_number: int, cross_section_id: str, global_db: GlobalDatabase) -> None:
        self.__lane_number = lane_number
        self.__cross_section_id = cross_section_id
        self.__global_db = global_db

    def set_average_speed(self, average_speed: float) -> Self:
        self.__average_speed = average_speed
        return self

    def set_traffic_volume(self, traffic_volume: int) -> Self:
        self.__traffic_volume = traffic_volume
        return self

    def set_a_display(self, a_display: ADisplay) -> Self:
        self.__a_display = a_display
        return self

    def try_build(self) -> LaneSnapshot | None:
        """todo"""
        if (self.__average_speed is not None) and (self.__average_speed is not None) and (
                self.__traffic_volume is not None) and (self.__a_display is not None):
            return LaneSnapshot(self.__cross_section_id,
                                GLib.uuid_string_random(),
                                self.__lane_number,
                                self.__average_speed,
                                self.__traffic_volume,
                                self.__a_display,
                                self.__global_db)
        return None


class VehicleBuilder:
    __current_vehicle_type: VehicleType | None
    __current_vehicle_speed: float | None

class ResultBuilder(GObject.GObject):
    """Contains methods to build the results"""
    __result_manager: ResultManager
    __global_db: GlobalDatabase
    __began_result_at: GLib.DateTime | None = None

    __result_scope: bool
    __snapshot_scope: bool
    __cross_section_scope: bool
    __lane_scope: bool
    __vehicle_scope: bool

    __current_result: Result
    # self, snapshot_id: str, capture_timestamp: GLib.DateTime, global_db: GlobalDatabase
    __current_snapshot: Snapshot | None

    # snapshot_id: str, cross_section_snapshot_id: str, cross_section_name: str,  b_display: BDisplay, global_db: GlobalDatabase
    __current_cross_section: CrossSectionSnapshot | None
    __current_cs_builder: _CrossSectionBuilder | None

    __current_lane: LaneSnapshot | None
    __current_lane_builder: _LaneBuilder | None

    __current_vehicle: VehicleSnapshot | None


    def __init__(self, result_manager: ResultManager, global_db: GlobalDatabase) -> None:
        """todo"""
        self.result_manager = result_manager
        self.__global_db = global_db
        __result_scope = False
        __snapshot_scope = False
        __cross_section_scope = False
        __lane_scope = False
        __vehicle_scope = False

    def begin_result(self, project_name: str) -> None:
        """todo"""
        now = GLib.DateTime.new_now_local()
        self.__began_result_at = now
        self.__current_result = Result(GLib.uuid_string_random(), project_name, now, self.__global_db)
        self.__result_scope = True

    def begin_snapshot(self, simulation_timestamp: GLib.DateTime) -> None:
        """todo"""
        self.__current_snapshot = Snapshot(GLib.uuid_string_random(), simulation_timestamp, self.__global_db)
        self.__snapshot_scope = True

    def begin_cross_section(self, cross_section_name: str) -> None:
        """todo"""
        if not self.__snapshot_scope:
            throw_error(f"Scope is False")
        self.__current_cs_builder = _CrossSectionBuilder(cross_section_name, self.__current_snapshot.id, self.__global_db)
        self.__cross_section_scope = True

    def add_b_display(self, b_display: BDisplay) -> None:
        """todo"""
        self.__current_cross_section = self.__current_cs_builder.set_b_display(
            b_display).try_build()

    def begin_lane(self, lane_number: int) -> None:
        """todo"""
        self.__current_lane_builder = _LaneBuilder(lane_number, self.__current_cross_section.cross_section_snapshot_id, self.__global_db)
        self.__lane_scope = True

    def add_average_speed(self, speed: float) -> None:
        """todo"""
        self.__current_lane = self.__current_lane_builder.set_average_speed(speed).try_build()

    def add_traffic_volume(self, volume: int) -> None:
        """todo"""
        self.__lane_traffic_volume = volume
        self.__try_create_lane()

    def add_a_display(self, a_display: ADisplay) -> None:
        """todo"""
        self.__lane_a_display = a_display
        self.__try_create_lane()

    def begin_vehicle(self) -> None:
        """todo"""
        self.__vehicle_scope = True

    def add_vehicle_type(self, vehicle_type: VehicleType) -> None:
        """todo"""
        self.__current_vehicle_type = vehicle_type
        self.__try_create_vehicle()

    def add_vehicle_speed(self, speed: float) -> None:
        """todo"""
        self.__current_vehicle_speed = speed
        self.__try_create_vehicle()

    def end_vehicle(self) -> None:
        """todo"""
        self.__current_lane.add_vehicle_snapshot(self.__current_vehicle)
        self.__reset_vehicle_values()

    def end_lane(self) -> None:
        """todo"""
        self.__current_cross_section.add_lane_snapshot(self.__current_lane)
        self.__reset_lane_values()

    def end_cross_section(self) -> None:
        """todo"""
        self.__current_snapshot.add_cross_section_snapshot(self.__current_cross_section)
        self.__current_cs_builder = None

    def end_snapshot(self) -> None:
        """todo"""
        self.__current_result.add_snapshot(self.__current_snapshot)

    def end_result(self) -> Result:
        """todo"""
        return self.__current_result


    # helper methods
    def __create_cs_if_available(self) -> None:
        """todo"""
        if (self.__cross_section_b_display is not None) and (self.__cross_section_name is not None):
            self.__current_cross_section = CrossSectionSnapshot(self.__current_snapshot.id,
                                                                GLib.uuid_string_random(),
                                                                self.__cross_section_name,
                                                                self.__cross_section_b_display,
                                                                self.__global_db)

    def __try_create_lane(self) -> None:
        """todo"""
        if self.__lane_information_complete():
            self.__current_lane = LaneSnapshot(self.__current_cross_section.cross_section_snapshot_id,
                                               GLib.uuid_string_random(),
                                               self.__lane_number,
                                               self.__lane_average_speed,
                                               self.__lane_traffic_volume,
                                               self.__lane_a_display,
                                               self.__global_db)

    def __lane_information_complete(self) -> bool:
        return (self.__lane_number is not None) and (self.__lane_average_speed is not None) and (self.__lane_traffic_volume is not None) and (self.__lane_a_display is not None)

    def __try_create_vehicle(self):
        """todo"""
        if self.__current_vehicle_type is not None and self.__current_vehicle_speed is not None:
            self.__current_vehicle = VehicleSnapshot(self.__current_lane.id, self.__current_vehicle_type, self.__current_vehicle_speed)


