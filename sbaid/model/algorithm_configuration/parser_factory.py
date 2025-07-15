"""This module defines the ParserFactory class"""
from gi.repository import GObject, Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser)


class ParserFactory(GObject.GObject):
    """todo"""

    def __init__(self) -> None:
        """todo"""

    def get_parser(self, file: Gio.File) -> ParameterParser:
        """todo"""
        return None
