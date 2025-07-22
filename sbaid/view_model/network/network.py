"""TODO"""
import sys

import gi

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, Gio, Gtk
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from sbaid.model.network.network import Network as ModelNetwork
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection
from sbaid.view_model.network.cross_section import CrossSection


class Network(GObject.GObject):
    __network: ModelNetwork
    __cross_sections: Gtk.MapListModel

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
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
        """TODO"""
        return await self.__network.create_cross_section(name, location, cs_type)

    async def delete_cross_section(self, cs_id: str) -> None:
        """TODO"""
        return await self.__network.delete_cross_section(cs_id)

    async def move_cross_section(self, cs_id: str, new_location: Location) -> None:
        """TODO"""
        return await self.__network.move_cross_section(cs_id, new_location)
