"""TODO"""
from common import CrossSectionType
from simulator import Simulator
from model import Coordinates
from typing import Tuple
from gi.repository.Gio import File


class Network:
    """TODO"""
    def __init__(self, simulator: Simulator):
        """TODO"""

    def load(self):
        """TODO"""

    def import_from_file(self, file: File) -> Tuple[int, int]:
        """TODO"""

    def create_cross_section(
            self,
            name: str,
            coordinates: Coordinates,
            cs_type: CrossSectionType) -> int:
        """TODO"""

    def delete_cross_section(self, cs_id: str):
        """TODO"""

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinates):
        """TODO"""
