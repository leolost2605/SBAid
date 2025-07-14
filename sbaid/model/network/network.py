"""TODO"""
from sbaid.common import CrossSectionType
from sbaid.simulator import Simulator
from sbaid.common.coordinate import Coordinate
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.route import Route
from typing import Tuple
from gi.repository import Gio, GObject


class Network:
    """TODO"""
    cross_sections = GObject.Property(type=Gio.ListModel[CrossSection],
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT)
    route = GObject.Property(type=Route,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator: Simulator):
        self.cross_sections: Gio.ListModel[CrossSection]
        self.route: Route

    def load(self):
        """TODO"""

    def import_from_file(self, file: Gio.File) -> Tuple[int, int]:
        """TODO"""

    def create_cross_section(
            self,
            name: str,
            coordinates: Coordinate,
            cs_type: CrossSectionType) -> int:
        """TODO"""

    def delete_cross_section(self, cs_id: str):
        """TODO"""

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinate):
        """TODO"""
