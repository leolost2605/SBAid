"""This module contains the DummyCrossSection class."""
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummyCrossSection(SimulatorCrossSection):
    """This class represents the dummy simulator cross section."""
    _id: str
    _name: str
    _type: CrossSectionType
    _location: Location
    _lanes: int
    _hard_shoulder_available: bool

    def get_id(self) -> str:
        """Getter for the id."""
        return self._id

    def get_name(self) -> str:
        """Getter for the name."""
        return self._name

    def get_type(self) -> CrossSectionType:
        """Getter for the type."""
        return self._type

    def get_location(self) -> Location:
        """Getter for the location."""
        return self._location

    def get_lanes(self) -> int:
        """Getter for the lanes."""
        return self._lanes

    def get_hard_shoulder_available(self) -> bool:
        """Getter for the hard shoulder available boolean."""
        return self._hard_shoulder_available

    def __init__(self, cs_id: str, name: str, cs_type: CrossSectionType, location: Location,
                 lanes: int, hard_shoulder_available: bool):
        super().__init__()
        self._id = cs_id
        self._name = name
        self._type = cs_type
        self._location = location
        self._lanes = lanes
        self._hard_shoulder_available = hard_shoulder_available
