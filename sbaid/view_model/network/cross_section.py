"""TODO"""
from gi.repository import GObject

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection


class FunctionalityNotAvailableException(Exception):
    pass


class CrossSection(GObject.GObject):
    __cross_section: ModelCrossSection

    @GObject.Property(type=str)
    def id(self) -> str:
        return self.__cross_section.id

    @GObject.Property(type=str)
    def name(self) -> str:
        return self.__cross_section.name

    @GObject.Property(type=Location)
    def position(self) -> Location:
        return self.__cross_section.position

    @GObject.Property(type=CrossSectionType, default=CrossSectionType.COMBINED)
    def type(self) -> CrossSectionType:
        return self.__cross_section.type

    @GObject.Property(type=int)
    def lanes(self) -> int:
        return self.__cross_section.lanes

    @GObject.Property(type=bool, default=False)
    def b_display_usable(self) -> bool:
        return self.__cross_section.b_display_active

    @b_display_usable.setter
    def b_display_usable(self, value: bool) -> None:
        self.__cross_section.b_display_active = value

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_available(self) -> bool:
        return self.__cross_section.hard_shoulder_available

    @GObject.Property(type=bool, default=False)
    def hard_shoulder_usable(self) -> bool:
        return self.__cross_section.hard_shoulder_available

    @hard_shoulder_usable.setter
    def hard_shoulder_usable(self, value: bool) -> None:
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available")

        self.__cross_section.hard_shoulder_available = value

    def __init__(self, cross_section: ModelCrossSection) -> None:
        super().__init__()
        self.__cross_section = cross_section
        cross_section.connect("notify", self.__on_notify)

    def __on_notify(self, pspec: GObject.ParamSpec) -> None:
        self.notify(pspec.name)


