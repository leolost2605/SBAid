from gi.repository import GObject
from typing import Optional, List
from sbaid.model.simulation.vehicle_info import VehicleInfo
from sbaid.common.vehicle_type import VehicleType


class Input(GObject.GObject):
    """TODO"""

    def get_average_speed(self, cross_section_id: str, lane_number: int) -> Optional[float]:
        """TODO"""

    def get_traffic_volume(self, cross_section_id: str, lane_number: int) -> Optional[float]:
        """TODO"""

    def get_all_vehicle_infos(self, cross_section_id: str, lane_number: int) -> List[VehicleInfo]:
        """TODO"""
        return []

    def add_vehicle_info(self, cross_section_id: str, lane_number: int, vehicle_type: VehicleType,
                         speed: float) -> None:
        """TODO"""
