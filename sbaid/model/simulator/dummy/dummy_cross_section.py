"""This module contains the DummyCrossSection class."""
from gi.repository import GObject

from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummyCrossSection(SimulatorCrossSection):
    """This class represents the dummy simulator cross section."""
    id: str = GObject.Property(type=str)  # type: ignore
    name: str = GObject.Property(type=str)  # type: ignore
    type: CrossSectionType = GObject.Property(type=CrossSectionType,  # type: ignore
                                              default=CrossSectionType.COMBINED)
    location: Location = GObject.Property(type=Location)  # type: ignore
    lanes: int = GObject.Property(type=int)  # type: ignore
    hard_shoulder_available: bool = GObject.Property(type=bool, default=False)  # type: ignore

    def __init__(self, cs_id: str, cs_name: str, cs_type: CrossSectionType, location: Location,
                 lanes: int, hard_shoulder_available: bool) -> None:
        super().__init__(id=cs_id, name=cs_name, type=cs_type, location=location, lanes=lanes,
                         hard_shoulder_available=hard_shoulder_available)
