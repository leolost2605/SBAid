"""This module defines the ParserFactory class"""
from gi.repository import GObject, Gio
from sbaid.model.algorithm_configuration.csv_parameter_parser import CSVParameterParser
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser)


class ParserFactory(GObject.GObject):
    """This class defines the ParserFactory class."""

    __parsers = []

    def __init__(self) -> None:
        """todo"""
        self.__parsers.append(CSVParameterParser)

    def get_parser(self, file: Gio.File) -> ParameterParser:
        """todo"""
        for parser in self.__parsers:
            if parser.can_handle_file(file):
                return parser
        raise NoSuitableParserException(Gio.content_type_guess(file.get_path())[0])

class NoSuitableParserException(Exception):
    """Exception raised when the user inputs a file in a format
        SBAid does not support for parameter configuration  input."""

    def __init__(self, file_format: str) -> None:
        self.message = "File format %s not supported." % file_format
