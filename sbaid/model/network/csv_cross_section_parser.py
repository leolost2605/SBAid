"""This module consists of the CSV cross section parser and InvalidFileFormattingException,
which can be raised during file parsing and handling."""
import csv
import aiofiles
import typing
from gi.repository import Gio
from sbaid.model.network.cross_section_parser import (CrossSectionParser,
                                                      CrossSectionParserForeachFunc)
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location


class CSVCrossSectionParser(CrossSectionParser):
    """This class handles the parsing of CSV files containing cross sections."""

    def can_handle_file(self, file_path: str) -> bool:
        """Checks if the given file is a csv file."""
        return Gio.content_type_guess(file_path)[0] == ".csv"

    async def foreach_cross_section(self, file: Gio.File,
                                    foreach_func: CrossSectionParserForeachFunc)\
            -> tuple[int, int]:
        """Loads the file contents asynchronously and reads the input CSV file row by row,
        attempting to add the cross section the row represents to the network.
        Returns the amount of added and skipped cross sections."""
        path = typing.cast(str, file.get_path())
        async with aiofiles.open(path, "r+") as csvfile:
            valid_cross_sections = 0
            invalid_cross_sections = 0
            csv_reader = csv.reader(await csvfile.readlines())
            try:
                has_header = self.__has_valid_header(next(csv_reader))
            except StopIteration as exc:  # raised if the file is empty
                raise InvalidFileFormattingException() from exc
            if not has_header:
                await csvfile.seek(0)  # restart reading from the beginning of file
            for row in csv_reader:
                parsed_info = self.__parse_cross_section_syntax(row)
                if parsed_info is not None:
                    if parsed_info[0]:
                        if await foreach_func(row[0], parsed_info[0], parsed_info[1]):
                            valid_cross_sections += 1
                        else:
                            invalid_cross_sections += 1
                    else:
                        next(csv_reader)
                        invalid_cross_sections += 1
        if valid_cross_sections == 0:
            raise InvalidFileFormattingException()
        return valid_cross_sections, invalid_cross_sections

    def __has_valid_header(self, row: list[str]) -> bool:
        return (row[0].casefold() == "name"
                and row[1].casefold() == "x-coordinate"
                and row[2].casefold() == "y-coordinate"
                and row[3].casefold() == "type")

    def __parse_cross_section_syntax(self, row: list[str]) -> (
            tuple[Location, CrossSectionType] | None):
        if len(row) != 4:
            return None
        try:
            coordinates = Location(float(row[1]),
                                   float(row[2]))
        except ValueError:
            return None
        cs_type = self.__get_enum_from_type_str(row[3])
        if cs_type is not None:
            return coordinates, cs_type
        return None

    def __get_enum_from_type_str(self, cross_section_type: str) \
            -> CrossSectionType | None:
        try:
            return CrossSectionType[cross_section_type.upper()]
        except KeyError:
            return None


class InvalidFileFormattingException(Exception):
    """Exception raised when the user inputs a file that has
    no valid cross section definitions."""
    def __init__(self) -> None:
        self.message = "File has no valid cross section definitions."
