"""
This module contains the abstract SimulatorCrossSection class
which provides cross section GObject properties.
"""
from gi.repository import GObject

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location


class SimulatorCrossSection(GObject.GObject):
    """
    This class is used as a wrapper for a cross section within the simulator.

    It contains several properties about the cross section.
    """
    id: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore
    name: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore
    type: CrossSectionType = GObject.Property(type=CrossSectionType,  # type: ignore
                                              flags=GObject.ParamFlags.READABLE,
                                              default=CrossSectionType.COMBINED)
    location: Location = GObject.Property(type=Location,  # type: ignore
                                          flags=GObject.ParamFlags.READABLE)
    lanes: int = GObject.Property(type=int, flags=GObject.ParamFlags.READABLE)  # type: ignore
    hard_shoulder_available: bool = GObject.Property(type=bool,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE,
                                                     default=False)

    @id.getter  # type: ignore
    def get_id(self) -> str:
        """Returns the id of the cross section."""
        return self.get_id()  # type: ignore

    @name.getter  # type: ignore
    def get_name(self) -> str:
        """Getter for the name."""
        return self.get_name()  # type: ignore

    @type.getter  # type: ignore
    def get_type(self) -> CrossSectionType:
        """Getter for the type."""
        return self.get_type()  # type: ignore

    @location.getter  # type: ignore
    def get_location(self) -> Location:
        """Getter for the location."""
        return self.get_location()  # type: ignore

    @lanes.getter  # type: ignore
    def get_lanes(self) -> int:
        """Getter for the lanes."""
        return self.get_lanes()  # type: ignore

    @hard_shoulder_available.getter  # type: ignore
    def get_hard_shoulder_available(self) -> bool:
        """Getter for the hard shoulder available boolean."""
        return self.get_hard_shoulder_available()  # type: ignore
