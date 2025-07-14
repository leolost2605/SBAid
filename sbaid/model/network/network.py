"""TODO"""
from sbaid.common import CrossSectionType
from sbaid.simulator import Simulator
from sbaid.common.coordinate import Coordinate
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.route import Route
from typing import Tuple
from gi.repository.Gio import File, ListModel


class Network:
    """TODO"""
    def __init__(self, simulator: Simulator):
        self.cross_sections: ListModel[CrossSection]
        self.route: Route

    def load(self):
        """TODO"""

    def import_from_file(self, file: File) -> Tuple[int, int]:
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
