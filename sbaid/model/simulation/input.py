"""This module contains the Input class."""
from typing import Optional, List
from gi.repository import GObject
from sbaid.model.simulation.vehicle_info import VehicleInfo
from sbaid.common.vehicle_type import VehicleType


class Input(GObject.GObject):
    """This class stores information about the state of the traffic within the simulation.
    It is possible to access the information directly but also derive secondary attributes."""
    _all_vehicle_infos: dict[str, dict[int, list[VehicleInfo]]]
    _average_speeds: dict[str, dict[int, float]]
    _traffic_volumes: dict[str, dict[int, int]]

    def __init__(self) -> None:
        """Construct a new Input."""
        super().__init__()
        self._all_vehicle_infos: dict[str, dict[int, list[VehicleInfo]]] = {}
        self._average_speeds = {}
        self._traffic_volumes = {}

    def get_average_speed(self, cross_section_id: str, lane_number: int) -> Optional[float]:
        """Return the average speed of all vehicles at the given cross-section and lane."""
        if not self._all_vehicle_infos:
            if (cross_section_id in self._average_speeds
                    and lane_number in self._average_speeds[cross_section_id]):
                return self._average_speeds[cross_section_id][lane_number]

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
        if not self._all_vehicle_infos:
            if (cross_section_id in self._traffic_volumes
                    and lane_number in self._traffic_volumes[cross_section_id]):
                return self._traffic_volumes[cross_section_id][lane_number]

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

    def add_lane_info(self, cross_section_id: str, lane_number: int,
                      avg_speed: float, volume: int):
        """If the simulator only supports average values and not separate vehicles use this
        instead of add_vehicle_info."""
        if cross_section_id not in self._average_speeds:
            self._average_speeds[cross_section_id] = {}

        if cross_section_id not in self._traffic_volumes:
            self._traffic_volumes[cross_section_id] = {}

        self._average_speeds[cross_section_id][lane_number] = avg_speed
        self._traffic_volumes[cross_section_id][lane_number] = volume
