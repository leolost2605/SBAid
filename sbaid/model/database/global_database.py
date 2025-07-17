"""TODO"""
from abc import ABC, abstractmethod

from gi.repository.GLib import DateTime
from gi.repository.Gio import File

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType


class GlobalDatabase(ABC):
    """TODO"""

    @abstractmethod
    async def open(self, file: File) -> None:
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
    async def get_all_results(self) -> list[tuple[str, DateTime]]:
        """TODO"""

    @abstractmethod
    async def save_result(self, result_id: str, project_name: str, creation_date_time: DateTime) -> None:
        """TODO"""

    @abstractmethod
    async def delete_result(self, result_id: str) -> None:
        """TODO"""

    @abstractmethod
    async def get_result_name(self, result_id: str) -> str:
        """TODO"""

    @abstractmethod
    async def get_all_tags(self) -> list[str]:
        """TODO"""

    @abstractmethod
    async def get_result_tags(self, result_id: str) -> list[str]:
        """TODO"""

    @abstractmethod
    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, DateTime]]:
        """TODO"""

    @abstractmethod
    async def save_snapshot(self, result_id: str, snapshot_id: str, time: DateTime) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_cross_section_snapshots(self, snapshot_id: str) -> list[tuple[str, str, BDisplay]]:
        """TODO"""

    @abstractmethod
    async def save_cross_section_snapshot(self, snapshot_id: str, cross_section_snapshot_ic: str,
                                    time: DateTime) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str)\
            -> list[tuple[str, int, float, int, ADisplay]]:
        """TODO"""

    @abstractmethod
    async def save_lane_snapshot(self, cross_section_snapshot_id: str, lane_snapshot_id: str,
                           lane: int, average_speed: float, traffic_volume: int,
                           a_display: ADisplay) -> None:
        """TODO"""

    @abstractmethod
    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str) -> list[tuple[VehicleType, float]]:
        """TODO"""

    @abstractmethod
    async def save_vehicle_snapshot(self, lane_snapshot_id: str,
                              vehicle_type: VehicleType, speed: float) -> None:
        """TODO"""
