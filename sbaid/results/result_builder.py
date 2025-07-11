from xmlrpc.client import DateTime
from sbaid.common.a_display import ADisplay
from sbaid.common.vehicle_type import VehicleType
from sbaid.results.result_manager import ResultManager
from sbaid.common.b_display import BDisplay
"""todo"""

class ResultBuilder:
    """todo"""

    def __init__(self, result_manager: ResultManager) -> None:
        """todo"""
        pass

    def begin_result(self, project_name: str) -> None:
        """todo"""
        pass

    def begin_snapshot(self, simulation_timestamp: DateTime) -> None:
        """todo"""
        pass

    def begin_cross_section(self, cross_section_name: str) -> None:
        """todo"""
        pass

    def add_b_display(self, b_display: BDisplay) -> None:
        """todo"""
        pass

    def begin_lane(self, lane_number: int) -> None:
        """todo"""
        pass

    def add_average_speed(self, speed: float) -> None:
        """todo"""
        pass

    def add_traffic_volume(self, volume: int) -> None:
        """todo"""
        pass

    def add_a_display(self, a_display: ADisplay) -> None:
        """todo"""
        pass

    def begin_vehicle(self) -> None:
        """todo"""
        pass

    def add_vehicle_type(self, type: VehicleType) -> None:
        """todo"""
        pass

    def add_vehicle_speed(self, speed: float) -> None:
        """todo"""
        pass

    def end_vehicle(self) -> None:
        """todo"""
        pass

    def end_lane(self) -> None:
        """todo"""
        pass

    def end_cross_section(self) -> None:
        """todo"""
        pass

    def end_snapshot(self) -> None:
        """todo"""
        pass

    def end_result(self) -> None:
        """todo"""
        pass
