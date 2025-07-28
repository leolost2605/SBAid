"""This module contains the VissimCrossSection class."""
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.simulator.vissim.vissim import VissimConnectorCrossSectionState


class VissimCrossSection(SimulatorCrossSection):
    """This class represents the PTV Vissim simulator cross section."""
    __id: str
    __type: CrossSectionType
    __position: Location
    __lanes: int

    @SimulatorCrossSection.id.getter  # type: ignore
    def id(self) -> str:
        return self.__id

    @SimulatorCrossSection.type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """TODO"""
        return self.__type

    @SimulatorCrossSection.position.getter  # type: ignore
    def position(self) -> Location:
        """TODO"""
        return self.__position

    @SimulatorCrossSection.lanes.getter  # type: ignore
    def lanes(self) -> int:
        return self.__lanes

    @SimulatorCrossSection.hard_shoulder_available.getter
    def hard_shoulder_available(self) -> bool:
        """TODO"""
        return True

    def __init__(self, state: VissimConnectorCrossSectionState):
        super().__init__()
        self.set_state(state)

    def set_state(self, state: VissimConnectorCrossSectionState) -> None:
        self.__id = state.id
        self.__type = state.type
        self.__position = state.position
        self.__lanes = state.lanes
