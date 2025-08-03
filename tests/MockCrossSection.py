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

    @SimulatorCrossSection.id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of the cross section."""
        return self.__id

    @SimulatorCrossSection.name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the cross section."""
        return self.__name

    @SimulatorCrossSection.type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """Returns the type of this cross section."""
        return self.__type

    @SimulatorCrossSection.location.getter  # type: ignore
    def location(self) -> Location:
        """Returns the location of this cross section."""
        return self.__location

    @SimulatorCrossSection.lanes.getter  # type: ignore
    def lanes(self) -> int:
        """Returns the number of lanes at this cross section."""
        return self.__lanes

    @SimulatorCrossSection.hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns whether the lane with index 0 is a hard shoulder. Always returns true
        because we assume every furthest-right lane is a hard shoulder."""
        return True

    def __init__(self, cs_id: str, name: str, cs_type: CrossSectionType, location: Location,
                 lanes: int):
        super().__init__()
        self.__id = cs_id
        self.__name = name
        self.__type = cs_type
        self.__location = location
        self.__lanes = lanes
