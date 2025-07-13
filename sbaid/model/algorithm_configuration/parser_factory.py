"""This module defines the ParserFactory class"""
from gi.repository import GObject, Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser)


class ParserFactory(GObject.GObject):
    """todo"""

    # GObject property definition
    parsers = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self) -> None:
        """todo"""

    def get_parser(self, file: Gio.File) -> ParameterParser:
        """todo"""
        return None
