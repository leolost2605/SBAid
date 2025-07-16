"""This module contains the Input class."""
from typing import Optional, List
from gi.repository import GObject
from sbaid.model.simulation.vehicle_info import VehicleInfo
from sbaid.common.vehicle_type import VehicleType


class Input(GObject.GObject):
    """This class stores information about the state of the traffic within the simulation.
    It is possible to access the information directly but also derive secondary attributes."""
    _all_vehicle_infos: dict[str, dict[int, list[VehicleInfo]]] = {}

    def __init__(self) -> None:
        """Construct a new Input."""
        super().__init__()
        self._all_vehicle_infos: dict[str, dict[int, list[VehicleInfo]]] = {}

    def get_average_speed(self, cross_section_id: str, lane_number: int) -> Optional[float]:
        """Return the average speed of all vehicles at the given cross-section and lane."""
        if len(self._all_vehicle_infos.get(cross_section_id, {}).get(lane_number, [])) == 0:
            return None
        all_speeds_sum: float = 0.0
        for vehicle_info in self._all_vehicle_infos.get(cross_section_id, {}).get(lane_number, []):
            all_speeds_sum += vehicle_info.speed
        result: float = (all_speeds_sum
                         / float(len(self._all_vehicle_infos
                                     .get(cross_section_id, {}).get(lane_number, []))))
        return result

    def get_traffic_volume(self, cross_section_id: str, lane_number: int) -> Optional[int]:
        """Return the amount of vehicles at the given cross-section and lane.
        Return None if there is no vehicle."""
        volume: int = len(self._all_vehicle_infos.get(cross_section_id, {})
                          .get(lane_number, {}))
        if volume == 0:
            return None
        return volume

    def get_all_vehicle_infos(self, cross_section_id: str, lane_number: int) -> List[VehicleInfo]:
        """Return a list of all vehicle information at the given cross-section and lane."""
        return self._all_vehicle_infos.get(cross_section_id, {}).get(lane_number, []).copy()

    def add_vehicle_info(self, cross_section_id: str, lane_number: int, vehicle_type: VehicleType,
                         speed: float) -> None:
        """Add a new vehicle information to the given cross-section and lane."""
        if self._all_vehicle_infos.get(cross_section_id) is None:
            self._all_vehicle_infos[cross_section_id] = {}
        if self._all_vehicle_infos.get(cross_section_id, {}).get(lane_number) is None:
            self._all_vehicle_infos[cross_section_id][lane_number] = []
        (self._all_vehicle_infos.get(cross_section_id, {}).get(lane_number, [])
         .append(VehicleInfo(vehicle_type, speed)))
