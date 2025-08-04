# pylint: disable=too-many-locals
"""This module contains the DummySimulator class."""
import json
import aiofiles

from jsonschema import validate, ValidationError

from gi.repository import GLib, Gio

from sbaid.model.simulator.dummy.dummy_cross_section import DummyCrossSection
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.location import Location
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType


class JSONExeption(Exception):
    """This exception is raised when a JSON file does not match the required format
    for a dummy simulator."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class EndOfSimulationException(Exception):
    """This exception is raised when the simulation is tried to be run beyond its run time."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotSupportedException(Exception):
    """This exception is raised when a method is called
    that is not supported by this simulator implementation."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DummySimulator(Simulator):
    """This class implements the DummySimulator class using a JSON file for Input measurements."""

    _sequence: dict[int, Input]
    _pointer: int
    _type: SimulatorType
    _route: Gio.ListModel
    _cross_sections: Gio.ListModel
    _simulation_start_time: int
    _simulation_end_time: int
    _schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "cross_section_locations": {
                "type": "object",
                "patternProperties": {
                    "^cs[\\w\\d_]+$": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"}
                        },
                        "required": ["x", "y"],
                        "additionalProperties": False
                    }
                }
            },
            "vehicle_infos": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "object",
                        "patternProperties": {
                            "^cs[\\w\\d_]+$": {
                                "type": "object",
                                "patternProperties": {
                                    "^[0-9]+$": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": {"type": "integer"},
                                                "speed": {"type": "number"}
                                            },
                                            "required": ["type", "speed"],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "additionalProperties": False
                            }
                        },
                        "additionalProperties": False
                    }
                },
                "additionalProperties": False
            }
        },
        "required": ["cross_section_locations", "vehicle_infos"],
        "additionalProperties": False
    }

    def get_type(self) -> SimulatorType:
        """Property definition for the simulator type."""
        return self._type

    def get_route(self) -> Gio.ListModel:
        """TODO"""
        return self._route

    def get_cross_sections(self) -> Gio.ListModel:
        """Property definition for the simulator cross section list model."""
        return self._cross_sections

    def __init__(self) -> None:
        """Create a new dummy simulator."""
        super().__init__()
        self._cross_sections = Gio.ListStore.new(DummyCrossSection)
        self._type = SimulatorType("dummy_json", "JSON Dummy Simulator")
        self._sequence = {}
        self._pointer = 0
        self._simulation_start_time = 0
        self._simulation_end_time = 0

    async def load_file(self, file: Gio.File) -> None:
        """Loads a new file that is used to create simulator cross sections and the deterministic
        sequence of input measurements."""
        async with aiofiles.open(str(file.get_path()), 'r', encoding="utf-8") as json_file:
            if self._pointer != 0:
                raise RuntimeError("Cannot open new file during simulation")
            data = json.loads(await json_file.read())
            try:
                validate(instance=data, schema=self._schema)
            except ValidationError as e:
                raise JSONExeption(e.message) from e

            cs_location_map = {}
            for cross_section in data['cross_section_locations']:
                location_x = data['cross_section_locations'].get(cross_section)['x']
                location_y = data['cross_section_locations'].get(cross_section)['y']
                cs_location_map[cross_section] = Location(location_x, location_y)

            for snapshot_time, snapshot in data["vehicle_infos"].items():
                current_input = Input()
                for cross_section, lanes in snapshot.items():
                    max_lanes = 0
                    for lane_id, vehicles in lanes.items():
                        for vehicle in vehicles:
                            vehicle_type = vehicle["type"]
                            current_input.add_vehicle_info(str(cross_section), int(lane_id),
                                                           vehicle_type, float(vehicle["speed"]))
                        max_lanes = max(max_lanes, int(lane_id))
                    self._cross_sections.append(DummyCrossSection(cross_section, cross_section,
                                                                 CrossSectionType.COMBINED,
                                                                 cs_location_map[cross_section],
                                                                 max_lanes, False))
                self._sequence[int(snapshot_time)] = current_input

        self._simulation_start_time = min(self._sequence.keys())
        self._simulation_end_time = max(self._sequence.keys())

        route = Gio.ListStore.new(Location)

        for location in cs_location_map.values():
            route.append(location)

        self._route = route

    async def create_cross_section(self, location: Location,
                                   cross_section_type: CrossSectionType) -> int:
        """Has no effect. Raises an exception."""
        raise NotSupportedException("The dummy simulator does not support creating"
                                    "new cross sections.")

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Has no effect. Raises an exception."""
        raise NotSupportedException("The dummy simulator does not support removing cross sections.")

    async def move_cross_section(self, cross_section_id: str, new_location: Location) -> None:
        """Has no effect. Raises an exception."""
        raise NotSupportedException("The dummy simulator does not support moving cross sections.")

    async def init_simulation(self) -> tuple[GLib.DateTime, int]:
        """Initialize the simulator. Always returns 0 as the starting point
        and the amount of input measurements as the simulation length."""
        self._pointer = 0
        return GLib.DateTime.new_now_local(), self._simulation_end_time

    async def continue_simulation(self, span: int) -> None:
        """Set the measuring pointer to the given location in the measurements."""
        if (self._pointer + span) <= self._simulation_end_time:
            self._pointer = self._pointer + span
        else:
            raise EndOfSimulationException(f"The simulation cannot be continued {span} steps.")

    async def measure(self) -> Input:
        """Return the current input of the simulator.
        If there is no measurement given at the current time,
        the nearest neighbouring measurement is returned."""
        if not self._sequence:
            raise FileNotFoundError("No simulator file has been loaded.")
        if not self._sequence.keys().__contains__(self._pointer):
            nearest = min(self._sequence.keys(), key=lambda x: abs(x - self._pointer))
            return self._sequence[nearest]
        return self._sequence[self._pointer]

    async def set_display(self, display: Display) -> None:
        """Has no effect."""

    async def stop_simulation(self) -> None:
        """Resets the simulator to its initial state."""
        self._pointer = 0
