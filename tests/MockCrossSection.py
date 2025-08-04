"""This module contains the VissimCrossSection class."""
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class MockCrossSection(SimulatorCrossSection):
    """This class represents a simulator cross section."""
    __id: str
    __name: str
    __type: CrossSectionType
    __location: Location
    __lanes: int

    def get_id(self) -> str:
        """Returns the id of the cross section."""
        return self.__id

    def get_name(self) -> str:
        """Returns the name of the cross section."""
        return self.__name

    def get_type(self) -> CrossSectionType:
        """Returns the type of this cross section."""
        return self.__type

    def get_location(self) -> Location:
        """Returns the location of this cross section."""
        return self.__location

    def get_lanes(self) -> int:
        """Returns the number of lanes at this cross section."""
        return self.__lanes

    def get_hard_shoulder_available(self) -> bool:
        """Returns whether the lane with index 0 is a hard shoulder. Always returns true
        because we assume every furthest-right lane is a hard shoulder."""
        return True

    def move(self, location: Location):
        self.__location = location

    def __init__(self, cs_id: str, name: str, cs_type: CrossSectionType, location: Location,
                 lanes: int):
        super().__init__()
        self.__id = cs_id
        self.__name = name
        self.__type = cs_type
        self.__location = location
        self.__lanes = lanes
