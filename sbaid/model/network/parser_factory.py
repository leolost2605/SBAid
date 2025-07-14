"""TODO"""
from gi.repository.Gio import File
from sbaid.model.network.cross_section_parser import CrossSectionParser
from sbaid.model.network.network import Network
from sbaid.simulator import Simulator


class ParserFactory(Network):
    """TODO"""
    def __init__(self, simulator: Simulator):
        super().__init__(simulator)
        self.parsers = None

    def get_parser(self, file: File) -> CrossSectionParser:
        """TODO"""
