"""This module contains the cross section class."""

from typing import cast
import asyncio
from gi.events import GLibEventLoopPolicy
from gi.repository import GObject, GLib
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.database.project_database import ProjectDatabase


class CrossSection(GObject.GObject):
    """This class defines a cross section in the network."""

    __cross_section: SimulatorCrossSection

    id: str = GObject.Property(type=str,  # type: ignore[assignment]
                          flags=GObject.ParamFlags.READABLE |
                          GObject.ParamFlags.WRITABLE |
                          GObject.ParamFlags.CONSTRUCT_ONLY)

    @id.getter  # type: ignore
    def id(self) -> str:
        return self.__cross_section.id

    name: str = GObject.Property(type=str,  # type: ignore[assignment]
                                 flags=GObject.ParamFlags.READABLE |
                                       GObject.ParamFlags.WRITABLE |
                                       GObject.ParamFlags.CONSTRUCT_ONLY)

    @name.getter  # type: ignore
    def name(self) -> str:
        return self.__cross_section.name  # TODO: needs implementation in simulator cross section

    @name.setter  # type: ignore
    def name(self, value: str) -> None:
        self.__cross_section.name = value

    location: Location = GObject.Property(type=Location)  # type: ignore

    @location.getter  # type: ignore
    def position(self) -> Location:
        return cast(Location, self.__cross_section.position)

    type: CrossSectionType = GObject.Property(type=CrossSectionType,
                                              default=CrossSectionType.COMBINED)  # type: ignore

    @type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        return cast(CrossSectionType, self.__cross_section.type)

    lanes: int = GObject.Property(type=int)  # type: ignore

    @lanes.getter  # type: ignore
    def lanes(self) -> int:
        return cast(int, self.__cross_section.lanes)

    b_display_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                                                  flags=GObject.ParamFlags.READABLE |
                                                        GObject.ParamFlags.WRITABLE |
                                                        GObject.ParamFlags.CONSTRUCT_ONLY,
                                                  default=False)

    @b_display_active.getter  # type: ignore
    def b_display_active(self) -> bool:
        """Returns the simulator cross section's b display status."""
        return self.b_display_active

    @b_display_active.setter  # type: ignore
    def b_display_active(self, value: bool) -> None:
        """Sets the simulator cross section's b display status."""
        self.b_display_active = value
        asyncio.set_event_loop_policy(GLib.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__update_b_display_active())
        loop.run_until_complete(task)

    async def __update_b_display_active(self) -> None:
        pass
        #project_db.


    hard_shoulder_available: bool = GObject.Property(type=bool, default=False)

    @hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns the simulator cross section's hard shoulder availability."""
        return self.__cross_section.hard_shoulder_available  # type: ignore

    hard_shoulder_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                               flags=GObject.ParamFlags.READABLE |
                                     GObject.ParamFlags.WRITABLE |
                                     GObject.ParamFlags.CONSTRUCT,
                                                  default=False)

    @hard_shoulder_active.getter  # type: ignore
    def hard_shoulder_active(self) -> bool:
        """Returns the simulator cross section's hard shoulder status."""
        return self.hard_shoulder_active

    @hard_shoulder_active.setter  # type: ignore
    def hard_shoulder_active(self, value: bool) -> None:
        """Sets the simulator cross section's hard shoulder status, if it is available."""
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available.")
        self.hard_shoulder_active = value
        asyncio.set_event_loop_policy(GLib.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__update_hard_shoulder_active())
        loop.run_until_complete(task)

    async def __update_hard_shoulder_active(self) -> None:
        pass

    def __init__(self, simulator_cross_section: SimulatorCrossSection, project_db: ProjectDatabase) -> None:
        """Constructs a new cross section with the given simulator cross section data."""
        self.__cross_section = simulator_cross_section
        self.__project_db = project_db
        super().__init__(location=simulator_cross_section.position,
                         type=simulator_cross_section.type,
                         id=simulator_cross_section.id)

    def load_from_db(self) -> None:
        """Loads cross section details from the database."""
        self.name = self.__project_db.get_cross_section_name(self.id)
        #self.hard_shoulder_active = self.__project_db.get_hard_shoulder_active
        #self.b_display_active = self.__project_db.get_b_display_active
        #TODO: methoden ainda nao existem


class FunctionalityNotAvailableException(Exception):
    """To be deleted :)"""
    # TODO: delete when exception is in common
