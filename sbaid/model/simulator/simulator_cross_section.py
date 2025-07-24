# mypy: disable-error-code="empty-body"
"""
This module contains the abstract SimulatorCrossSection class
which provides cross section GObject properties.
"""
from gi.repository import GObject

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location


class SimulatorCrossSection(GObject.GInterface):
    """
    This class is used as a wrapper for a cross section within the simulator
    that contains several properties about the cross section.
    """
    # GObject.Property definitions
    @GObject.Property(type=str)
    def id(self) -> str:
        """TODO"""

    @GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    def type(self) -> CrossSectionType:
        """TODO"""

    @GObject.Property(type=Location)
    def position(self) -> Location:
        """TODO"""

    @GObject.Property(type=int)
    def lanes(self) -> int:
        """TODO"""

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_available(self) -> bool:
        """TODO"""
