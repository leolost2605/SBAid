"""TODO"""
from abc import ABC, abstractmethod

from gi.repository import GLib, Gio

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType


class GlobalDatabase(ABC):
    """TODO"""

    @abstractmethod
    async def open(self, file: Gio.File) -> None:
        """TODO"""

    @abstractmethod
    async def add_project(self, project_id: str, simulator_type: SimulatorType,
                          simulator_file_path: str, project_file_path: str) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_projects(self) -> list[tuple[str, SimulatorType, str, str,]]:
        """TODO"""

    @abstractmethod
    async def remove_project(self, project_id: str) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_results(self) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""

    @abstractmethod
    async def add_result(self, result_id: str, result_name: str, project_name: str,
                         creation_date_time: GLib.DateTime) -> None:
        """TODO"""

    @abstractmethod
    async def delete_result(self, result_id: str) -> None:
        """TODO"""

    @abstractmethod
    async def get_result_name(self, result_id: str) -> str:
        """TODO"""

    @abstractmethod
    async def add_result_tag(self, result_tag_id: str, result_id: str,
                             tag_id: str, tag_name: str) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_tags(self) -> list[tuple[str, str]]:
        """TODO"""

    @abstractmethod
    async def get_result_tags(self, result_id: str) -> list[str]:
        """TODO"""

    @abstractmethod
    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, GLib.DateTime]]:
        """TODO"""

    @abstractmethod
    async def add_snapshot(self, snapshot_id: str, result_id: str, time: GLib.DateTime) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_cross_section_snapshots(self, snapshot_id: str)\
            -> list[tuple[str, str, BDisplay]]:
        """TODO"""

    @abstractmethod
    async def add_cross_section_snapshot(self, cross_section_snapshot_id: str,
                                         snapshot_id: str,
                                         cross_section_name: str,
                                         b_display: BDisplay) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str)\
            -> list[tuple[str, int, float, int, ADisplay]]:
        """TODO"""

    @abstractmethod
    async def add_lane_snapshot(self, lane_snapshot_id: str, cross_section_snapshot_id: str,
                                lane: int, average_speed: float, traffic_volume: int,
                                a_display: ADisplay) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str)\
            -> list[tuple[VehicleType, float]]:
        """TODO"""

    @abstractmethod
    async def add_vehicle_snapshot(self, lane_snapshot_id: str,
                                   vehicle_type: VehicleType, speed: float) -> None:
        """TODO"""
