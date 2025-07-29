"""
This module contains the abstract SimulatorCrossSection class
which provides cross section GObject properties.
"""
from gi.repository import GObject

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location


class SimulatorCrossSection(GObject.GObject):
    """
    This class is used as a wrapper for a cross section within the simulator
    that contains several properties about the cross section.
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
