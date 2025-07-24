"""This module contains the DummySimulator class."""
import json
from jsonschema import validate, ValidationError

from gi.repository import GObject, Gio

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


class DummySimulator(Simulator):
    """This class implements the DummySimulator class using a JSON file for Input measurements."""

    _sequence: dict[int, Input]
    _pointer: int
    _type: SimulatorType
    _cross_sections: Gio.ListModel
    _schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "vehicle_infos": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "object",
                        "properties": {
                            "cs1": {
                                "$ref": "#/$defs/csData"
                            },
                            "cs2": {
                                "$ref": "#/$defs/csData"
                            }
                        },
                        "required": ["cs1", "cs2"],
                        "additionalProperties": False
                    }
                },
                "additionalProperties": False
            }
        },
        "required": ["vehicle_infos"],
        "additionalProperties": False,
        "$defs": {
            "csData": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "integer"
                                },
                                "speed": {
                                    "type": "number"
                                }
                            },
                            "required": ["type", "speed"],
                            "additionalProperties": False
                        }
                    }
                },
                "additionalProperties": False
            }
        }
    }

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """Property definition for the simulator type."""
        return self._type

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """Property definition for the simulator cross section list model."""
        return self._cross_sections

    def __init__(self) -> None:
        """Create a new dummy simulator."""
        super().__init__()
        self._cross_sections = Gio.ListStore.new(DummyCrossSection)
        self._type = SimulatorType("dummy_json", "JSON Dummy Simulator")
        self._sequence = {}
        self._pointer = 0

    async def load_file(self, file: Gio.File) -> None:
        """Loads a new file that is used to create simulator cross sections and the deterministic
        sequence of input measurements."""
        with open(str(file.get_path()), 'r', encoding="utf-8") as json_file:
            if self._pointer != 0:
                raise RuntimeError("Cannot open new file during simulation")
            data = json.load(json_file)
            try:
                validate(instance=data, schema=self._schema)
            except ValidationError as e:
                raise JSONExeption(e.message) from e

            for snapshot_id, snapshot in data["vehicle_infos"].items():
                current_input = Input()
                for cross_section, lanes in snapshot.items():
                    max_lanes = 0
                    for lane_id, vehicles in lanes.items():
                        for vehicle in vehicles:
                            vehicle_type = vehicle["type"]
                            current_input.add_vehicle_info(str(cross_section), int(lane_id),
                                                           vehicle_type, float(vehicle["speed"]))
                        max_lanes = max(max_lanes, int(lane_id))
                    self.cross_sections.append(DummyCrossSection(cross_section,
                                                                 CrossSectionType.MEASURING,
                                                                 Location(0, 0), max_lanes,
                                                                 False, False, False))
                self._sequence[int(snapshot_id)] = current_input

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
        self._pointer = 0
        return 0, len(self._sequence)

    async def continue_simulation(self, span: int) -> None:
        """Set the measuring pointer to the next position in the measurements."""
        if (self._pointer + span) < len(self._sequence):
            self._pointer = self._pointer + span
        else:
            raise EndOfSimulationException(f"The simulation cannot be continued {span} steps.")

    async def measure(self) -> Input:
        """Return the current input of the simulator."""
        if not self._sequence:
            raise FileNotFoundError("No simulator file has been loaded.")
        return self._sequence.get(self._pointer)

    async def set_display(self, display: Display) -> None:
        """Has no effect."""

    async def stop_simulation(self) -> None:
        """Resets the simulator to its initial state."""
        self._sequence = {}
        self._pointer = 0
