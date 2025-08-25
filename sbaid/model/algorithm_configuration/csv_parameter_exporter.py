"""This module contains an exporter class that allows exporting a parameter configuration
to a csv file."""

import csv
import io
import aiofiles

from gi.repository import Gio

from sbaid.model.algorithm_configuration.parameter_exporter import ParameterExporter
from sbaid.common import list_model_iterator
from sbaid.model.algorithm_configuration.parameter import Parameter


class CSVParameterExporter(ParameterExporter):
    """This class exports a parameter configuration to a csv file."""

    def can_handle_format(self, export_format: str) -> bool:
        return export_format == "csv"

    async def for_each_parameter(self, file: Gio.File, parameters: Gio.ListModel) -> None:
        params = self.__populate_data(parameters)
        params[0][0] = "cs_id"
        cs_ids = ["cs_id"]
        found_params = ["cs_id"]
        for param in list_model_iterator(parameters):
            for cs_index, param_index, value in await self.__format_parameter(param, cs_ids,
                                                                              found_params):
                params[cs_index][param_index] = str(value)
            if param.cross_section is None:
                cs_ids.append("")
            elif param.cross_section.id not in cs_ids:
                cs_ids.append(param.cross_section.id)
            if param.name not in found_params:
                found_params.append(param.name)

        path = file.get_path()
        assert isinstance(path, str)
        async with aiofiles.open(path, "w", newline="") as csvfile:
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerows(params)

            await csvfile.write(buffer.getvalue())

    def __populate_data(self, parameters: Gio.ListModel) -> list[list[str]]:
        """Finds all unique parameter names and cross sections and builds a 2d-list
        with x rows (amount of cross sections + 1)
        and y columns (amount of distinct parameters + 1).
         Also populates all cells with an empty string."""
        param_names: list[str] = []
        cross_sections: list[str] = []
        data: list[list[str]] = []

        for param in list_model_iterator(parameters):
            cross_section_id = ""
            if param.cross_section is not None:
                cross_section_id = param.cross_section.id

            if param.name not in param_names:
                param_names.append(param.name)
            if cross_section_id not in cross_sections:
                cross_sections.append(cross_section_id)

        for i in range(len(cross_sections) + 1):
            data.append([])
            for j in range(len(param_names)+1):  # pylint: disable=unused-variable
                data[i].append("")
        return data

    async def __format_parameter(self, parameter: Parameter, ids: list[str], header: list[str]) \
            -> list[tuple[int, int, str]]:
        entries = []
        value = ""

        if parameter.value is not None:
            value = parameter.value.print_(True)

        cross_section_id = ""
        if parameter.cross_section is not None:
            cross_section_id = parameter.cross_section.id

        try:
            cs_id_index = ids.index(cross_section_id)
        except ValueError:
            cs_id_index = len(ids)
            entries.append((cs_id_index, 0, cross_section_id))

        try:
            param_index = header.index(parameter.name)
            entries.append((cs_id_index, param_index, value))
        except ValueError:
            param_index = len(header)
            entries.append((0, len(header), parameter.name))
            entries.append((cs_id_index, param_index, value))

        return entries
