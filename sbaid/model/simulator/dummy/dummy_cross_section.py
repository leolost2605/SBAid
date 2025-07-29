"""This module contains the DummyCrossSection class."""
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummyCrossSection(SimulatorCrossSection):
    """This class represents the dummy simulator cross section."""
    @SimulatorCrossSection.id.getter  # type: ignore
    def id(self) -> str:
        """TODO"""
        return ""

    @SimulatorCrossSection.type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """TODO"""
        return CrossSectionType.COMBINED

    @SimulatorCrossSection.location.getter  # type: ignore
    def location(self) -> Location:
        """TODO"""
        return Location(0, 0)

    @SimulatorCrossSection.lanes.getter  # type: ignore
    def lanes(self) -> int:
        """TODO"""
        return 0

    @SimulatorCrossSection.hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """TODO"""
        return False
