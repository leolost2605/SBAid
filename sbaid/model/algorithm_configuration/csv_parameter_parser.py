"""This module defines the CSVParameterParser class."""
import csv
import typing
import aiofiles
from typing import Tuple

from gi.repository import Gio, GLib
from sbaid.model.algorithm_configuration.parameter_parser import (
    ParameterParser, ParameterParserForeachFunc)


class CSVParameterParser(ParameterParser):
    """This class handles the parsing of CSV files containing cross sections."""

    def can_handle(self, file_path: str) -> bool:
        """Checks if the given file is a csv file."""
        # TODO: Make platform independent
        return Gio.content_type_guess(file_path)[0] == ".csv"

    async def for_each_parameter(self, file: Gio.File,
                           callback: ParameterParserForeachFunc) -> Tuple[int, int]:
        """Loads the file contents asynchronously and reads the input CSV file row by row,
        attempting to add the parameter to the parameter configuration.
        Returns the amount of added and skipped parameters."""
        path = typing.cast(str, file.get_path())

        async with aiofiles.open(path, "r+") as csvfile:
            valid_parameters = 0
            invalid_parameters = 0

            try:
                builder = file.read(None)
                info = builder.read_all(None)[1].decode("utf-8")
                rows = info.splitlines()
                csv_reader = csv.reader(rows)
                header = next(csv_reader)
                for row in csv_reader:

                    row_info = dict(zip(header, row))
                    raw_number = row_info.get("QS_NR", '').strip()
                    cross_section = raw_number

                    for param_name, value in row_info.items():
                        if param_name == "QS_NR":
                            continue
                        value_str = value.strip()
                        if value_str == '':
                            continue

                        try:
                            if value_str == 'True':
                                variant = GLib.Variant('bool', True)
                            elif value_str == 'False':
                                variant = GLib.Variant('bool', False)
                            elif value_str == 'False':
                                variant = GLib.Variant('float', float(value_str))
                            else:
                                variant = GLib.Variant('int', int(value_str))
                        except Exception:
                            raise ValueError("Unsupported value")

                        if not callback(param_name, cross_section, variant):
                            return valid_parameters, invalid_parameters
                        valid_parameters += 1

            except Exception:
                invalid_parameters += 1

        return valid_parameters, invalid_parameters
