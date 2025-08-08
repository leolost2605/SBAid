"""This module defines the CSVParameterParser class."""
import csv
import typing
import aiofiles
from gi.repository import Gio, GLib

from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)
from sbaid.model.network.csv_cross_section_parser import InvalidFileFormattingException


class CSVParameterParser(ParameterParser):
    """This class handles the parsing of CSV files containing global
    and cross section parameters."""

    def can_handle_file(self, file_path: str) -> bool:
        """Checks if the given file is a csv file."""
        return Gio.content_type_guess(file_path)[0] == ".csv"

    async def for_each_parameter(self, file: Gio.File,
                                 foreach_func: ParameterParserForeachFunc) -> tuple[int, int]:
        """Loads the file contents asynchronously and reads the input CSV file row by row,
        attempting to add the parameter to the parameter configuration.
        Returns the amount of added and skipped parameters."""
        path = typing.cast(str, file.get_path())

        async with aiofiles.open(path, "r+") as csvfile:
            valid_parameters = 0
            invalid_parameters = 0
            csv_reader = csv.reader(await csvfile.readlines())
            try:
                header = next(csv_reader)
            except StopIteration as exc:
                raise InvalidFileFormattingException() from exc
            if header[0].casefold() != "cs_id":
                raise InvalidFileFormattingException()
            for row in csv_reader:
                for i in range(len(row)-1):
                    if row[i+1] != "" and foreach_func(header[i + 1], row[0],
                                                       GLib.Variant.parse(None, row[i+1])):
                        valid_parameters += 1
                    else:
                        invalid_parameters += 1
        return valid_parameters, invalid_parameters
