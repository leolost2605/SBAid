"""This module defines the ParserFactory class"""
from gi.repository import GObject, Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser)


class ParserNotFoundException(Exception):
    """An exception that will be raised if no parser for the given file was found."""


class ParserFactory(GObject.GObject):
    """todo"""

    def get_parser(self, file: Gio.File) -> ParameterParser:
        """todo"""
        raise ParserNotFoundException()
