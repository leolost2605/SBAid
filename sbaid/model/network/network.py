"""TODO"""
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator import Simulator
from sbaid.common.coordinate import Coordinate
from sbaid.model.network.route import Route
from typing import Tuple
from gi.repository import Gio, GObject


class Network(GObject.Object):
    """TODO"""
    cross_sections = GObject.Property(type=Gio.ListModel,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT)
    route = GObject.Property(type=Route,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator: Simulator) -> None:
        super().__init__()
        """TODO"""

    def load(self) -> None:
        pass #TODO

    def import_from_file(self, file: Gio.File) -> Tuple[int, int]:
        pass #TODO

    def create_cross_section(
            self,
            name: str,
            coordinates: Coordinate,
            cs_type: CrossSectionType) -> int:
        pass #TODO

    def delete_cross_section(self, cs_id: str) -> None:
        """TODO"""

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinate) -> None:
        """TODO"""
