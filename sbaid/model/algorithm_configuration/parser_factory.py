"""This module defines the ParserFactory class"""
from gi.repository import GObject, Gio
from sbaid.model.algorithm_configuration import ParameterParser

class ParserFactory(GObject.GObject):

    # GObject property definition
    parsers = GObject.property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self):
        """todo"""
        pass

    def get_parser(self, file: Gio.File) -> ParameterParser:
        """todo"""
        pass



