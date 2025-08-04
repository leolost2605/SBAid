"""This module contains the GlobalDatabase interface."""
from abc import ABC, abstractmethod

from gi.repository import GLib

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType


class GlobalDatabase(ABC):
    """This interface provides methods that ecapsule
    the global database functionality."""

    @abstractmethod
    async def add_project(self, project_id: str, simulator_type: SimulatorType,
                          simulator_file_path: str, project_file_path: str) -> None:
        """Add a project to the database."""

    @abstractmethod
    async def get_all_projects(self) -> list[tuple[str, SimulatorType, str, str,]]:
        """Return meta-information about all projects in the database."""

    @abstractmethod
    async def remove_project(self, project_id: str) -> None:
        """Remove a project from the database."""

    @abstractmethod
    async def get_all_results(self) -> list[tuple[str, str, str, GLib.DateTime]]:
        """Return all results in the database."""

    @abstractmethod
    async def add_result(self, result_id: str, result_name: str, project_name: str,
                         creation_date_time: GLib.DateTime) -> None:
        """Add a result to the database."""

    @abstractmethod
    async def delete_result(self, result_id: str) -> None:
        """Remove a result and all sub-results from the database."""

    @abstractmethod
    async def get_result_name(self, result_id: str) -> str:
        """Return the name of the given result_id from the database."""

    @abstractmethod
    async def add_tag(self, tag_id: str, tag_name: str) -> None:
        """Add a tag to the database."""

    @abstractmethod
    async def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the database."""

    @abstractmethod
    async def get_tag_name(self, tag_id: str) -> str:
        """Return the name of the given tag_id."""

    @abstractmethod
    async def add_result_tag(self, result_tag_id: str, result_id: str, tag_id: str) -> None:
        """Add a tag to a result."""

    @abstractmethod
    async def get_all_tags(self) -> list[tuple[str, str]]:
        """Return all tags in the database."""

    @abstractmethod
    async def get_result_tag_ids(self, result_id: str) -> list[str]:
        """Return all tags that belong to the given result."""

    @abstractmethod
    async def get_all_snapshots(self, result_id: str) -> list[tuple[str, GLib.DateTime]]:
        """Return all snapshots from a given result."""

    @abstractmethod
    async def add_snapshot(self, snapshot_id: str, result_id: str, time: GLib.DateTime) -> None:
        """Add a snapshot to a given result."""

    @abstractmethod
    async def get_all_cross_section_snapshots(self, snapshot_id: str)\
            -> list[tuple[str, str, BDisplay]]:
        """Return all cross section snapshots from a given snapshot."""

    @abstractmethod
    async def add_cross_section_snapshot(self, cross_section_snapshot_id: str,
                                         snapshot_id: str,
                                         cross_section_name: str,
                                         b_display: BDisplay) -> None:
        """Add a cross section snapshot to a given snapshot."""

    @abstractmethod
    async def get_all_lane_snapshots(self, cross_section_snapshot_id: str)\
            -> list[tuple[str, int, float, int, ADisplay]]:
        """Return all lane snapshots from a given cross section snapshot."""

    @abstractmethod
    async def add_lane_snapshot(self, lane_snapshot_id: str, cross_section_snapshot_id: str,
                                lane: int, average_speed: float, traffic_volume: int,
                                a_display: ADisplay) -> None:
        """Add a lane snapshot to a given cross section snapshot."""

    @abstractmethod
    async def get_all_vehicle_snapshots(self, lane_snapshot_id: str)\
            -> list[tuple[VehicleType, float]]:
        """Return all vehicle snapshots from a given lane snapshot."""

    @abstractmethod
    async def add_vehicle_snapshot(self, lane_snapshot_id: str,
                                   vehicle_type: VehicleType, speed: float) -> None:
        """Add a venicle snapshot to a given lane snapshot."""
