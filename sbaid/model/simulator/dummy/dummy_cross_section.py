"""This module contains the DummyCrossSection class."""
from gi.repository import GObject

from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummyCrossSection(SimulatorCrossSection):
    """This class represents the dummy simulator cross section."""
    id = GObject.Property(type=str)
    type = GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    location = GObject.Property(type=Location)
    lanes = GObject.Property(type=int)
    hard_shoulder_available = GObject.Property(type=bool, default=False)
    hard_should_active = GObject.Property(type=bool, default=False)
    b_display_active = GObject.Property(type=bool, default=False)

    def __init__(self, cs_id: str, cs_type: CrossSectionType, location: Location, lanes: int,
                 hard_shoulder_available: bool, hard_shoulder_active: bool,
                 b_display_active: bool) -> None:
        super().__init__(id=cs_id, type=cs_type, location=location, lanes=lanes,
                         hard_shoulder_available=hard_shoulder_available, hard_shoulder_active=hard_shoulder_active,
                         b_display_active=b_display_active)
