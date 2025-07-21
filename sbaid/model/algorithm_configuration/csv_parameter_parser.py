"""This module defines the CSVParameterParser class."""
import csv
from typing import Tuple
from gi.repository import Gio
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)


class CSVParameterParser(ParameterParser):
    """TODO"""

    def can_handle(self, file: Gio.File) -> bool:
        """todo"""
        return Gio.content_type_guess(file.get_path())[0] == ".csv"


    def for_each_parameter(self, file: Gio.File,
                           callback: ParameterParserForeachFunc) -> Tuple[int, int]:
        """TODO"""
        with open(file.get_path(), newline='') as csvfile:
            valid_parameters = 0
            invalid_parameters = 0

            csv_reader = csv.reader(csvfile)
            try:
                has_header = self.__has_valid_header(csv_reader)
            except StopIteration:  # raised if the file is empty and there is no line to read from
                raise InvalidFileFormattingException()

        return valid_parameters, invalid_parameters

    def __has_valid_header(self, csv_reader) -> bool:
        """Control if first row = header = all parameter names are valid and unique"""

        return None

    def __cross_sections_valid(self, csv_reader) -> bool:
        """Control if first column are all valid cross-section names"""
        return None