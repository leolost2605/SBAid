"""TO DO"""
from typing import Tuple


class Network:
    """TO DO"""
    def __init__(self, simulator: Simulator):
        """TO DO"""

    def load(self):
        """TO DO"""

    def import_from_file(self, file: File) -> Tuple[int, int]:
        """TO DO"""

    def create_cross_section(
            self,
            name: str,
            coordinates: Coordinates,
            cs_type: Common.CrossSectionType) -> int:
        """TO DO"""

    def delete_cross_section(self, cs_id: str):
        """TO DO"""

    def move_cross_section(self, cs_id: str, new_coordinates: Coordinates):
        """TO DO"""
