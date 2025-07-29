"""This module contains the VissimCrossSection class."""
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.simulator.vissim.vissim import VissimConnectorCrossSectionState


class VissimCrossSection(SimulatorCrossSection):
    """This class represents the PTV Vissim simulator cross section."""
    __id: str
    __name: str
    __type: CrossSectionType
    __position: Location
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
        return self.__position

    @SimulatorCrossSection.lanes.getter  # type: ignore
    def lanes(self) -> int:
        """Returns the number of lanes at this cross section."""
        return self.__lanes

    @SimulatorCrossSection.hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns whether the lane with index 0 is a hard shoulder."""
        return True

    def __init__(self, state: VissimConnectorCrossSectionState):
        super().__init__()
        self.set_state(state)

    def set_state(self, state: VissimConnectorCrossSectionState) -> None:
        """Sets a new state for this cross section."""
        self.__id = state.id
        self.__name = state.name
        self.__type = state.type
        self.__position = state.position
        self.__lanes = state.lanes
