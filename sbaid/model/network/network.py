"""TODO"""
from typing import Tuple
from gi.repository import Gio, GObject
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator import Simulator
from sbaid.common.location import Location
from sbaid.model.network.route import Route


class Network(GObject.Object):
    """TODO"""
    cross_sections = GObject.Property(type=Gio.ListModel,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT_ONLY)
    route = GObject.Property(type=Route,
                             flags=GObject.ParamFlags.READABLE |
                             GObject.ParamFlags.WRITABLE |
                             GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, simulator: Simulator) -> None:
        """TODO"""
        super().__init__()

    def load(self) -> None:
        """TODO"""

    def import_from_file(self, file: Gio.File) -> Tuple[int, int]:
        """TODO"""
        return 0, 0

    def create_cross_section(
            self,
            name: str,
            location: Location,
            cs_type: CrossSectionType) -> int:
        """TODO"""
        return 0

    def delete_cross_section(self, cs_id: str) -> None:
        """TODO"""

    def move_cross_section(self, cs_id: str, new_location: Location) -> None:
        """TODO"""
