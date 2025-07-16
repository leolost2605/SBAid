"""TODO"""

from gi.repository import Gio
from sbaid.model.network.cross_section_parser import CrossSectionParser
from sbaid.model.simulator.simulator import Simulator


class ParserFactory:
    """TODO"""

    def __init__(self, simulator: Simulator) -> None:
        """TODO"""

    def get_parser(self, file: Gio.File) -> CrossSectionParser:
        """TODO"""
        return None
