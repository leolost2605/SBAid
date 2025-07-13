"""todo"""

from gi.repository import GLib
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.results.result_manager import ResultManager
from sbaid.common.b_display import BDisplay
from sbaid.model.results.result import Result


class ResultBuilder:
    """todo"""

    def __init__(self, result_manager: ResultManager) -> None:
        """todo"""

    def begin_result(self, project_name: str) -> None:
        """todo"""

    def begin_snapshot(self, simulation_timestamp: GLib.DateTime) -> None:
        """todo"""

    def begin_cross_section(self, cross_section_name: str) -> None:
        """todo"""

    def add_b_display(self, b_display: BDisplay) -> None:
        """todo"""

    def begin_lane(self, lane_number: int) -> None:
        """todo"""

    def add_average_speed(self, speed: float) -> None:
        """todo"""

    def add_traffic_volume(self, volume: int) -> None:
        """todo"""

    def add_a_display(self, a_display: ADisplay) -> None:
        """todo"""

    def begin_vehicle(self) -> None:
        """todo"""

    def add_vehicle_type(self, vehicle_type: VehicleType) -> None:
        """todo"""

    def add_vehicle_speed(self, speed: float) -> None:
        """todo"""

    def end_vehicle(self) -> None:
        """todo"""

    def end_lane(self) -> None:
        """todo"""

    def end_cross_section(self) -> None:
        """todo"""

    def end_snapshot(self) -> None:
        """todo"""

    def end_result(self) -> Result:
        """todo"""
