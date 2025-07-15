"""TODO"""
from gi.repository import Gio, GObject
from gi.repository.Gio import ListModel
from sbaid.model.network.cross_section_parser import CrossSectionParser
from sbaid.model.simulator import Simulator


class ParserFactory:
    """TODO"""
    parsers = GObject.Property(type=ListModel,
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator: Simulator) -> None:
        """TODO"""

    def get_parser(self, file: Gio.File) -> CrossSectionParser:
        cross_section_parser = CrossSectionParser.__init__(self)
        return cross_section_parser  # TODO
