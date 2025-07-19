"""This module contains the VissimCrossSection class."""
from gi.repository import GObject

from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.model.simulator.vissim.vissim import VissimConnectorCrossSectionState


class VissimCrossSection(SimulatorCrossSection):
    """This class represents the PTV Vissim simulator cross section."""

    __id: str
    __type: CrossSectionType
    __position: Coordinate
    __lanes: int

    def __init__(self, state: VissimConnectorCrossSectionState):
        super().__init__()
        self.__id = state.id
        self.__type = state.type
        self.__position = state.position
        self.__lanes = state.lanes

    @GObject.Property(type=str)
    def id(self) -> str:
        return self.__id

    @GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    def type(self) -> CrossSectionType:
        return self.__type

    @GObject.Property(type=Coordinate)
    def position(self) -> Coordinate:
        return self.__position

    @GObject.Property(type=int)
    def lanes(self) -> int:
        return self.__lanes

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_available(self) -> bool:
        """TODO"""
        return False

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_active(self) -> bool:
        """TODO"""
        return False

    @GObject.Property(type=bool, default=False)
    def b_display_active(self) -> bool:
        """TODO"""
        return False
