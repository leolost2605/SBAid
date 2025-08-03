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
        self.__location = state.location
        self.__lanes = state.lanes
