"""This module contains the DummySimulator class."""
import json

from gi.repository import GObject, Gio

from sbaid.model.simulator.dummy.dummy_cross_section import DummyCrossSection
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.location import Location
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class DummySimulator(Simulator):
    """TODO"""


    _sequence: dict[int, Input]
    _pointer: int

    type = GObject.Property(type=SimulatorType)
    cross_section = Gio.ListStore.new(DummyCrossSection)

    def __init__(self) -> None:
        """TODO"""
        super().__init__(type=SimulatorType("dummy.json", "CSV Dummy"),
                         cross_sections=Gio.ListStore.new(DummyCrossSection))
        self._sequence = {}
        self._pointer = 0


    async def load_file(self, file: Gio.File) -> None:
        """TODO"""
        with open(str(file.get_path()), 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            for i, timestamp in enumerate(data["vehicle_infos"]):
                current_input = Input()
                for cs in data["vehicle_infos"][timestamp]:
                    max_lanes = 0
                    for lane in data["vehicle_infos"][timestamp][cs]:
                        for i in enumerate(data["vehicle_infos"][timestamp][cs][lane]):
                            veh_type = data["vehicle_infos"][timestamp][cs][lane][i[0]]["type"]
                            veh_speed = data["vehicle_infos"][timestamp][cs][lane][i[0]]["speed"]
                            current_input.add_vehicle_info(cs, int(lane), veh_type, veh_speed)
                        max_lanes = max(max_lanes, int(lane))
                    if i == 0:
                        self.cross_sections.append(DummyCrossSection(cs, CrossSectionType.MEASURING,
                                                                  Location(0, 0), max_lanes,
                                                                  False, False, False))
                self._sequence[int(timestamp)] = current_input

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """TODO"""
        return -1

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    async def move_cross_section(self, cross_section_id: str, new_position: Location) -> None:
        """TODO"""

    async def init_simulation(self) -> tuple[int, int]:
        return 0, len(self._sequence)

    async def continue_simulation(self, span: int) -> None:
        """TODO"""
        self._pointer = self._pointer + span

    async def measure(self) -> Input:
        return self._sequence.get(self._pointer)

    async def set_display(self, display: Display) -> None:
        """TODO"""

    async def stop_simulation(self) -> None:
        """TODO"""
        self._pointer = 0
