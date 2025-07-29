"""
This module contains the network class which is used to get information about the network
and manage cross sections.
"""
import sys

import gi

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, Gio, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location

from sbaid.model.network.network import Network as ModelNetwork
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection
from sbaid.view_model.network.cross_section import CrossSection


class Network(GObject.GObject):
    """
    Represents the network from the simulation file. Provides information about the route
    and the cross sections on the route. Allows to manage the cross sections on the route.
    """

    __network: ModelNetwork
    __cross_sections: Gtk.MapListModel

    cross_sections: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    @cross_sections.getter  # type: ignore
    def cross_sections(self) -> Gio.ListModel:
        """Returns the list of cross sections on the route."""
        return self.__cross_sections

    def __init__(self, network: ModelNetwork) -> None:
        super().__init__()
        self.__network = network
        self.__cross_sections = Gtk.MapListModel.new(network.cross_sections,
                                                     self.__map_func, self)

    def __map_func(self, model_cross_section: ModelCrossSection) -> GObject.GObject:
        return CrossSection(model_cross_section)

    async def create_cross_section(self, name: str, location: Location,
                                   cs_type: CrossSectionType) -> int:
        """
        Create a new cross section on the route.
        :param name: the name of the new cross section
        :param location: the location of the new cross section
        :param cs_type: the type of the new cross section
        :return: the position of the new cross section in self.cross_sections
        """
        return await self.__network.create_cross_section(name, location, cs_type)

    async def delete_cross_section(self, cs_id: str) -> None:
        """
        Deletes a cross section on the route.
        :param cs_id: the id of the cross section to delete
        """
        return await self.__network.delete_cross_section(cs_id)

    async def move_cross_section(self, cs_id: str, new_location: Location) -> None:
        """
        Moves a cross section on the route to a new location.
        :param cs_id: the id of the cross section to move
        :param new_location: the new location of the cross section
        """
        return await self.__network.move_cross_section(cs_id, new_location)
