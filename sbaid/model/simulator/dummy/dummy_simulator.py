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
    """This class implements the DummySimulator class using a JSON file for Input measurements."""

    _sequence: dict[int, Input]
    _pointer: int

    type = GObject.Property(type=SimulatorType)
    cross_section = Gio.ListStore.new(DummyCrossSection)

    def __init__(self) -> None:
        """Create a new dummy simulator."""
        super().__init__(type=SimulatorType("dummy.json", "CSV Dummy"),
                         cross_sections=Gio.ListStore.new(DummyCrossSection))
        self._sequence = {}
        self._pointer = 0

    async def load_file(self, file: Gio.File) -> None:
        """Loads a new file that is used to create simulator cross sections and the deterministic
        sequence of input measurements."""
        with open(str(file.get_path()), 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            for i, timestamp in enumerate(data["vehicle_infos"]):
                current_input = Input()
                for cs in data["vehicle_infos"][timestamp]:
                    max_lanes = 0
                    for lane in data["vehicle_infos"][timestamp][cs]:
                        for data in data["vehicle_infos"][timestamp][cs][lane]:
                            veh_type = data["vehicle_infos"][timestamp][cs][lane][data[0]]["type"]
                            veh_speed = data["vehicle_infos"][timestamp][cs][lane][data[0]]["speed"]
                            current_input.add_vehicle_info(cs, int(lane), veh_type, veh_speed)
                        max_lanes = max(max_lanes, int(lane))
                    if i == 0:
                        self.cross_sections.append(DummyCrossSection(cs, CrossSectionType.MEASURING,
                                                                     Location(0, 0), max_lanes,
                                                                     False, False, False))
                self._sequence[int(timestamp)] = current_input

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """Has no effect. Returns -1 as there is no  position of the new cross section."""
        return -1

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Has no effect."""

    async def move_cross_section(self, cross_section_id: str, new_position: Location) -> None:
        """Has no effect."""

    async def init_simulation(self) -> tuple[int, int]:
        """Initialize the simulator. Always returns 0 as the starting point
        and the amount of input measurements as the simulation length."""
        return 0, len(self._sequence)

    async def continue_simulation(self, span: int) -> None:
        """Set the measuring pointer to the next position in the measurements."""
        self._pointer = self._pointer + span

    async def measure(self) -> Input:
        """Return the current input of the simulator."""
        return self._sequence.get(self._pointer)

    async def set_display(self, display: Display) -> None:
        """Has no effect."""

    async def stop_simulation(self) -> None:
        """Resets the simulator to its initial state."""
        self._pointer = 0
