"""This module consists of the CSV cross section parser. TODO"""
import csv
from abc import ABC
from sbaid.model.network.cross_section_parser import (CrossSectionParser,
                                                      CrossSectionParserForeachFunc)
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.coordinate import Coordinate
from gi.repository import Gio


class CSVCrossSectionParser(CrossSectionParser, ABC):
    """This class handles the parsing of CSV files containing cross sections."""

    def can_handle_file(self, file_path: str) -> bool:
        return Gio.content_type_guess(file_path)[0] == ".csv"

    def foreach_cross_section(self, file: Gio.File,
                              foreach_func: CrossSectionParserForeachFunc) -> tuple[int, int]:
        """TODO:
        - check for a valid header; if there isn't one go back and start reading from the first line
        - read file
        - convert row for row, skip if invalid (increment invalid counter)
        - create cross section instances with valid rows, increment valid counter
        """
        with open(file.get_path(), newline='') as csvfile:
            valid_cross_sections = 0
            invalid_cross_sections = 0
            csv_reader = csv.reader(csvfile)
            try:
                has_header = self.__has_valid_header(csv_reader)
            except StopIteration:
                raise InvalidFileFormattingException("Empty file.")
            if not has_header:
                csvfile.seek(0)
            for row in csv_reader:
                if self.__parse_cross_section(row):
                    valid_cross_sections += 1  # falls creation funktioniert?

                else:
                    next(csv_reader)
                    invalid_cross_sections += 1


    def __has_valid_header(self, csv_reader: csv.reader) -> bool:
            row = next(csv_reader)
            return (row[0].casefold() == "Name".casefold()
                    and row[1].casefold() == "X-Coordinate".casefold()
                    and row[2].casefold() == "Y-Coordinate".casefold()
                    and row[3].casefold() == "Type".casefold())

    def __parse_cross_section(self, row: list) -> Coordinate | None:
        if len(row) != 4:
            return None
        try:
            coordinates = Coordinate(float(row[1]),float(row[2]))
        except ValueError:
            return None
        if not self.__cross_section_type_valid(row[3]):
            return None
        return coordinates

    def __cross_section_type_valid(self, cross_section_type: str) -> int | None:
        try:
            return CrossSectionType[cross_section_type.upper()].value
        except KeyError:
            return None

class InvalidFileFormattingException(Exception):
    """Exception raised when the user inputs a file with invalid formatting."""
    def __init__(self, formatting_error: str):
        self.message = "Illegal file formatting: \n %s"%formatting_error

