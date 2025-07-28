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
                          flags=GObject.ParamFlags.READABLE)

    @CrossSection.id.getter  # type: ignore
    def id(self) -> str:
        """Returns this cross section's id."""
        return self.__cross_section.id

    name: str = GObject.Property(type=str,  # type: ignore[assignment]
                                 flags=GObject.ParamFlags.READABLE |
                                       GObject.ParamFlags.WRITABLE |
                                       GObject.ParamFlags.CONSTRUCT_ONLY)

    @CrossSection.name.getter  # type: ignore
    def name(self) -> str:
        """Returns this cross section's name."""
        return self.__cross_section.name  # TODO: needs implementation in simulator cross section

    @CrossSection.name.setter  # type: ignore
    def name(self, value: str) -> None:
        self.__cross_section.name = value

    location: Location = GObject.Property(type=Location)  # type: ignore

    @CrossSection.location.getter  # type: ignore
    def position(self) -> Location:
        """Returns this cross section's position."""
        return cast(Location, self.__cross_section.position)

    type: CrossSectionType = GObject.Property(type=CrossSectionType,
                                              default=CrossSectionType.COMBINED)  # type: ignore

    @CrossSection.type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """Returns this cross section's type."""
        return cast(CrossSectionType, self.__cross_section.type)

    lanes: int = GObject.Property(type=int)  # type: ignore

    @CrossSection.lanes.getter  # type: ignore
    def lanes(self) -> int:
        """Returns this cross section's type."""
        return cast(int, self.__cross_section.lanes)

    b_display_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                                                  flags=GObject.ParamFlags.READABLE |
                                                        GObject.ParamFlags.WRITABLE |
                                                        GObject.ParamFlags.CONSTRUCT_ONLY,
                                                  default=False)

    @CrossSection.b_display_active.getter  # type: ignore
    def b_display_active(self) -> bool:
        """Returns the simulator cross section's b display status."""
        return self.b_display_active

    @CrossSection.b_display_active.setter  # type: ignore
    def b_display_active(self, value: bool) -> None:
        """Sets the simulator cross section's b display status."""
        self.b_display_active = value
        asyncio.set_event_loop_policy(GLib.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__update_b_display_active(value))
        loop.run_until_complete(task)

    hard_shoulder_available: bool = GObject.Property(type=bool, default=False)

    @CrossSection.hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns the simulator cross section's hard shoulder availability."""
        return self.__cross_section.hard_shoulder_available  # type: ignore

    hard_shoulder_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                               flags=GObject.ParamFlags.READABLE |
                                     GObject.ParamFlags.WRITABLE |
                                     GObject.ParamFlags.CONSTRUCT,
                                                  default=False)

    @CrossSection.hard_shoulder_active.getter  # type: ignore
    def hard_shoulder_active(self) -> bool:
        """Returns the simulator cross section's hard shoulder status."""
        return self.hard_shoulder_active

    @CrossSection.hard_shoulder_active.setter  # type: ignore
    def hard_shoulder_active(self, value: bool) -> None:
        """Sets the simulator cross section's hard shoulder status, if it is available."""
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available.")
        self.hard_shoulder_active = value
        asyncio.set_event_loop_policy(GLib.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__update_hard_shoulder_active(value))
        loop.run_until_complete(task)

    def __init__(self, simulator_cross_section: SimulatorCrossSection,
                 project_db: ProjectDatabase) -> None:
        """Constructs a new cross section with the given simulator cross section data."""
        self.__cross_section = simulator_cross_section
        self.__project_db = project_db
        super().__init__(location=simulator_cross_section.position,
                         type=simulator_cross_section.type,
                         id=simulator_cross_section.id)

    async def load_from_db(self) -> None:
        """Loads cross section details from the database."""
        self.name = await self.__project_db.get_cross_section_name(self.id)
        self.hard_shoulder_active = (await self.__project_db
                                     .get_cross_section_hard_shoulder_active(self.id))
        self.b_display_active = await self.__project_db.get_cross_section_b_display_active(self.id)

    async def __update_b_display_active(self, value: bool) -> None:
        await self.__project_db.set_cross_section_b_display_active(self.id, value)

    async def __update_hard_shoulder_active(self, value: bool) -> None:
        await self.__project_db.set_cross_section_hard_shoulder_active(self.id, value)


class FunctionalityNotAvailableException(Exception):
    """To be deleted :)"""
    # TODO: delete when exception is in common
