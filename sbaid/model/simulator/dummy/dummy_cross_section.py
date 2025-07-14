"""This module contains the DummyCrossSection class."""
from gi.repository import GObject

from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummyCrossSection(SimulatorCrossSection):
    """This class represents the dummy simulator cross section."""
    @GObject.Property(type=str)
    def simulator_cross_section_id(self) -> str:
        """TODO"""
        return ""

    @GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    def simulator_cross_section_type(self) -> CrossSectionType:
        """TODO"""
        return CrossSectionType.COMBINED

    @GObject.Property(type=Coordinate)
    def position(self) -> Coordinate:
        """TODO"""
        return Coordinate(0, 0)

    @GObject.Property(type=int)
    def lanes(self) -> int:
        """TODO"""
        return 0

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
