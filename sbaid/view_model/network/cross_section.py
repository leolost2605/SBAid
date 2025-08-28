"""
This module contains the cross section class which is mainly responsible for passing
through properties from model cross sections.
"""
from gi.repository import GObject

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection


class FunctionalityNotAvailableException(Exception):
    """An Exception raised when a functionality is not available."""


class CrossSection(GObject.GObject):
    """
    Represents a cross section on the route.
    """
    __cross_section: ModelCrossSection

    id: str = GObject.Property(type=str)  # type: ignore

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of the cross section."""
        return self.__cross_section.id

    name: str = GObject.Property(type=str)  # type: ignore

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the cross section."""
        return self.__cross_section.name

    @name.setter  # type: ignore
    def name(self, value: str) -> None:
        """Sets the name of the cross section."""
        self.__cross_section.name = value

    location: Location = GObject.Property(type=Location)  # type: ignore

    @location.getter  # type: ignore
    def location(self) -> Location:
        """Returns the location of this cross section."""
        return self.__cross_section.location

    type: CrossSectionType = GObject.Property(type=CrossSectionType,
                                              default=CrossSectionType.COMBINED)  # type: ignore

    @type.getter  # type: ignore
    def type(self) -> CrossSectionType:
        """Returns the type of the cross section."""
        return self.__cross_section.type

    lanes: int = GObject.Property(type=int)  # type: ignore

    @lanes.getter  # type: ignore
    def lanes(self) -> int:
        """Returns the number of lanes of the cross section."""
        return self.__cross_section.lanes

    b_display_usable: bool = GObject.Property(type=bool, default=False)  # type: ignore

    @b_display_usable.getter  # type: ignore[no-redef]
    def b_display_usable(self) -> bool:
        """Returns whether the algorithm should calculate b displays for this cross section."""
        return self.__cross_section.b_display_active

    @b_display_usable.setter  # type: ignore[no-redef]
    def b_display_usable(self, value: bool) -> None:
        """Sets whether the algorithm should calculate b displays for this cross section."""
        self.__cross_section.b_display_active = value

    hard_shoulder_available: bool = GObject.Property(type=bool, default=False)  # type: ignore

    @hard_shoulder_available.getter  # type: ignore
    def hard_shoulder_available(self) -> bool:
        """Returns whether the lane with index 0 is a hard shoulder."""
        return self.__cross_section.hard_shoulder_available

    hard_shoulder_usable: bool = GObject.Property(type=bool, default=False)  # type: ignore

    @hard_shoulder_usable.getter  # type: ignore
    def hard_shoulder_usable(self) -> bool:
        """
        Returns whether the algorithm can allow opening the hard shoulder so the lane with
        index 0. Always false if no hard shoulder available.
        """
        return self.__cross_section.hard_shoulder_active

    @hard_shoulder_usable.setter  # type: ignore
    def hard_shoulder_usable(self, value: bool) -> None:
        """
        Sets whether the algorithm can allow opening the hard shoulder so the lane with
        index 0. Setting this is ignored if no hard shoulder is available.
        """
        if not self.hard_shoulder_available:
            raise FunctionalityNotAvailableException("Hard shoulder is not available")

        self.__cross_section.hard_shoulder_active = value

    def __init__(self, cross_section: ModelCrossSection) -> None:
        super().__init__()
        self.__cross_section = cross_section
        cross_section.connect("notify", self.__on_notify)

    def __on_notify(self, obj: GObject.Object, pspec: GObject.ParamSpec) -> None:
        self.notify(pspec.name.replace("active", "usable"))
