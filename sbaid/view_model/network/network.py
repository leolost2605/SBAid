"""TODO"""
from gi.repository import GObject, Gio

from common.cross_section_type import CrossSectionType
from common.location import Location
from sbaid.model.network import network
from view_model.network.cross_section import CrossSection


class Network(GObject.GObject):
    """TODO"""
    route = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE |
                                          GObject.ParamFlags.WRITABLE |
                                          GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, model_network: network.Network) -> None:
        """TODO"""
        route = Gio.ListStore(Location)
        for point in model_network.route.points:
            route.append(point)

        super().__init__(route=route)

    def create_cross_section(self, name: str, location: Location, cs_type: CrossSectionType) -> CrossSection:
        """TODO"""

    def move_cross_section(self, cs_id: str, location: Location) -> bool:
        """TODO"""

    def delete_cross_section(self, cs_id: str) -> None:
        """TODO"""

    def import_cross_sections(self, path: str) -> tuple[int, int]:
        """TODO"""
