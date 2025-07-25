"""This module contains the cross section class."""
from gi.repository import GObject
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
import typing
# from sbaid.model.database.project_database import ProjectDatabase


class CrossSection(GObject.GObject):
    """This class defines a cross section in the network."""

    __cross_section: SimulatorCrossSection

    @GObject.Property(type=str)
    def id(self) -> str:
        return typing.cast(str, self.__cross_section.id)

    @GObject.Property(type=str)
    def name(self) -> str:
        # TODO: read from database or idk
        return "hi"

    @GObject.Property(type=Location)
    def location(self) -> Location:
        return self.__cross_section.position # type: ignore

    @GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    def type(self) -> CrossSectionType:
        return self.__cross_section.type # type: ignore

    @GObject.Property(type=int)
    def lanes(self) -> int:
        return self.__cross_section.lanes # type: ignore

    b_display_active = GObject.Property(type=bool, default=False)

    @b_display_active.getter #type: ignore
    def b_display_active(self) -> bool:
        return self.__cross_section.b_display_active

    @b_display_active.setter #type: ignore
    def b_display_active(self, value: bool) -> None:
        self.__cross_section.b_display_active = value

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_available(self) -> bool:
        return self.__cross_section.hard_shoulder_available # type: ignore 

    hard_shoulder_active = GObject.Property(type=bool, default=False)

    @hard_shoulder_active.getter #type: ignore
    def hard_shoulder_active(self) -> bool:
        return self.__cross_section.hard_shoulder_available

    @hard_shoulder_active.setter #type: ignore
    def hard_shoulder_active(self, value: bool) -> None:
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available")
        self.__cross_section.hard_shoulder_available = value

    def __init__(self, simulator_cross_section: SimulatorCrossSection) -> None:
        """Constructs a new cross section with the given simulator cross section data."""
        self.__cross_section = simulator_cross_section
        super().__init__(location=simulator_cross_section.position,
                         type=simulator_cross_section.type,
                         id=simulator_cross_section.id)

    def load_from_db(self) -> None:
        """Loads cross section details from the database."""
        # TODO: have project database instance
        # self.name = project_db.get_cross_section_name(self.id)

class FunctionalityNotAvailableException(Exception):  #TODO: delete when exception is in common
    pass
