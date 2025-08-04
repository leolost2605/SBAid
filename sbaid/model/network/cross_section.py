"""This module contains the cross section class."""

import asyncio
from gi.repository import GObject
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.database.project_database import ProjectDatabase


class CrossSection(GObject.GObject):
    """This class defines a cross section in the network."""

    __cross_section: SimulatorCrossSection
    __background_tasks: set[asyncio.Task[None]]
    __name: str | None
    __b_display_active: bool
    __hard_shoulder_active: bool

    id: str = GObject.Property(type=str,  # type: ignore[assignment]
                               flags=GObject.ParamFlags.READABLE)

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns this cross section's id."""
        return self.__cross_section.id

    name: str = GObject.Property(type=str,  # type: ignore[assignment]
                                 flags=GObject.ParamFlags.READABLE |
                                 GObject.ParamFlags.WRITABLE)

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns this cross section's name."""
        if self.__name is not None:
            return self.__name
        return self.__cross_section.name

    @name.setter  # type: ignore
    def name(self, value: str) -> None:  # pylint: disable=function-redefined
        self.__name = value
        task = asyncio.create_task(self.__update_cross_section_name(value))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    location: Location = GObject.Property(type=Location)  # type: ignore

    @location.getter  # type: ignore
    def position(self) -> Location:
        """Returns this cross section's position."""
        return self.__cross_section.location

    type: CrossSectionType = GObject.Property(type=CrossSectionType,
                                              default=CrossSectionType.COMBINED)  # type: ignore

    @type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """Returns this cross section's type."""
        return self.__cross_section.type

    lanes: int = GObject.Property(type=int)  # type: ignore

    @lanes.getter  # type: ignore
    def lanes(self) -> int:
        """Returns this cross section's type."""
        return self.__cross_section.lanes

    b_display_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                                              flags=GObject.ParamFlags.READABLE |
                                              GObject.ParamFlags.WRITABLE,
                                              default=False)

    @b_display_active.getter  # type: ignore
    def b_display_active(self) -> bool:
        """Returns the simulator cross section's b display status."""
        return self.__b_display_active

    @b_display_active.setter  # type: ignore
    def b_display_active(self, value: bool) -> None:  # pylint: disable=function-redefined
        """Sets the simulator cross section's b display status."""
        self.__b_display_active = value
        task = asyncio.create_task(self.__update_b_display_active(value))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    hard_shoulder_available: bool = GObject.Property(type=bool, default=False)  # type: ignore

    @hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns the simulator cross section's hard shoulder availability."""
        return self.__cross_section.hard_shoulder_available

    hard_shoulder_active: bool = GObject.Property(type=bool,  # type: ignore[assignment]
                                                  flags=GObject.ParamFlags.READABLE |
                                                  GObject.ParamFlags.WRITABLE,
                                                  default=False)

    @hard_shoulder_active.getter  # type: ignore
    def hard_shoulder_active(self) -> bool:
        """Returns the simulator cross section's hard shoulder status."""
        return self.__hard_shoulder_active

    @hard_shoulder_active.setter  # type: ignore
    def hard_shoulder_active(self, value: bool) -> None:  # pylint: disable=function-redefined
        """Sets the simulator cross section's hard shoulder status, if it is available."""
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available.")
        self.__hard_shoulder_active = value
        task = asyncio.create_task(self.__update_hard_shoulder_active(value))
        self.__background_tasks.add(task)
        task.add_done_callback(self.__background_tasks.discard)

    def __init__(self, simulator_cross_section: SimulatorCrossSection,
                 project_db: ProjectDatabase) -> None:
        """Constructs a new cross section with the given simulator cross section data."""
        self.__cross_section = simulator_cross_section
        self.__project_db = project_db
        self.__background_tasks = set()
        self.__b_display_active = False
        self.__hard_shoulder_active = False
        self.__name = self.__cross_section.name
        super().__init__()

    async def load_from_db(self) -> None:
        """Loads cross section details from the database."""
        db_name = await self.__project_db.get_cross_section_name(self.id)
        if db_name is not None:
            self.__name = db_name
        db_hard_shoulder_active = await (self.__project_db.
                                         get_cross_section_hard_shoulder_active(self.id))
        if db_hard_shoulder_active is not None:
            self.__hard_shoulder_active = db_hard_shoulder_active
        db_b_display_active = await (self.__project_db.
                                     get_cross_section_b_display_active(self.id))
        if db_b_display_active is not None:
            self.__b_display_active = db_b_display_active

    async def __update_b_display_active(self, value: bool) -> None:
        await self.__project_db.set_cross_section_b_display_active(self.id, value)

    async def __update_hard_shoulder_active(self, value: bool) -> None:
        await self.__project_db.set_cross_section_hard_shoulder_active(self.id, value)

    async def __update_cross_section_name(self, name: str) -> None:
        await self.__project_db.set_cross_section_name(self.id, name)


class FunctionalityNotAvailableException(Exception):
    """To be deleted :)"""
    # TODO: delete when exception is in common
