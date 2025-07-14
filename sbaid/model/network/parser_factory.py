"""TODO"""
from gi.repository import Gio, GObject
from gi.repository.Gio import ListModel
from sbaid.model.network.cross_section_parser import CrossSectionParser
from sbaid.model.network.network import Network
from sbaid.simulator import Simulator


class ParserFactory(Network):
    """TODO"""
    parsers = GObject.Property(type=ListModel[CrossSectionParser],
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator: Simulator):
        super().__init__(simulator)
        self.parsers = ListModel[CrossSectionParser]

    def get_parser(self, file: Gio.File) -> CrossSectionParser:
        """TODO"""
